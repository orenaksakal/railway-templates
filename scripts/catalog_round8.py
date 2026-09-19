"""Twenty marketplace-gap drafts, with explicit eligibility evidence."""
import json
import uuid
from pathlib import Path
import catalog_round3 as base

ROOT = Path(__file__).resolve().parents[1]
BRANCH = 'codex/unique-template-drafts'
secret, ref, public = base.secret, base.ref, base.public


def svc(name, **kwargs):
    if kwargs.get('image'):
        kwargs['image'] = json.loads((ROOT / 'images.round8.lock.json').read_text())[kwargs['image']]
    value = base.svc(name, **kwargs)
    if 'repo' in value['source']:
        value['source']['branch'] = BRANCH
    return value


def protected(slug, port, *, image=None, dockerfile=None, env=None, volume=None, command=None):
    core = svc('core', image=image, dockerfile=dockerfile, env=env, volume=volume, command=command)
    edge = svc(slug, dockerfile='shared/round6-gateway/Dockerfile', port=8080, health='/healthz', env={
        'UPSTREAM_HOST': ref('core', 'RAILWAY_PRIVATE_DOMAIN'), 'UPSTREAM_PORT': port,
        'OWNER_AUTH': 'true', 'OWNER_SCOPE': 'all', 'ACCESS_PASSWORD': secret(),
    })
    return [core, edge]


def solidinvoice():
    db = svc('mysql', image='mysql:8.0', volume='/var/lib/mysql', env={
        'MYSQL_DATABASE': 'solidinvoice', 'MYSQL_USER': 'solidinvoice',
        'MYSQL_PASSWORD': secret(), 'MYSQL_ROOT_PASSWORD': secret(),
    })
    return [db] + protected('solidinvoice', 8765, image='solidinvoice/solidinvoice:3.0.1',
        volume='/etc/solidinvoice', env={
            'SOLIDINVOICE_ENV': 'prod', 'SOLIDINVOICE_DEBUG': '0',
            'SOLIDINVOICE_CONFIG_DIR': '/etc/solidinvoice',
            'SETUP_DATABASE_HOST': (ref('mysql', 'RAILWAY_PRIVATE_DOMAIN'), 'Copy this private host into the protected database installer; not an application configuration key.'),
            'SETUP_DATABASE_PORT': (3306, 'Use this port in the database installer.'),
            'SETUP_DATABASE_NAME': ('solidinvoice', 'Use this database name in the installer.'),
            'SETUP_DATABASE_USER': ('solidinvoice', 'Use this restricted database user in the installer.'),
            'SETUP_DATABASE_PASSWORD': (ref('mysql', 'MYSQL_PASSWORD'), 'Copy this generated password into the protected installer; keep it private.'),
        })


def titra():
    db = svc('mongodb', image='mongo:7.0', volume='/data/db', env={
        'MONGO_INITDB_ROOT_USERNAME': 'titra_admin', 'MONGO_INITDB_ROOT_PASSWORD': secret(),
    })
    return [db] + protected('titra', 3000, image='titraio/titra:v1.1.0', env={
        'ROOT_URL': public('titra'), 'PORT': 3000,
        'MONGO_URL': 'mongodb://titra_admin:' + ref('mongodb', 'MONGO_INITDB_ROOT_PASSWORD') + '@' +
                     ref('mongodb', 'RAILWAY_PRIVATE_DOMAIN') + ':27017/titra?authSource=admin&directConnection=true',
    })


def dumb(slug, volume='/app/data', extra=None):
    images = {'dumbpad': '1.0.4', 'dumbassets': '1.0.11'}
    return protected(slug, 3000, image='dumbwareio/' + slug + ':' + images.get(slug, 'latest'),
        volume=volume, env={
            'PORT': 3000, 'NODE_ENV': 'production', 'BASE_URL': public(slug),
            'ALLOWED_ORIGINS': public(slug),
            slug.upper() + '_PIN': ('${{secret(10, "0123456789")}}', 'Generated ten-digit native PIN. The separate owner gateway must also remain enabled.'),
            **(extra or {}),
        })


CATALOG = {
    'jelu': lambda: protected('jelu', 11111, image='wabayang/jelu:0.87.3', volume='/data', env={
        'JELU_DATABASE_PATH': '/data/database/', 'JELU_FILES_IMAGES': '/data/images/',
        'JELU_FILES_IMPORTS': '/data/imports/', 'SERVER_PORT': 11111,
    }),
    'grimoire': lambda: protected('grimoire', 3210, dockerfile='templates/grimoire/Dockerfile', volume='/data', env={
        'HOST': '0.0.0.0', 'PORT': 3210, 'DATA_DIR': '/data', 'XDG_CONFIG_HOME': '/data/config',
        'HOME': '/data', 'NODE_ENV': 'production', 'LOG_FORMAT': 'json',
        'LITTLEIMP_IN_CONTAINER': '1', 'CORS_ORIGINS': public('grimoire'),
    }),
    'linkace': lambda: protected('linkace', 80, dockerfile='templates/linkace/Dockerfile', volume='/data', env={
        'APP_KEY': secret(32), 'APP_URL': public('linkace'), 'APP_ENV': 'production', 'APP_DEBUG': 'false',
        'DB_CONNECTION': 'sqlite', 'DB_DATABASE': '/data/database.sqlite',
        'APP_SEARCH_DRIVER': 'database', 'QUEUE_CONNECTION': 'sync', 'TRUSTED_PROXIES': '*',
    }),
    'solidinvoice': solidinvoice,
    'titra': titra,
    'fava': lambda: protected('fava', 5000, dockerfile='templates/fava/Dockerfile', volume='/data',
        env={'FAVA_HOST': '0.0.0.0', 'FAVA_PORT': 5000}),
    'yaade': lambda: protected('yaade', 9339, image='esperotech/yaade:latest', volume='/app/data',
        env={'YAADE_ADMIN_USERNAME': 'admin'}),
    'wiremock': lambda: protected('wiremock', 8080, image='wiremock/wiremock:3.13.2', volume='/home/wiremock',
        env={'WIREMOCK_OPTIONS': '--port 8080 --disable-request-logging --max-request-journal-entries 1000'}),
    'mockserver': lambda: protected('mockserver', 1080, dockerfile='templates/mockserver/Dockerfile', volume='/config',
        env={'MOCKSERVER_SERVER_PORT': 1080, 'MOCKSERVER_PERSIST_EXPECTATIONS': 'true',
             'MOCKSERVER_PERSISTED_EXPECTATIONS_PATH': '/config/expectations.json',
             'MOCKSERVER_INITIALIZATION_JSON_PATH': '/config/expectations.json',
             'MOCKSERVER_MAX_EXPECTATIONS': 1000, 'MOCKSERVER_MAX_LOG_ENTRIES': 1000}),
    'sqlpage': lambda: protected('sqlpage', 8080, dockerfile='templates/sqlpage/Dockerfile', volume='/data',
        env={'SQLPAGE_WEB_ROOT': '/data/www', 'SQLPAGE_CONFIGURATION_DIRECTORY': '/data/config',
             'DATABASE_URL': 'sqlite:///data/app.db?mode=rwc'}),
    'lingarr': lambda: protected('lingarr', 9876, image='ghcr.io/lingarr-translate/lingarr:1.3.0', volume='/app/config',
        env={'ASPNETCORE_URLS': 'http://+:9876', 'DB_CONNECTION': 'sqlite',
             'DB_HANGFIRE_SQLITE_PATH': '/app/config/Hangfire.db'}),
    'dumbpad': lambda: dumb('dumbpad'),
    'dumbassets': lambda: dumb('dumbassets', extra={'DEBUG': 'false', 'DEMO_MODE': 'false'}),
    'dumbbudget': lambda: dumb('dumbbudget', extra={'CURRENCY': 'USD'}),
    'dumbkan': lambda: dumb('dumbkan'),
    'dumbdrop': lambda: dumb('dumbdrop', '/app/uploads', {'UPLOAD_DIR': '/app/uploads', 'MAX_FILE_SIZE': 25, 'AUTO_UPLOAD': 'false'}),
    'maintainerr': lambda: protected('maintainerr', 6246, dockerfile='templates/maintainerr/Dockerfile',
        volume='/opt/data', env={'TZ': 'UTC'}),
    'olivetin': lambda: protected('olivetin', 1337, dockerfile='templates/olivetin/Dockerfile', volume='/config',
        env={'PORT': 1337}),
    'go-feature-flag': lambda: protected('go-feature-flag', 1031, dockerfile='templates/go-feature-flag/Dockerfile'),
    'flagd': lambda: protected('flagd', 8013, dockerfile='templates/flagd/Dockerfile'),
}


def configuration(slug):
    return {'services': {str(uuid.uuid5(uuid.NAMESPACE_URL, 'round8/' + slug + '/' + s['name'])): s
                         for s in CATALOG[slug]()}}


def generate():
    for slug in CATALOG:
        path = ROOT / 'templates' / slug
        path.mkdir(parents=True, exist_ok=True)
        (path / 'template.json').write_text(json.dumps(configuration(slug), indent=2) + '\n')


if __name__ == '__main__':
    generate()
