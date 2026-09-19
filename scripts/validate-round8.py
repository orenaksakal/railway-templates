"""Static validation, including marketplace eligibility; no runtime claims."""
import ast
import json
import re
import subprocess
from catalog_round8 import ROOT, CATALOG, BRANCH, configuration


def validate():
    metadata = json.loads((ROOT / 'marketplace.round8.json').read_text())
    sources = json.loads((ROOT / 'sources.round8.lock.json').read_text())
    eligibility = json.loads((ROOT / 'eligibility.round8.json').read_text())
    locks = json.loads((ROOT / 'images.round8.lock.json').read_text())
    assert len(CATALOG) == 20 and set(CATALOG) == set(metadata) == set(sources) == set(eligibility)
    for name in ['marketplace.json', 'marketplace.round3.json', 'marketplace.round4.json', 'marketplace.round6.json', 'marketplace.round7.json']:
        path = ROOT / name
        if path.exists():
            assert not set(CATALOG).intersection(json.loads(path.read_text())), name
    for tag, pin in locks.items():
        assert pin.startswith(tag + '@sha256:') and re.fullmatch(r'.+@sha256:[a-f0-9]{64}', pin)
    total = 0
    for slug in CATALOG:
        evidence = eligibility[slug]
        assert evidence['criterion'] == 'no_matching_public_listing_found'
        assert evidence['matchingListings'] == [] and len(evidence['queries']) >= 2
        excluded = {x['code'] for x in evidence.get('excludedMatches', [])}
        for q in evidence['queries']:
            assert not q['hasNextPage'] and q['resultCount'] == len(q['results'])
            assert re.fullmatch(r'[a-f0-9]{64}', q['receiptSha256'])
            assert all(x['code'] in excluded for x in q['results'])
        assert re.fullmatch(r'[a-f0-9]{40}', sources[slug]['sha'])
        assert sources[slug]['archived'] is False
        assert len(metadata[slug]['description']) <= 75
        config = json.loads((ROOT / 'templates' / slug / 'template.json').read_text())
        assert config == configuration(slug), slug + ': stale generated configuration'
        services = list(config['services'].values())
        by_name = {s['name']: s for s in services}
        assert len(by_name) == len(services)
        assert [s['name'] for s in services if s['networking']['serviceDomains']] == [slug]
        edge = by_name[slug]
        assert edge['variables']['OWNER_AUTH']['defaultValue'] == 'true'
        assert edge['variables']['ACCESS_PASSWORD']['defaultValue'].startswith('${{secret(')
        for s in services:
            total += 1
            assert not s['networking'].get('tcpProxies')
            src = s['source']
            if 'image' in src:
                assert src['image'] in locks.values()
            else:
                assert src == {'repo': 'orenaksakal/railway-templates', 'branch': BRANCH}
                dockerfile = ROOT / s['build']['dockerfilePath']
                assert dockerfile.exists()
                stages = set()
                for line in dockerfile.read_text().splitlines():
                    if line.startswith('FROM '):
                        parts = line.split()
                        assert re.search(r'@sha256:[a-f0-9]{64}$', parts[1]) or parts[1] in stages, (dockerfile, line)
                        if len(parts) >= 4 and parts[-2].lower() == 'as':
                            stages.add(parts[-1])
                    if line.startswith('COPY ') and '--from=' not in line:
                        paths = [x for x in line.split()[1:-1] if not x.startswith('--')]
                        for path in paths:
                            assert (ROOT / path).exists(), (dockerfile, path)
                assert s['variables']['RAILWAY_DOCKERFILE_PATH']['defaultValue'] == s['build']['dockerfilePath']
            mounts = list(s.get('volumeMounts', {}).values())
            assert len(mounts) <= 1
            if mounts:
                assert mounts[0]['mountPath'].startswith('/')
                assert s['deploy']['requiredMountPath'] == mounts[0]['mountPath']
            for key, variable in s['variables'].items():
                assert variable['description'] and isinstance(variable['isOptional'], bool)
                for target, field in re.findall(r'\$\{\{([\w-]+)\.([\w]+)\}\}', variable.get('defaultValue', '')):
                    assert target in by_name, (slug, key, target)
                    assert field in by_name[target]['variables'] or field in ['RAILWAY_PRIVATE_DOMAIN', 'RAILWAY_PUBLIC_DOMAIN']
                    if field == 'RAILWAY_PUBLIC_DOMAIN':
                        assert by_name[target]['networking']['serviceDomains']
        readme = (ROOT / 'templates' / slug / 'README.md').read_text()
        for required in ['marketplace gap', 'Validation scope: source review and static checks', 'First use', 'Recommended acceptance checks', 'Scope and limitations']:
            assert required in readme, (slug, required)
        for path in (ROOT / 'templates' / slug).glob('*.sh'):
            subprocess.run(['sh', '-n', str(path)], check=True)
    for path in (ROOT / 'scripts').glob('*round8*.py'):
        ast.parse(path.read_text())
    print(f'PASS: 20 eligible marketplace-gap templates / {total} services; 56 recorded name/alias checks.')
    print('PASS: source and image pins, deterministic configuration, private dependencies, gateway access, mounts, metadata, README and shell/Python syntax.')
    print('Not tested: image builds, Railway runtime, product workflows, persistence or recovery.')


if __name__ == '__main__':
    validate()
