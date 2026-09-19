"""Five additional marketplace gaps: administration, scheduling and operations."""
import json
import uuid
from pathlib import Path
import catalog_round3 as base

ROOT = Path(__file__).resolve().parents[1]
BRANCH = 'codex/unique-template-drafts'
secret, ref, public = base.secret, base.ref, base.public


def svc(name, **kwargs):
    if kwargs.get('image'):
        kwargs['image'] = json.loads((ROOT / 'images.round10-c.lock.json').read_text())[kwargs['image']]
    value = base.svc(name, **kwargs)
    if 'repo' in value['source']:
        value['source']['branch'] = BRANCH
    return value


def protected(slug, port, **kwargs):
    return [svc('core', **kwargs), svc(slug,
        dockerfile='shared/round10-gateway/Dockerfile', port=8080, health='/healthz', env={
            'UPSTREAM_HOST': ref('core', 'RAILWAY_PRIVATE_DOMAIN'), 'UPSTREAM_PORT': port,
            'OWNER_AUTH': 'true', 'OWNER_SCOPE': 'all', 'ACCESS_PASSWORD': secret(),
        })]


def maria(slug):
    return svc('mariadb', image='mariadb:10.11', volume='/var/lib/mysql', env={
        'MARIADB_DATABASE': slug, 'MARIADB_USER': slug,
        'MARIADB_PASSWORD': secret(), 'MARIADB_ROOT_PASSWORD': secret(),
    })


def librebooking():
    return [maria('librebooking')] + protected('librebooking', 8080,
        dockerfile='templates/round10/librebooking/Dockerfile', volume='/data', env={
            'LB_DATABASE_NAME': 'librebooking', 'LB_DATABASE_USER': 'librebooking',
            'LB_DATABASE_HOSTSPEC': ref('mariadb', 'RAILWAY_PRIVATE_DOMAIN'),
            'LB_DATABASE_PASSWORD': ref('mariadb', 'MARIADB_PASSWORD'),
            'LB_INSTALL_PASSWORD': (secret(), 'Generated installer password. Use the existing restricted database user; leave Create database and Create user unchecked. Clear this variable after setup.'),
            'LB_ADMIN_EMAIL': (None, 'Required administrator email. Register the first application account with exactly this address after completing the protected installer.'),
            'LB_SCRIPT_URL': public('librebooking') + '/Web',
            'LB_DEFAULT_TIMEZONE': 'UTC', 'LB_APP_DEBUG': 'false',
            'LB_EMAIL_ENABLED': 'false', 'LB_PASSWORD_DISABLE_RESET': 'true',
            'LB_RESERVATION_REMINDERS_ENABLED': 'false',
            'LB_PRIVACY_VIEW_SCHEDULES': 'false', 'LB_PRIVACY_ALLOW_GUEST_RESERVATIONS': 'false',
            'LB_REGISTRATION_ALLOW_SELF_REGISTRATION': ('true', 'Enabled for the first administrator registration behind the owner gateway. Set false after creating that account; administrators can add users.'),
            'LB_UPLOADS_RESERVATION_ATTACHMENTS_ENABLED': 'true',
            'LB_UPLOADS_RESERVATION_ATTACHMENT_PATH': '/data/reservations',
            'LB_LOGGING_LEVEL': 'error', 'LB_LOGGING_SQL': 'false',
            'LB_ICS_SUBSCRIPTION_KEY': secret(),
        })


def domainmod():
    return [maria('domainmod')] + protected('domainmod', 80,
        dockerfile='templates/round10/domainmod/Dockerfile', volume='/data', env={
            'DB_HOST': ref('mariadb', 'RAILWAY_PRIVATE_DOMAIN'), 'DB_NAME': 'domainmod',
            'DB_USER': 'domainmod', 'DB_PASSWORD': ref('mariadb', 'MARIADB_PASSWORD'),
            'TZ': 'UTC',
        })


def farmos():
    db = svc('postgres', image='postgres:17', volume='/var/lib/postgresql/data', env={
        'POSTGRES_USER': 'farm', 'POSTGRES_DB': 'farm', 'POSTGRES_PASSWORD': secret(),
        'PGDATA': '/var/lib/postgresql/data/pgdata',
    })
    return [db] + protected('farmos', 80,
        dockerfile='templates/round10/farmos/Dockerfile', volume='/data', env={
            'SETUP_DATABASE_HOST': (ref('postgres', 'RAILWAY_PRIVATE_DOMAIN'), 'Copy this private hostname into the protected PostgreSQL installer. This is an operator reference, not an automatic farmOS setting.'),
            'SETUP_DATABASE_PORT': (5432, 'Use this PostgreSQL port in the installer.'),
            'SETUP_DATABASE_NAME': ('farm', 'Use this existing database name in the installer.'),
            'SETUP_DATABASE_USER': ('farm', 'Use this database user in the installer.'),
            'SETUP_DATABASE_PASSWORD': (ref('postgres', 'POSTGRES_PASSWORD'), 'Copy this generated password into the installer. Preserve it with the database backup.'),
            'TZ': 'UTC',
        })


CATALOG = {
    'backrest': lambda: protected('backrest', 9898,
        image='ghcr.io/garethgeorge/backrest:v1.14.1', volume='/data', env={
            'BACKREST_PORT': '[::]:9898', 'BACKREST_DATA': '/data/state',
            'BACKREST_CONFIG': '/data/config.json', 'BACKREST_RESTIC_COMMAND': '/bin/restic',
            'XDG_CONFIG_HOME': '/data/config', 'XDG_CACHE_HOME': '/tmp/cache', 'TZ': 'UTC',
        }),
    'speedtest-tracker': lambda: protected('speedtest-tracker', 80,
        image='ghcr.io/linuxserver/speedtest-tracker:version-v1.15.0', volume='/config', env={
            'PUID': 1000, 'PGID': 1000, 'TZ': 'UTC', 'APP_ENV': 'production',
            'APP_KEY': (secret(32), 'Generated 32-character Laravel encryption key. Preserve with the SQLite database; changing it invalidates encrypted application data.'),
            'APP_URL': public('speedtest-tracker'), 'APP_DEBUG': 'false',
            'DB_CONNECTION': 'sqlite', 'PUBLIC_DASHBOARD': 'false',
            'SPEEDTEST_SCHEDULE': ('', 'Automatic speed tests are disabled initially. Tests measure Railway regional egress, not your home Internet, and can consume billable bandwidth. Set a cron schedule only after a manual test.'),
            'PRUNE_RESULTS_OLDER_THAN': (90, 'Remove speed-test results older than 90 days using the upstream scheduler.'),
        }),
    'librebooking': librebooking,
    'domainmod': domainmod,
    'farmos': farmos,
}


def configuration(slug):
    return {'services': {str(uuid.uuid5(uuid.NAMESPACE_URL, 'round10/' + slug + '/' + s['name'])): s
                         for s in CATALOG[slug]()}}


def generate():
    for slug in CATALOG:
        path = ROOT / 'templates' / 'round10' / slug
        path.mkdir(parents=True, exist_ok=True)
        (path / 'template.json').write_text(json.dumps(configuration(slug), indent=2) + '\n')


if __name__ == '__main__':
    generate()
