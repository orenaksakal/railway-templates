"""Materialize native template variables into an isolated local Compose project."""
import argparse
import json
import os
from pathlib import Path
import re
import secrets
from catalog import ROOT, CATALOG as PUBLISHED_CATALOG
from catalog_round3 import CATALOG as DRAFT_CATALOG
CATALOG = {**PUBLISHED_CATALOG, **DRAFT_CATALOG}

parser = argparse.ArgumentParser()
parser.add_argument('template', choices=CATALOG)
parser.add_argument('--port', type=int, default=18080)
parser.add_argument('--input', action='append', default=[], metavar='SERVICE.KEY=VALUE', help='Supply a required operator input for a local test only')
args = parser.parse_args()
os.umask(0o077)
folder = ROOT / '.local' / args.template
folder.mkdir(parents=True, exist_ok=True)
config = json.loads((ROOT / 'templates' / args.template / 'template.json').read_text())
services = {s['name']: s for s in config['services'].values()}
secret_file = folder / 'secrets.json'
saved = json.loads(secret_file.read_text()) if secret_file.exists() else {}
resolved = {}
inputs = dict(value.split('=', 1) for value in args.input)
public_ports = {name: args.port + index for index, name in enumerate(s['name'] for s in services.values() if s['networking']['serviceDomains'])}
if public_ports and max(public_ports.values()) > 65535:
    raise SystemExit('Local port range exceeds 65535')

def resolve(owner, key, stack=()):
    ident = owner + '.' + key
    if ident in resolved:
        return resolved[ident]
    if ident in stack:
        raise ValueError(f'Circular reference: {ident}')
    if key == 'RAILWAY_PRIVATE_DOMAIN': return owner
    if key == 'RAILWAY_PUBLIC_DOMAIN': return f'localhost:{public_ports[owner]}'
    definition = services[owner]['variables'][key]
    if ident in inputs:
        value = inputs[ident]
    elif 'defaultValue' in definition:
        value = definition['defaultValue']
    else:
        raise SystemExit(f'Required local input: --input {ident}=VALUE')
    if value.startswith('${{secret('):
        match = re.fullmatch(r'\$\{\{secret\((\d+), "([^"]+)"\)\}\}', value)
        if not match:
            raise ValueError('Unsupported secret expression')
        length, alphabet = int(match[1]), match[2]
        value = saved.setdefault(ident, ''.join(secrets.choice(alphabet) for _ in range(length)))
        if len(value) != length:
            raise SystemExit(f'Existing local secret length differs for {ident}; use an isolated test directory or migrate it deliberately')
    else:
        def substitute(match):
            token = match.group(1).strip()
            target, variable = token.split('.', 1) if '.' in token else (owner, token)
            return resolve(target, variable, stack + (ident,))
        value = re.sub(r'\$\{\{(.*?)\}\}', substitute, value)
    for port in public_ports.values():
        value = value.replace(f'https://localhost:{port}', f'http://localhost:{port}')
    resolved[ident] = value
    return value

compose = {'name': 'rt-' + args.template, 'services': {}, 'volumes': {}}
for name, s in services.items():
    env = {k: resolve(name, k) for k in s['variables']}
    if args.template == 'openproject':
        env.update(OPENPROJECT_HTTPS='false', OPENPROJECT_HSTS='false')
    value = {'environment': env, 'restart': 'no', 'logging': {'driver': 'json-file', 'options': {'max-size': '5m', 'max-file': '2'}}}
    if 'repo' in s['source']:
        value['build'] = {'context': str(ROOT), 'dockerfile': s['build']['dockerfilePath']}
        value['image'] = f'railway-templates/{args.template}-{name}:test'
    else:
        value['image'] = s['source']['image']
    if args.template in ('tooljet', 'openproject', 'frappe-crm', 'frappe-helpdesk', 'ragflow'):
        value['platform'] = 'linux/amd64'
    if s['deploy'].get('startCommand'):
        value['command'] = s['deploy']['startCommand'].replace('$', '$$')
    for mount in s.get('volumeMounts', {}).values():
        key = name + '-data'
        compose['volumes'][key] = {}
        value.setdefault('volumes', []).append(key + ':' + mount['mountPath'])
    for domain in s['networking']['serviceDomains'].values():
        value['ports'] = [f'127.0.0.1:{public_ports[name]}:{domain["port"]}']
    compose['services'][name] = value
(folder / 'compose.json').write_text(json.dumps(compose, indent=2) + '\n')
secret_file.write_text(json.dumps(saved, indent=2) + '\n')
print(folder / 'compose.json')
