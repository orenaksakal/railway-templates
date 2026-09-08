"""Single source for native Railway template definitions and local Compose checks."""
from pathlib import Path
import json
import uuid

ROOT = Path(__file__).resolve().parents[1]
REPO = 'orenaksakal/railway-templates'
LOCK_PATH = ROOT / 'images.lock.json'
IMAGE_LOCK = json.loads(LOCK_PATH.read_text()) if LOCK_PATH.exists() else {}
SECRET = '${{secret(64, "abcdef0123456789")}}'
PG16 = 'pgvector/pgvector:pg16'
VALKEY = 'valkey/valkey@sha256:e0eb7c480958d32bdc4357a74bdd70653ae15f2f9b4c93c4a5a9fad1dc471c84'

def ref(service, variable):
    return '${{' + service + '.' + variable + '}}'

def service(name, *, image=None, dockerfile=None, env=None, port=None, volume=None, health=None, command=None):
    image = IMAGE_LOCK.get(image, image)
    value = {'name': name, 'source': {'image': image} if image else {'repo': REPO, 'branch': 'main'},
             'variables': {k: {'defaultValue': str(v), 'isOptional': False} for k, v in (env or {}).items()},
             'deploy': {'restartPolicyType': 'ON_FAILURE', 'restartPolicyMaxRetries': 5},
             'networking': {'serviceDomains': {}}}
    if dockerfile:
        value['build'] = {'builder': 'DOCKERFILE', 'dockerfilePath': dockerfile}
    if port:
        value['networking']['serviceDomains'] = {f'<hasDomain>:{port}': {'port': port}}
    if health:
        value['deploy'].update(healthcheckPath=health, healthcheckTimeout=600)
    if command:
        value['deploy']['startCommand'] = command
    if volume:
        key = str(uuid.uuid5(uuid.NAMESPACE_URL, name + volume))
        value['volumeMounts'] = {key: {'mountPath': volume}}
        value['deploy']['requiredMountPath'] = volume
    return value

def database(app, *, version=16, vector=False, tooljet=False):
    image = f'pgvector/pgvector:pg{version}' if vector else f'postgres:{version}'
    env = {'POSTGRES_USER': 'postgres', 'POSTGRES_PASSWORD': SECRET, 'POSTGRES_DB': 'postgres',
           'APP_USER': app, 'APP_DB': app, 'APP_PASSWORD': SECRET,
           'PGDATA': '/var/lib/postgresql/data/pgdata', 'ENABLE_VECTOR': str(vector).lower(),
           'ALLOW_APP_DATABASE_CREATION': str(tooljet).lower(),
           'DATABASE_URL': f'postgresql://{app}:' + ref('postgres', 'APP_PASSWORD') + '@' + ref('postgres', 'RAILWAY_PRIVATE_DOMAIN') + f':5432/{app}'}
    value = service('postgres', dockerfile=f'templates/{app}/Postgres.Dockerfile', env=env,
                    volume='/var/lib/postgresql' if version >= 18 else '/var/lib/postgresql/data')
    path = ROOT / 'templates' / app / 'Postgres.Dockerfile'
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(f'FROM {IMAGE_LOCK.get(image, image)}\nCOPY --chmod=755 shared/postgres/init.sh /docker-entrypoint-initdb.d/10-app.sh\n')
    return value

def redis(*, image=VALKEY):
    return service('redis', image=image, volume='/data',
                   command='sh -c \'exec valkey-server --bind 0.0.0.0 --appendonly yes --maxmemory-policy noeviction --requirepass "$REDIS_PASSWORD"\'',
                   env={'REDIS_PASSWORD': SECRET,
                        'REDIS_URL': 'redis://:' + ref('redis', 'REDIS_PASSWORD') + '@' + ref('redis', 'RAILWAY_PRIVATE_DOMAIN') + ':6379'})

def formbricks():
    db, cache = database('formbricks', version=18, vector=True), redis()
    env = {'NODE_ENV': 'production', 'PORT': '3000', 'HOSTNAME': '0.0.0.0',
           'WEBAPP_URL': 'https://${{RAILWAY_PUBLIC_DOMAIN}}', 'NEXTAUTH_URL': 'https://${{RAILWAY_PUBLIC_DOMAIN}}',
           'NEXTAUTH_SECRET': SECRET, 'ENCRYPTION_KEY': SECRET, 'CRON_SECRET': SECRET,
           'DATABASE_URL': ref('postgres', 'DATABASE_URL') + '?schema=public',
           'REDIS_URL': ref('redis', 'REDIS_URL'), 'HUB_API_KEY': SECRET,
           'HUB_API_URL': 'http://' + ref('hub', 'RAILWAY_PRIVATE_DOMAIN') + ':8080',
           'CUBEJS_API_URL': 'http://' + ref('cube', 'RAILWAY_PRIVATE_DOMAIN') + ':4000',
           'CUBEJS_API_SECRET': SECRET, 'CUBEJS_JWT_ISSUER': 'formbricks-web', 'CUBEJS_JWT_AUDIENCE': 'formbricks-cube',
           'EMAIL_VERIFICATION_DISABLED': '1', 'PASSWORD_RESET_DISABLED': '1', 'TELEMETRY_DISABLED': '1'}
    app = service('formbricks', dockerfile='templates/formbricks/Dockerfile', env=env,
                  port=3000, volume='/home/nextjs/apps/web/uploads', health='/health')
    hub = service('hub', dockerfile='templates/formbricks/Hub.Dockerfile', env={
        'API_KEY': ref('formbricks', 'HUB_API_KEY'), 'DATABASE_URL': ref('postgres', 'DATABASE_URL') + '?sslmode=disable',
        'FORMBRICKS_MIGRATIONS_URL': 'http://' + ref('formbricks', 'RAILWAY_PRIVATE_DOMAIN') + ':3001/migrations'})
    cube = service('cube', dockerfile='templates/formbricks/Cube.Dockerfile', env={
        'CUBEJS_DB_TYPE': 'postgres', 'CUBEJS_DB_HOST': ref('postgres', 'RAILWAY_PRIVATE_DOMAIN'),
        'CUBEJS_DB_NAME': 'formbricks', 'CUBEJS_DB_USER': 'formbricks', 'CUBEJS_DB_PASS': ref('postgres', 'APP_PASSWORD'),
        'CUBEJS_DB_PORT': '5432', 'CUBEJS_API_SECRET': ref('formbricks', 'CUBEJS_API_SECRET'),
        'CUBEJS_JWT_ISSUER': 'formbricks-web', 'CUBEJS_JWT_AUDIENCE': 'formbricks-cube',
        'CUBEJS_DEFAULT_API_SCOPES': 'meta,data', 'CUBEJS_EXTERNAL_DEFAULT': 'false', 'CUBEJS_CACHE_AND_QUEUE_DRIVER': 'memory'})
    return [db, cache, app, hub, cube]

def tooljet():
    db, cache = database('tooljet', tooljet=True), redis()
    env = {'NODE_ENV': 'production', 'TOOLJET_EDITION': 'ce', 'PORT': '3000', 'SERVE_CLIENT': 'true',
           'TOOLJET_HOST': 'https://${{RAILWAY_PUBLIC_DOMAIN}}', 'LOCKBOX_MASTER_KEY': SECRET, 'SECRET_KEY_BASE': SECRET,
           'PG_HOST': ref('postgres', 'RAILWAY_PRIVATE_DOMAIN'), 'PG_PORT': '5432', 'PG_USER': 'tooljet',
           'PG_PASS': ref('postgres', 'APP_PASSWORD'), 'PG_DB': 'tooljet', 'PG_SSL': 'false',
           'TOOLJET_DB_HOST': ref('postgres', 'RAILWAY_PRIVATE_DOMAIN'), 'TOOLJET_DB_PORT': '5432',
           'TOOLJET_DB_USER': 'tooljet', 'TOOLJET_DB_PASS': ref('postgres', 'APP_PASSWORD'), 'TOOLJET_DB': 'tooljet_data',
           'TOOLJET_DB_SSL': 'false', 'TOOLJET_DB_RECONFIG': 'true', 'ENABLE_TOOLJET_DB': 'true',
           'PGRST_HOST': 'postgrest.railway.internal:3000', 'PGRST_JWT_SECRET': SECRET,
           'REDIS_HOST': ref('redis', 'RAILWAY_PRIVATE_DOMAIN'), 'REDIS_PORT': '6379', 'REDIS_PASSWORD': ref('redis', 'REDIS_PASSWORD'),
           'WORKER': 'true', 'TOOLJET_QUEUE_DASH_PASSWORD': SECRET, 'TOOLJET_WORKFLOW_SANDBOX_BYPASS': 'false',
           'DISABLE_TOOLJET_TELEMETRY': 'true', 'SMTP_DISABLED': 'true'}
    env['PGRST_HOST'] = ref('postgrest', 'RAILWAY_PRIVATE_DOMAIN') + ':3000'
    app = service('tooljet', dockerfile='templates/tooljet/Dockerfile', env=env, port=3000, health='/api/health')
    rest = service('postgrest', image='postgrest/postgrest:v12.0.2', env={
        'PGRST_DB_URI': 'postgresql://tooljet:' + ref('postgres', 'APP_PASSWORD') + '@' + ref('postgres', 'RAILWAY_PRIVATE_DOMAIN') + ':5432/tooljet_data',
        'PGRST_JWT_SECRET': ref('tooljet', 'PGRST_JWT_SECRET'), 'PGRST_DB_PRE_CONFIG': 'postgrest.pre_config', 'PGRST_SERVER_PORT': '3000'})
    return [db, cache, app, rest]

def affine():
    return [database('affine', vector=True), redis(), service('affine', dockerfile='templates/affine/Dockerfile',
        port=3010, health='/info', volume='/root/.affine', env={
            'DATABASE_URL': ref('postgres', 'DATABASE_URL'), 'REDIS_SERVER_HOST': ref('redis', 'RAILWAY_PRIVATE_DOMAIN'),
            'REDIS_SERVER_PORT': '6379', 'REDIS_SERVER_PASSWORD': ref('redis', 'REDIS_PASSWORD'),
            'AFFINE_SERVER_EXTERNAL_URL': 'https://${{RAILWAY_PUBLIC_DOMAIN}}', 'AFFINE_SERVER_HOST': '0.0.0.0',
            'AFFINE_SERVER_PORT': '3010', 'PORT': '3010', 'AFFINE_INDEXER_ENABLED': 'false'})]

def openproject():
    return [database('openproject', version=17), service('openproject', dockerfile='templates/openproject/Dockerfile',
        port=80, health='/health_checks/default', volume='/var/openproject/assets', env={
            'DATABASE_URL': ref('postgres', 'DATABASE_URL'),
            'SECRET_KEY_BASE': SECRET, 'OPENPROJECT_HOST__NAME': '${{RAILWAY_PUBLIC_DOMAIN}}',
            'OPENPROJECT_HTTPS': 'true', 'OPENPROJECT_HSTS': 'true', 'PORT': '8080',
            'OPENPROJECT_SEED__ADMIN__USER__PASSWORD': SECRET,
            'OPENPROJECT_SEED__ADMIN__USER__PASSWORD__RESET': 'true',
            'OPENPROJECT_COLLABORATIVE__EDITING__HOCUSPOCUS__URL': 'auto',
            'PG_STARTUP_WAIT_TIME': '60', 'RAILS_MIN_THREADS': '2', 'RAILS_MAX_THREADS': '8'})]

def firecrawl():
    cache = redis()
    # Firecrawl upstream marks Valkey untested: use Redis 7.4 and the same persistent/authenticated setup.
    cache['source']['image'] = IMAGE_LOCK.get('redis:7.4', 'redis:7.4')
    cache['deploy']['startCommand'] = cache['deploy']['startCommand'].replace('valkey-server', 'redis-server')
    db = service('postgres', image='ghcr.io/firecrawl/nuq-postgres@sha256:aed86f62858f29bd971abddcdeb301c12888098d2cf5d33c1ba42b053bc460f6',
        volume='/var/lib/postgresql/data', env={'POSTGRES_USER': 'postgres', 'POSTGRES_DB': 'postgres', 'POSTGRES_PASSWORD': SECRET,
            'PGDATA': '/var/lib/postgresql/data/pgdata'})
    rabbit = service('rabbitmq', image='rabbitmq:3.13', volume='/var/lib/rabbitmq', env={
        'RABBITMQ_DEFAULT_USER': 'firecrawl', 'RABBITMQ_DEFAULT_PASS': SECRET, 'RABBITMQ_NODENAME': 'rabbit@localhost'})
    browser = service('browser', image='ghcr.io/firecrawl/playwright-service@sha256:df1a393ce8bfc3801570a826a9b0dcc400ae48789adb4a0ad9d6cbf0229b059b',
        env={'PORT': '3000', 'MAX_CONCURRENT_PAGES': '2', 'ALLOW_LOCAL_WEBHOOKS': 'false', 'BLOCK_MEDIA': 'true'})
    api = service('api', image='ghcr.io/firecrawl/firecrawl@sha256:03c94c9f99e0e4fc4ab9c844d2f64abb649396503180b14aeaf0a1169da88bab', env={
        'HOST': '0.0.0.0', 'PORT': '3002', 'ENV': 'local', 'USE_DB_AUTHENTICATION': 'false',
        'REDIS_URL': ref('redis', 'REDIS_URL'), 'REDIS_RATE_LIMIT_URL': ref('redis', 'REDIS_URL'),
        'POSTGRES_HOST': ref('postgres', 'RAILWAY_PRIVATE_DOMAIN'), 'POSTGRES_PORT': '5432',
        'POSTGRES_DB': 'postgres', 'POSTGRES_USER': 'postgres', 'POSTGRES_PASSWORD': ref('postgres', 'POSTGRES_PASSWORD'),
        'NUQ_RABBITMQ_URL': 'amqp://firecrawl:' + ref('rabbitmq', 'RABBITMQ_DEFAULT_PASS') + '@' + ref('rabbitmq', 'RAILWAY_PRIVATE_DOMAIN') + ':5672',
        'PLAYWRIGHT_MICROSERVICE_URL': 'http://' + ref('browser', 'RAILWAY_PRIVATE_DOMAIN') + ':3000/scrape',
        'NUM_WORKERS_PER_QUEUE': '2', 'CRAWL_CONCURRENT_REQUESTS': '2', 'MAX_CONCURRENT_JOBS': '2', 'BROWSER_POOL_SIZE': '2',
        'EXTRACT_WORKER_PORT': '3004', 'WORKER_PORT': '3005', 'HARNESS_STARTUP_TIMEOUT_MS': '180000',
        'BULL_AUTH_KEY': SECRET, 'ALLOW_LOCAL_WEBHOOKS': 'false'}, command='node dist/src/harness.js --start-docker')
    gateway = service('firecrawl', dockerfile='templates/firecrawl/Gateway.Dockerfile', port=8080, health='/healthz',
                      env={'PORT': '8080', 'API_KEY': SECRET, 'UPSTREAM_URL': 'http://' + ref('api', 'RAILWAY_PRIVATE_DOMAIN') + ':3002'})
    return [db, cache, rabbit, browser, api, gateway]

CATALOG = {'formbricks': formbricks, 'firecrawl': firecrawl, 'affine': affine, 'openproject': openproject, 'tooljet': tooljet}

def generate():
    for name, factory in CATALOG.items():
        services = factory()
        config = {'services': {str(uuid.uuid5(uuid.NAMESPACE_URL, name + '/' + s['name'])): s for s in services}}
        path = ROOT / 'templates' / name / 'template.json'
        path.write_text(json.dumps(config, indent=2) + '\n')
        print(path.relative_to(ROOT))

if __name__ == '__main__':
    generate()
