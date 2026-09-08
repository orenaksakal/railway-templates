"""Create unpublished Railway templates through the authenticated CLI public API.

No deployment or publication mutation is invoked. Never prints variable values.
"""
import argparse
import json
import os
from pathlib import Path
import subprocess
from catalog import ROOT, CATALOG

def api(document, variables):
    result = subprocess.run(['railway', 'api', document, '--variables', json.dumps(variables), '--compact'],
                            text=True, capture_output=True, check=True)
    response = json.loads(result.stdout)
    if response.get('errors'):
        raise RuntimeError(json.dumps(response['errors']))
    return response['data']

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--workspace', required=True)
    parser.add_argument('--template', choices=CATALOG)
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
        if receipt.get('templateId'):
            print(name, 'draft already created:', receipt['templateId'])
            continue
        if not receipt.get('projectId'):
            project = api('mutation($input: ProjectCreateInput!) { projectCreate(input:$input) { id environments { edges { node { id name } } } } }',
                          {'input': {'name': 'template-' + name, 'workspaceId': args.workspace, 'isPublic': False, 'description': 'Unpublished template source; no deployments requested.'}})['projectCreate']
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
            if not state.get('configured'):
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
        receipt.update(templateId=template['id'], templateCode=template['code'], status=template['status'])
        save()
        (ROOT / '.local' / f'{name}-railway-draft.json').write_text(json.dumps(template, indent=2) + '\n')
        print(name, template['status'], template['id'])

if __name__ == '__main__':
    main()
