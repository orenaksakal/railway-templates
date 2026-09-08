"""Create/update the ten UNPUBLISHED drafts without projects or deployments.

Uses the Railway editor's template-only API with the existing CLI session.
Receipts and read-back evidence stay in ignored .local/. No publish operation exists.
"""
import argparse,hashlib,json,os,subprocess,urllib.request,urllib.error
from pathlib import Path
from catalog_round3 import ROOT,CATALOG
READ='query($id:String!){template(id:$id){id code name status category description image readme serializedConfig}}'
def api(query,variables):
    user=json.loads((Path.home()/'.railway/config.json').read_text())['user']
    request=urllib.request.Request('https://backboard.railway.com/graphql/internal',data=json.dumps({'query':query,'variables':variables}).encode(),headers={'Authorization':'Bearer '+user['accessToken'],'Content-Type':'application/json','User-Agent':'Railway CLI'})
    try:
        with urllib.request.urlopen(request,timeout=60) as response:result=json.load(response)
    except urllib.error.HTTPError as error:raise RuntimeError(f'Railway returned HTTP {error.code}; request contents suppressed') from None
    if result.get('errors'):raise RuntimeError('; '.join(e.get('message','GraphQL error') for e in result['errors']))
    return result['data']
def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--workspace',required=True);parser.add_argument('--verify-only',action='store_true');parser.add_argument('--template',choices=CATALOG);args=parser.parse_args();workspace=args.workspace
    os.umask(0o077)
    # This read also refreshes an expired CLI access token through the normal login flow.
    subprocess.run(['railway','api','query { __typename }','--compact'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,check=True)
    root=ROOT/'.local/round3';root.mkdir(parents=True,exist_ok=True);path=root/'drafts.json';receipts=json.loads(path.read_text()) if path.exists() else {}
    def save():
        temporary=path.with_suffix('.tmp');temporary.write_text(json.dumps(receipts,indent=2)+'\n');temporary.replace(path)
    metadata=json.loads((ROOT/'marketplace.round3.json').read_text())
    for name in ([args.template] if args.template else CATALOG):
        config=json.loads((ROOT/'templates'/name/'template.json').read_text());meta={**metadata[name],'readme':(ROOT/'templates'/name/'README.md').read_text()}
        if name not in receipts:
            if args.verify_only:raise RuntimeError(name+': draft does not exist')
            created=api('mutation($input:TemplateCreateV2Input!){templateCreateV2(input:$input){id code status}}',{'input':{'metadata':meta,'serializedConfig':config,'workspaceId':workspace}})['templateCreateV2']
            receipts[name]={'templateId':created['id'],'workspaceId':workspace,'verified':False};save()
        receipt=receipts[name]
        if receipt['workspaceId']!=workspace:raise RuntimeError('Workspace mismatch')
        live=api(READ,{'id':receipt['templateId']})['template']
        if live['status']!='UNPUBLISHED':raise RuntimeError(name+': refusing to modify a published template')
        actual=live['serializedConfig'];actual=json.loads(actual) if isinstance(actual,str) else actual
        if actual!=config or any(live.get(k)!=v for k,v in meta.items()):
            if args.verify_only:raise RuntimeError(name+': draft differs from local source')
            patch=json.loads(json.dumps(config))
            for sid in actual.get('services',{}):
                if sid not in patch['services']:patch['services'][sid]=None
            staged=api('mutation($templateId:String!,$patch:TemplatePatch!,$merge:Boolean){templateChangeSetStage(templateId:$templateId,patch:$patch,merge:$merge){id status}}',{'templateId':receipt['templateId'],'patch':{'config':patch,'metadata':meta},'merge':False})['templateChangeSetStage']
            applied=api('mutation($changeSetId:String!){templateChangeSetApply(changeSetId:$changeSetId){id status}}',{'changeSetId':staged['id']})['templateChangeSetApply']
            if applied['status']!='APPLIED':raise RuntimeError(name+': changes not applied')
            live=api(READ,{'id':receipt['templateId']})['template'];actual=live['serializedConfig'];actual=json.loads(actual) if isinstance(actual,str) else actual
        if live['status']!='UNPUBLISHED' or actual!=config or any(live.get(k)!=v for k,v in meta.items()):raise RuntimeError(name+': saved configuration or metadata did not match')
        (root/(name+'-readback.json')).write_text(json.dumps(live,indent=2)+'\n')
        receipt.update(name=live['name'],templateCode=live['code'],status=live['status'],verified=True,serviceCount=len(config['services']),configHash=hashlib.sha256(json.dumps(config,sort_keys=True).encode()).hexdigest(),url='https://railway.com/workspace/templates/'+live['id'])
        save();print(name,live['status'],'configuration and metadata verified',receipt['url'],flush=True)
if __name__=='__main__':main()
