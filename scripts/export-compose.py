"""Export catalog defaults for the Railway template editor's Compose import.

No cloud actions; references and secret generators stay symbolic. Import behavior
must be checked against template.json before a draft is treated as complete.
"""
import json
from pathlib import Path
import shlex
from catalog import CATALOG, ROOT


def export(config):
    result = {'services': {}, 'volumes': {}}
    for service in config['services'].values():
        name = service['name']
        # Missing operator inputs must fail Compose interpolation rather than become empty credentials.
        environment = {k: v['defaultValue'] if 'defaultValue' in v else '${' + k + ':?Set ' + k + ' before starting this template}' for k, v in service['variables'].items()}
        entry = {'environment': environment, 'restart': 'on-failure:' + str(service['deploy'].get('restartPolicyMaxRetries', 5))}
        source = service['source']
        if source.get('image'):
            entry['image'] = source['image']
        else:
            entry['build'] = {'context': 'https://github.com/' + source['repo'] + '.git#' + source.get('branch', 'main'), 'dockerfile': service['build']['dockerfilePath']}
        if service['deploy'].get('startCommand'):
            entry['command'] = shlex.split(service['deploy']['startCommand'])
        ports = [v['port'] for v in service.get('networking', {}).get('serviceDomains', {}).values()]
        if ports:
            entry['ports'] = [f'{port}:{port}' for port in ports]
        for i, mount in enumerate(service.get('volumeMounts', {}).values()):
            volume = f'{name}-data-{i}'
            result['volumes'][volume] = {}
            entry.setdefault('volumes', []).append(f"{volume}:{mount['mountPath']}")
        result['services'][name] = entry
    return result


if __name__ == '__main__':
    output = ROOT / '.local' / 'imports'
    output.mkdir(parents=True, exist_ok=True)
    for name in CATALOG:
        config = json.loads((ROOT / 'templates' / name / 'template.json').read_text())
        path = output / f'{name}.compose.yaml'
        # JSON is a YAML subset and needs no third-party YAML package.
        path.write_text(json.dumps(export(config), indent=2) + '\n')
        print(path)
