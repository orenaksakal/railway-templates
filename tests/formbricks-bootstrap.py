"""Opt-in PostgreSQL/Hub integration test using cached images and temporary RAM data.

Build templates/formbricks/Hub.Dockerfile as railway-templates/formbricks-hub:bootstrap-test,
then run: python3 tests/formbricks-bootstrap.py
No images are pulled, no ports are published, and all test containers are removed.
"""
import os
from pathlib import Path
import shutil
import subprocess
import time
import uuid

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'templates/formbricks'
APP_IMAGE = os.environ.get('FORMBRICKS_TEST_APP_IMAGE', 'railway-templates/formbricks-formbricks:test')
HUB_IMAGE = os.environ.get('FORMBRICKS_TEST_HUB_IMAGE', 'railway-templates/formbricks-hub:bootstrap-test')
DB_IMAGE = os.environ.get('FORMBRICKS_TEST_DB_IMAGE', 'railway-templates/formbricks-postgres:test')
PREFIX = 'formbricks-bootstrap-' + uuid.uuid4().hex[:10]
DB = PREFIX + '-postgres'
HUB = PREFIX + '-hub'
DATABASE_URL = 'postgresql://formbricks:bootstrap-test@postgres:5432/formbricks?sslmode=disable'
containers = []


def docker(*args, check=True, timeout=180, input=None):
    result = subprocess.run(['docker', *args], text=True, input=input, capture_output=True, timeout=timeout)
    if check and result.returncode:
        raise RuntimeError(f'Docker command {args[0]} failed: {result.stderr[-2500:]}')
    return result


def sql(statement):
    return docker('exec', '-i', DB, 'psql', '-XAt', '-v', 'ON_ERROR_STOP=1', '-U', 'formbricks', '-d', 'formbricks',
                  input=statement).stdout.strip()


def wait_for(check, timeout=120):
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if check():
            return
        time.sleep(1)
    raise AssertionError('Timed out waiting for test condition')


def app_script(script, *, database_url=DATABASE_URL):
    name = PREFIX + '-app-' + uuid.uuid4().hex[:6]
    containers.append(name)
    return docker('run', '--rm', '--pull=never', '--name', name, '--network', PREFIX,
                  '--memory=768m', '--log-opt', 'max-size=1m',
                  '--tmpfs', '/home/nextjs/apps/web/uploads:uid=1001,gid=1001',
                  '--tmpfs', '/home/nextjs/apps/web/saml-connection:uid=1001,gid=1001',
                  '-v', f'{SOURCE}:/home/nextjs/railway-template:ro',
                  '-e', f'DATABASE_URL={database_url}', '--entrypoint', 'node', APP_IMAGE, script,
                  check=False)


def assert_hub_waiting():
    assert docker('inspect', '-f', '{{.State.Running}}', HUB).stdout.strip() == 'true'
    assert sql("SELECT to_regclass('public.goose_db_version') IS NULL;") == 't'


try:
    if shutil.disk_usage(ROOT).free < 30 * 1024**3:
        raise RuntimeError('At least 30 GiB free disk is required')
    for image in (APP_IMAGE, HUB_IMAGE, DB_IMAGE):
        docker('image', 'inspect', image)
    docker('network', 'create', '--internal', PREFIX)
    containers.append(DB)
    docker('run', '-d', '--pull=never', '--name', DB, '--network', PREFIX, '--network-alias', 'postgres',
           '--memory=384m', '--tmpfs', '/var/lib/postgresql:rw,size=192m',
           '--log-opt', 'max-size=1m', '-e', 'PGDATA=/var/lib/postgresql/data',
           '-e', 'POSTGRES_PASSWORD=bootstrap-test', '-e', 'POSTGRES_USER=postgres',
           '-e', 'APP_USER=formbricks', '-e', 'APP_DB=formbricks', '-e', 'APP_PASSWORD=bootstrap-test',
           '-e', 'ENABLE_VECTOR=true', DB_IMAGE)
    wait_for(lambda: docker('exec', DB, 'pg_isready', '-U', 'formbricks', '-d', 'formbricks', check=False).returncode == 0)
    wait_for(lambda: docker('exec', DB, 'psql', '-XAt', '-U', 'formbricks', '-d', 'formbricks', '-c', 'SELECT 1', check=False).returncode == 0)
    containers.append(HUB)
    docker('run', '-d', '--pull=never', '--name', HUB, '--network', PREFIX, '--memory=256m',
           '--log-opt', 'max-size=1m', '-e', f'DATABASE_URL={DATABASE_URL}',
           '-e', 'API_KEY=' + 'a' * 64, '-e', 'FORMBRICKS_MIGRATIONS_WAIT_SECONDS=180', HUB_IMAGE)
    time.sleep(3)
    assert_hub_waiting()
    print('PASS: Hub waits on a fresh database with no Formbricks service or DNS record', flush=True)

    migration = app_script('packages/database/dist/scripts/apply-migrations.js')
    assert migration.returncode == 0, (migration.stdout + migration.stderr)[-3000:]
    # Upstream migration logging differs between image builds; exit status and
    # the real dependent Goose/River migrations below establish success.
    assert_hub_waiting()
    print('PASS: real pinned Formbricks migrations finish before Hub starts its migrations', flush=True)

    sql("""CREATE TABLE public.railway_template_migrations (
      component text PRIMARY KEY, release text NOT NULL, completed_at timestamptz NOT NULL DEFAULT now());
      INSERT INTO public.railway_template_migrations VALUES ('formbricks', 'previous-release', now());""")
    time.sleep(3)
    assert_hub_waiting()
    print('PASS: a restored marker from an older release does not unblock Hub', flush=True)

    recorded = app_script('/home/nextjs/railway-template/record-migrations.mjs')
    assert recorded.returncode == 0, recorded.stderr
    wait_for(lambda: docker('exec', HUB, 'wget', '-q', '-T', '2', '-O', '/dev/null', 'http://localhost:8080/health', check=False).returncode == 0)
    assert sql('SELECT max(version_id) FROM goose_db_version;') == '26'
    assert sql("SELECT to_regclass('public.river_job') IS NOT NULL;") == 't'
    print('PASS: exact release marker unblocks real Goose/River migrations and Hub HTTP health', flush=True)

    assert app_script('/home/nextjs/railway-template/record-migrations.mjs').returncode == 0
    assert sql('SELECT count(*) FROM public.railway_template_migrations;') == '1'
    print('PASS: publishing migration completion is idempotent', flush=True)

    broken = app_script('/home/nextjs/railway-template/record-migrations.mjs', database_url='postgresql://user:secret-not-for-logs@missing.invalid/db')
    assert broken.returncode != 0
    assert 'secret-not-for-logs' not in broken.stdout + broken.stderr
    assert 'Could not record Formbricks migration completion' in broken.stderr
    print('PASS: database publication failure exits nonzero without leaking credentials', flush=True)

    sql("UPDATE public.railway_template_migrations SET release = 'previous-release' WHERE component = 'formbricks';")
    name = PREFIX + '-timeout'
    containers.append(name)
    timeout_result = docker('run', '--rm', '--pull=never', '--name', name, '--network', PREFIX,
                            '--memory=128m', '--log-opt', 'max-size=1m',
                            '-e', f'DATABASE_URL={DATABASE_URL}',
                            '-e', 'FORMBRICKS_MIGRATIONS_WAIT_SECONDS=1', HUB_IMAGE, check=False, timeout=15)
    assert timeout_result.returncode != 0
    assert 'Formbricks migrations did not become ready' in timeout_result.stderr, (timeout_result.stdout + timeout_result.stderr)[-1500:]
    print('PASS: missing current release fails closed within the configured wait timeout', flush=True)
finally:
    for name in reversed(containers):
        docker('rm', '-fv', name, check=False)
    docker('network', 'rm', PREFIX, check=False)
