"""Check publication inputs and exposure boundaries; not a runtime certification."""
import ast
import importlib
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BRANCH = 'codex/unique-template-drafts'


def read(name):
    return json.loads((ROOT / name).read_text())


def main():
    meta = read('marketplace.round10.json')
    sources = read('sources.round10.lock.json')
    eligibility = read('eligibility.round10.json')
    pins = read('images.round10.lock.json')
    assert len(meta) == 15 and set(meta) == set(sources) == set(eligibility)
    assert len({m['name'] for m in meta.values()}) == 15
    generated = {}
    for group in 'abc':
        catalog = importlib.import_module('catalog_round10_' + group)
        assert not set(generated) & set(catalog.CATALOG)
        generated.update({slug: catalog.configuration(slug) for slug in catalog.CATALOG})
    assert set(generated) == set(meta)
    for path in ROOT.glob('marketplace*.json'):
        if 'round10' not in path.name:
            assert not set(meta) & set(json.loads(path.read_text())), path.name
    for tag, pin in pins.items():
        assert pin.startswith(tag + '@sha256:')
        assert re.fullmatch(r'.+@sha256:[a-f0-9]{64}', pin)
    count = searches = 0
    dockerfiles = set()
    for slug, m in meta.items():
        assert set(m) == {'name', 'description', 'category', 'image'}, slug
        assert 0 < len(m['description']) <= 75 and m['image'].startswith('https://')
        e = eligibility[slug]
        assert e['criterion'] == 'no_matching_public_listing_found', slug
        assert e['matchingListings'] == [] and len(e['queries']) >= 2, slug
        excluded = {x['code'] for x in e.get('excludedMatches', [])}
        for q in e['queries']:
            searches += 1
            assert not q['hasNextPage'], (slug, q['query'])
            assert q['resultCount'] == len(q['results'])
            assert re.fullmatch(r'[a-f0-9]{64}', q['receiptSha256'])
            assert all(x['code'] in excluded for x in q['results']), (slug, q['query'])
        assert re.fullmatch(r'[a-f0-9]{40}', sources[slug]['sha']), slug
        assert sources[slug]['archived'] is False, slug
        folder = ROOT / 'templates/round10' / slug
        config = json.loads((folder / 'template.json').read_text())
        assert config == generated[slug], slug + ': stale generated configuration'
        services = list(config['services'].values())
        by_name = {s['name']: s for s in services}
        assert len(by_name) == len(services)
        exposed = [s for s in services if s['networking']['serviceDomains']]
        assert len(exposed) == 1, slug
        edge = exposed[0]
        assert edge['build']['dockerfilePath'] == 'shared/round10-gateway/Dockerfile'
        assert edge['variables']['OWNER_AUTH']['defaultValue'] == 'true'
        assert edge['variables']['OWNER_SCOPE']['defaultValue'] == 'all'
        assert edge['variables']['ACCESS_PASSWORD']['defaultValue'].startswith('${{secret(')
        for s in services:
            count += 1
            assert not s['networking'].get('tcpProxies')
            mounts = list(s.get('volumeMounts', {}).values())
            assert len(mounts) <= 1
            if mounts:
                assert mounts[0]['mountPath'].startswith('/')
                assert s['deploy']['requiredMountPath'] == mounts[0]['mountPath']
            src = s['source']
            if 'image' in src:
                assert src['image'] in pins.values(), (slug, src)
            else:
                assert src == {'repo': 'orenaksakal/railway-templates', 'branch': BRANCH}
                path = s['build']['dockerfilePath']
                assert path == s['variables']['RAILWAY_DOCKERFILE_PATH']['defaultValue']
                assert (ROOT / path).is_file(), (slug, path)
                dockerfiles.add(path)
            for key, var in s['variables'].items():
                assert var['description'] and isinstance(var['isOptional'], bool)
                for target, field in re.findall(r'\$\{\{([\w-]+)\.([\w]+)\}\}', var.get('defaultValue', '')):
                    assert target in by_name, (slug, key, target)
                    assert field in by_name[target]['variables'] or field in ('RAILWAY_PRIVATE_DOMAIN', 'RAILWAY_PUBLIC_DOMAIN')
                    if field == 'RAILWAY_PUBLIC_DOMAIN':
                        assert by_name[target]['networking']['serviceDomains']
        readme = (folder / 'README.md').read_text()
        for section in ['# Deploy and Host', '## About Hosting', '## Why Deploy',
                        '## Common Use Cases', '## Dependencies for',
                        '### Deployment Dependencies', '## First use']:
            assert section in readme, (slug, section)
        assert 'acceptance' in readme.lower() and 'unverified' in readme.lower(), slug
        for path in folder.glob('*.sh'):
            subprocess.run(['sh', '-n', str(path)], check=True)
        for path in folder.glob('*.py'):
            ast.parse(path.read_text())
    for path in dockerfiles:
        stages = set()
        for line in (ROOT / path).read_text().splitlines():
            parts = line.split()
            if not parts:
                continue
            if parts[0] == 'FROM':
                assert parts[1] == 'scratch' or parts[1] in stages or re.search(r'@sha256:[a-f0-9]{64}$', parts[1]), (path, line)
                if len(parts) > 3 and parts[-2].lower() == 'as':
                    stages.add(parts[-1])
            if parts[0] == 'COPY' and '--from=' not in line:
                for source in [x for x in parts[1:-1] if not x.startswith('--')]:
                    assert (ROOT / source).exists(), (path, source)
    for path in (ROOT / 'scripts').glob('*round10*.py'):
        ast.parse(path.read_text())
    print(f'PASS: 15 templates / {count} services / {searches} marketplace checks.')
    print('PASS: pins, references, private dependencies, owner access, mounts, source paths and publication documentation.')
    print('Unverified: builds, Railway application workflows, restart and recovery.')


if __name__ == '__main__':
    main()
