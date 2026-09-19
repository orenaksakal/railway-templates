"""Validate the recovered draft batch without claiming runtime proof."""
import ast
import json
import re
import subprocess
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]

def main():
    metadata = json.loads((ROOT / 'marketplace.round9.json').read_text())
    eligibility = json.loads((ROOT / 'eligibility.round9.json').read_text())
    pins = json.loads((ROOT / 'images.round9.lock.json').read_text())
    assert len(metadata) == 18
    assert set(eligibility) - set(metadata) == {'linkace', 'dumbdrop'}
    count = 0
    dockerfiles = set()
    for slug, meta in metadata.items():
        assert len(meta['description']) <= 75
        e = eligibility[slug]
        assert e['criterion'] == 'no_matching_public_listing_found'
        excluded = {x['code'] for x in e['excludedMatches']}
        for q in e['queries']:
            assert not q['pageInfo']['hasNextPage']
            assert all(edge['node']['code'] in excluded for edge in q['edges']), slug
        folder = ROOT / 'templates/round9' / slug
        config = json.loads((folder / 'template.json').read_text())
        services = list(config['services'].values())
        by_name = {s['name']: s for s in services}
        assert len(by_name) == len(services)
        assert sum(bool(s['networking']['serviceDomains']) for s in services) == 1, slug
        for s in services:
            count += 1
            assert not s['networking'].get('tcpProxies')
            mounts = list(s.get('volumeMounts', {}).values())
            assert len(mounts) <= 1
            if mounts:
                assert s['deploy']['requiredMountPath'] == mounts[0]['mountPath']
            src = s['source']
            if 'image' in src:
                assert src['image'] in pins.values()
                assert re.search(r'@sha256:[a-f0-9]{64}$', src['image'])
            else:
                assert src == {'repo': 'orenaksakal/railway-templates', 'branch': 'codex/unique-template-drafts'}
                path = s['build']['dockerfilePath']
                assert path == s['variables']['RAILWAY_DOCKERFILE_PATH']['defaultValue']
                assert (ROOT / path).is_file(), (slug, path)
                dockerfiles.add(path)
            for key, value in s['variables'].items():
                assert value['description'] and isinstance(value['isOptional'], bool)
                for target, field in re.findall(r'\$\{\{([\w-]+)\.([\w]+)\}\}', value.get('defaultValue', '')):
                    assert target in by_name, (slug, key, target)
                    assert field in by_name[target]['variables'] or field in ('RAILWAY_PRIVATE_DOMAIN', 'RAILWAY_PUBLIC_DOMAIN')
                    if field == 'RAILWAY_PUBLIC_DOMAIN':
                        assert by_name[target]['networking']['serviceDomains']
        readme = (folder / 'README.md').read_text()
        for heading in ['# Deploy and Host', '## About Hosting', '## Why Deploy', '## Common Use Cases', '## Dependencies for', '### Deployment Dependencies', '## First use', '## Acceptance checks']:
            assert heading in readme, (slug, heading)
        assert '../../RELEASES' not in readme and 'scripts/catalog_round5.py' not in readme
        for path in folder.glob('*.sh'):
            subprocess.run(['sh', '-n', str(path)], check=True)
        for path in folder.glob('*.py'):
            ast.parse(path.read_text())
        for path in folder.glob('*.mjs'):
            subprocess.run(['node', '--check', str(path)], check=True)
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
    for path in (ROOT / 'scripts').glob('*round9*.py'):
        ast.parse(path.read_text())
    print(f'PASS: 18 eligible drafts / {count} services; 2 duplicate holds; source paths, digest pins, private dependencies, mounts, references, required overview sections and script syntax.')
    print('Unverified: image builds, Railway startup, application workflows, persistence recovery and cost.')

if __name__ == '__main__':
    main()
