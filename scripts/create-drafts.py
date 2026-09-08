"""Create unpublished Railway templates through the authenticated CLI public API.

Source connection and volume creation can start billable deployments.
Templates remain unpublished. Never prints variable values.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
from catalog import ROOT, CATALOG

def api(document, variables):
    result = subprocess.run(['railway', 'api', document, '--variables', json.dumps(variables), '--compact'],
                            text=True, capture_output=True)
    if result.returncode:
        # CLI errors can echo variables, including credentials. Never include args/output.
        raise RuntimeError(f"Railway API request failed (exit {result.returncode}); configuration values suppressed")
    response = json.loads(result.stdout)
    if response.get('errors'):
        raise RuntimeError('Railway API returned GraphQL errors; configuration values suppressed')
    return response['data']

def verify_draft(expected, template):
    actual = template['serializedConfig']
    actual = json.loads(actual) if isinstance(actual, str) else actual
    expected_services = {s['name']: s for s in expected['services'].values()}
    actual_services = {s['name']: s for s in actual['services'].values()}
    assert actual_services.keys() == expected_services.keys(), 'Draft service set differs'
    for name, source in expected_services.items():
        target = actual_services[name]
        for key, value in source['variables'].items():
            assert target.get('variables', {}).get(key, {}).get('defaultValue') == value['defaultValue'], f'{name}: variable {key} changed during generation'
        for key in ('image', 'repo'):
            if key in source['source']:
                assert target['source'].get(key, '').removeprefix('https://github.com/') == source['source'][key], f'{name}: source changed'
        paths = lambda s: sorted(v['mountPath'] for v in s.get('volumeMounts', {}).values())
        assert paths(source) == paths(target), f'{name}: volume mounts changed'
        domains = lambda s: sorted(v['port'] for v in s.get('networking', {}).get('serviceDomains', {}).values())
        assert domains(source) == domains(target), f'{name}: public ports changed'
        assert not target.get('networking', {}).get('tcpProxies'), f'{name}: unexpected public TCP proxy'
        for key in ('healthcheckPath', 'startCommand', 'restartPolicyType', 'restartPolicyMaxRetries'):
            assert source['deploy'].get(key) == target.get('deploy', {}).get(key), f'{name}: {key} changed'

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--workspace', required=True)
    parser.add_argument('--template', choices=CATALOG)
    parser.add_argument('--stage-only', action='store_true', help='Create drafts requiring editor repair; do not claim validation')
    parser.add_argument('--verify-only', action='store_true', help='Read and verify existing drafts without cloud mutations')
    args = parser.parse_args()
    os.umask(0o077)
    receipt_path = ROOT / '.local' / 'drafts.json'
    receipt_path.parent.mkdir(exist_ok=True)
    receipts = json.loads(receipt_path.read_text()) if receipt_path.exists() else {}
    def save():
        temp = receipt_path.with_suffix('.tmp')
        temp.write_text(json.dumps(receipts, indent=2) + '\n')
        temp.replace(receipt_path)
    names = [args.template] if args.template else list(CATALOG)
    for name in names:
        config = json.loads((ROOT / 'templates' / name / 'template.json').read_text())
        receipt = receipts.setdefault(name, {'workspaceId': args.workspace, 'services': {}})
        if receipt['workspaceId'] != args.workspace:
            raise SystemExit(f'{name}: receipt belongs to another workspace')
        fingerprint = hashlib.sha256(json.dumps(config, sort_keys=True).encode()).hexdigest()
        if args.verify_only or (receipt.get('templateId') and receipt.get('configHash') == fingerprint):
            if not receipt.get('templateId'):
                raise SystemExit(f'{name}: no draft exists')
            template = api('query($id:String!) { template(id:$id) { id code status name serializedConfig } }',
                           {'id': receipt['templateId']})['template']
            (ROOT / '.local' / f'{name}-railway-draft.json').write_text(json.dumps(template, indent=2) + '\n')
            try:
                verify_draft(config, template)
            except AssertionError as error:
                receipt['verified'] = False
                save()
                if not args.stage_only:
                    raise SystemExit(f'{name}: draft needs editor repair: {error}') from None
                print(name, 'UNVERIFIED: editor repair required')
            else:
                receipt['verified'] = True
                save()
                print(name, 'configuration verified:', receipt['templateId'])
            continue
        if not receipt.get('projectId'):
            project = api('mutation($input: ProjectCreateInput!) { projectCreate(input:$input) { id environments { edges { node { id name } } } } }',
                          {'input': {'name': 'template-' + name, 'workspaceId': args.workspace, 'isPublic': False, 'description': 'Unpublished template source and deployment validation project.'}})['projectCreate']
            receipt['projectId'] = project['id']
            receipt['environmentId'] = project['environments']['edges'][0]['node']['id']
            save()
        project_id, environment_id = receipt['projectId'], receipt['environmentId']
        # All services exist before references are added.
        for service in config['services'].values():
            sname = service['name']
            if sname not in receipt['services']:
                created = api('mutation($input: ServiceCreateInput!) { serviceCreate(input:$input) { id } }',
                              {'input': {'projectId': project_id, 'name': sname}})['serviceCreate']
                receipt['services'][sname] = {'id': created['id']}
                save()
        for service in config['services'].values():
            sname = service['name']
            state = receipt['services'][sname]
            service_id = state['id']
            if not state.get('configured') or receipt.get('configHash') != fingerprint:
                variables = {k: v.get('defaultValue', '') for k, v in service['variables'].items()}
                api('mutation($input: VariableCollectionUpsertInput!) { variableCollectionUpsert(input:$input) }',
                    {'input': {'projectId': project_id, 'environmentId': environment_id, 'serviceId': service_id,
                               'variables': variables, 'replace': True, 'skipDeploys': True}})
                settings = {k: v for k, v in service['deploy'].items() if k != 'requiredMountPath'}
                settings.update(service.get('build', {}))
                settings['source'] = {k: v for k, v in service['source'].items() if k in ('image', 'repo')}
                api('mutation($serviceId:String!, $environmentId:String!, $input:ServiceInstanceUpdateInput!) { serviceInstanceUpdate(serviceId:$serviceId, environmentId:$environmentId, input:$input) }',
                    {'serviceId': service_id, 'environmentId': environment_id, 'input': settings})
                state['configured'] = True
                save()
            if not state.get('connected'):
                api('mutation($id:String!, $input:ServiceConnectInput!) { serviceConnect(id:$id, input:$input) { id } }',
                    {'id': service_id, 'input': service['source']})
                state['connected'] = True
                save()
            if service.get('volumeMounts') and not state.get('volumeId'):
                mount = next(iter(service['volumeMounts'].values()))['mountPath']
                volume = api('mutation($input:VolumeCreateInput!) { volumeCreate(input:$input) { id } }',
                    {'input': {'projectId': project_id, 'environmentId': environment_id, 'serviceId': service_id, 'mountPath': mount}})['volumeCreate']
                state['volumeId'] = volume['id']
                save()
            if service['networking']['serviceDomains'] and not state.get('domain'):
                domain = next(iter(service['networking']['serviceDomains'].values()))
                created = api('mutation($input:ServiceDomainCreateInput!) { serviceDomainCreate(input:$input) { domain } }',
                    {'input': {'environmentId': environment_id, 'serviceId': service_id, 'targetPort': domain['port']}})['serviceDomainCreate']
                state['domain'] = created['domain']
                save()
        template = api('mutation($input:TemplateGenerateInput!) { templateGenerate(input:$input) { id code status name serializedConfig } }',
                       {'input': {'projectId': project_id, 'environmentId': environment_id}})['templateGenerate']
        if receipt.get('templateId'):
            receipt.setdefault('supersededTemplateIds', []).append(receipt['templateId'])
        receipt.update(templateId=template['id'], templateCode=template['code'], status=template['status'], configHash=fingerprint)
        save()
        (ROOT / '.local' / f'{name}-railway-draft.json').write_text(json.dumps(template, indent=2) + '\n')
        try:
            verify_draft(config, template)
        except AssertionError as error:
            receipt['verified'] = False
            save()
            if not args.stage_only:
                raise SystemExit(f'{name}: draft needs editor repair: {error}') from None
            print(name, template['status'], template['id'], 'UNVERIFIED: editor repair required')
        else:
            receipt['verified'] = True
            save()
            print(name, template['status'], template['id'], 'configuration verified')

if __name__ == '__main__':
    main()
