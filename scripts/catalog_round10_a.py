"""Five distinct personal publishing and media marketplace gaps."""
import json
import uuid
from pathlib import Path
import catalog_round3 as base

ROOT = Path(__file__).resolve().parents[1]
BRANCH = 'codex/unique-template-drafts'
LOCK = json.loads((ROOT / 'images.round10-a.lock.json').read_text())
secret, ref, public = base.secret, base.ref, base.public


def svc(name, **kwargs):
    if kwargs.get('image'):
        kwargs['image'] = LOCK[kwargs['image']]
    service = base.svc(name, **kwargs)
    if 'repo' in service['source']:
        service['source']['branch'] = BRANCH
    return service


def protected(slug, port, **kwargs):
    return [svc('app', **kwargs), svc(slug, dockerfile='shared/round10-gateway/Dockerfile',
        port=8080, health='/healthz', env={
            'UPSTREAM_HOST': ref('app', 'RAILWAY_PRIVATE_DOMAIN'),
            'UPSTREAM_PORT': port, 'OWNER_AUTH': 'true', 'OWNER_SCOPE': 'all',
            'ACCESS_PASSWORD': secret(),
        })]


CATALOG = {
    'raneto': lambda: protected('raneto', 8080,
        dockerfile='templates/round10/raneto/Dockerfile', volume='/data', env={
            'HOST': '0.0.0.0', 'PORT': 8080, 'NODE_ENV': 'production',
            'PUBLIC_URL': public('raneto'), 'SITE_TITLE': 'My Knowledge Base',
            'SESSION_SECRET': secret(), 'RANETO_USERNAME': 'owner', 'RANETO_PASSWORD': secret(),
        }),
    'movary': lambda: protected('movary', 8080,
        dockerfile='templates/round10/movary/Dockerfile', volume='/app/storage', env={
            'APPLICATION_URL': public('movary'), 'DATABASE_MODE': 'sqlite',
            'DATABASE_SQLITE': '/app/storage/movary.sqlite',
            'TMDB_API_KEY': (None, 'Required TMDB API key from themoviedb.org/settings/api. Movie lookup needs your own key; this template does not supply one.'),
            'TMDB_ENABLE_IMAGE_CACHING': '1', 'TIMEZONE': 'UTC',
            'ENABLE_REGISTRATION': '0', 'LOG_ENABLE_FILE_LOGGING': '0',
        }),
    'pinry': lambda: protected('pinry', 80,
        dockerfile='templates/round10/pinry/Dockerfile', volume='/data', env={
            'PUBLIC_URL': public('pinry'), 'PINRY_SECRET_KEY': secret(),
            'ADMIN_USERNAME': 'owner', 'ADMIN_PASSWORD': secret(),
            'ADMIN_EMAIL': (None, 'Required email address for the initial Pinry administrator. Only used when the database has no users; email delivery is not configured.'),
        }),
    'mikochi': lambda: protected('mikochi', 8080, image='zer0tonin/mikochi:1.11.0',
        volume='/data', env={'HOST': '0.0.0.0:8080', 'DATA_DIR': '/data',
                            'USERNAME': 'owner', 'PASSWORD': secret(), 'NO_AUTH': 'false'}),
    'airstation': lambda: protected('airstation', 7331, image='cheatsnake/airstation:1.4.1',
        volume='/data', env={
            'AIRSTATION_HTTP_PORT': 7331, 'AIRSTATION_DB_DIR': '/data/database',
            'AIRSTATION_TRACKS_DIR': '/data/tracks', 'AIRSTATION_TMP_DIR': '/tmp/airstation',
            'AIRSTATION_SECRET_KEY': secret(), 'AIRSTATION_JWT_SIGN': secret(),
            'AIRSTATION_SECURE_COOKIE': 'true',
        }),
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
