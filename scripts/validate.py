"""Fail on unsafe or incomplete template wiring; no cloud mutations."""
import json
from pathlib import Path
import re
import subprocess
from catalog import ROOT, CATALOG

for name in CATALOG:
    path = ROOT / 'templates' / name / 'template.json'
    config = json.loads(path.read_text())
    services = {s['name']: s for s in config['services'].values()}
    public = []
    for service, value in services.items():
        assert value['source'].get('image') or value['source'].get('repo'), (name, service, 'missing source')
        if 'repo' in value['source']:
            assert value['variables']['RAILWAY_DOCKERFILE_PATH']['defaultValue'] == value['build']['dockerfilePath'], (name, service, 'Dockerfile path must survive template generation')
            assert value['build'].get('builder') in ('RAILPACK', 'NIXPACKS', 'HEROKU', 'PAKETO'), (name, service, 'unsupported Railway builder')
            assert (ROOT / value['build']['dockerfilePath']).is_file(), (name, service, 'missing Dockerfile')
        domains = value['networking']['serviceDomains']
        if domains:
            public.append(service)
            assert value['deploy'].get('healthcheckPath'), (name, service, 'no healthcheck')
        assert not value['networking'].get('tcpProxies'), (name, service, 'public dependency port')
        assert len(value.get('volumeMounts', {})) <= 1, (name, service, 'Railway permits one volume per service')
        for variable, specification in value['variables'].items():
            default = specification.get('defaultValue', '')
            for token in re.findall(r'\$\{\{(.*?)\}\}', default):
                token = token.strip()
                if token.startswith('secret('):
                    assert re.fullmatch(r'secret\(64, "abcdef0123456789"\)', token), token
                    continue
                owner, key = token.split('.', 1) if '.' in token else (service, token)
                assert owner in services, (name, service, variable, 'unknown service', owner)
                assert key.startswith('RAILWAY_') or key in services[owner]['variables'], (name, service, variable, 'unknown variable', key)
            assert 'changeme' not in default.lower() and 'replace_me' not in default.lower()
    assert public == [name], (name, 'only the application should be public', public)
    if name == 'firecrawl':
        assert not services['api']['networking']['serviceDomains']
        assert services['firecrawl']['variables']['API_KEY']['defaultValue'].startswith('${{secret(')
    print(f'{name}: {len(services)} services, references and exposure validated')
for script in list((ROOT / 'templates').rglob('*.sh')) + list((ROOT / 'shared').rglob('*.sh')):
    subprocess.run(['bash', '-n', str(script)], check=True)
for script in list((ROOT / 'templates').rglob('*.mjs')) + list((ROOT / 'shared').rglob('*.mjs')):
    subprocess.run(['node', '--check', str(script)], check=True)
print('Shell and JavaScript syntax validated')
