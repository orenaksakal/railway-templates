"""Five gap-qualified developer tools; pins and upstream evidence live beside catalog."""
import json
import uuid
from pathlib import Path
import catalog_round3 as base

ROOT = Path(__file__).resolve().parents[1]
BRANCH = 'codex/unique-template-drafts'
secret, ref = base.secret, base.ref


def svc(name, **kwargs):
    if kwargs.get('image'):
        kwargs['image'] = json.loads((ROOT / 'images.round10-b.lock.json').read_text())[kwargs['image']]
    value = base.svc(name, **kwargs)
    if 'repo' in value['source']:
        value['source']['branch'] = BRANCH
    return value


def protected(slug, port, **kwargs):
    return [svc('core', **kwargs), svc(slug, dockerfile='shared/round10-gateway/Dockerfile',
        port=8080, health='/healthz', env={
            'UPSTREAM_HOST': ref('core', 'RAILWAY_PRIVATE_DOMAIN'), 'UPSTREAM_PORT': port,
            'OWNER_AUTH': 'true', 'OWNER_SCOPE': 'all', 'ACCESS_PASSWORD': secret(),
        })]


CATALOG = {
    'swagger-editor': lambda: protected('swagger-editor', 8080,
        image='swaggerapi/swagger-editor:v5.8.8-unprivileged'),
    'redoc': lambda: protected('redoc', 8080, dockerfile='templates/round10/redoc/Dockerfile',
        volume='/data', env={'PORT': 8080}),
    'plantuml': lambda: protected('plantuml', 8080,
        image='plantuml/plantuml-server:jetty-v1.2026.8', env={
            'PLANTUML_SECURITY_PROFILE': ('SANDBOX', 'Disable diagram access to local files and remote URLs; keep SANDBOX for this private renderer.'),
            'PLANTUML_LIMIT_SIZE': ('4096', 'Maximum rendered image width or height in pixels. Keep bounded for resource control.'),
            'JAVA_TOOL_OPTIONS': ('-Xms128m -Xmx512m', 'Initial and maximum Java heap. Provision additional memory for the JVM and Graphviz.')
        }),
    'mountebank': lambda: protected('mountebank', 2525,
        dockerfile='templates/round10/mountebank/Dockerfile', volume='/data'),
    'prism': lambda: protected('prism', 4010, dockerfile='templates/round10/prism/Dockerfile',
        volume='/data'),
}


def configuration(slug):
    return {'services': {str(uuid.uuid5(uuid.NAMESPACE_URL, 'round10/' + slug + '/' + s['name'])): s
                         for s in CATALOG[slug]()}}


def generate():
    for slug in CATALOG:
        folder = ROOT / 'templates/round10' / slug
        folder.mkdir(parents=True, exist_ok=True)
        (folder / 'template.json').write_text(json.dumps(configuration(slug), indent=2) + '\n')


if __name__ == '__main__':
    generate()
