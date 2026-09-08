"""Static publication checks for the ten unpublished draft templates."""
import ast,json,re,subprocess,sys
from pathlib import Path
from catalog_round3 import ROOT,CATALOG,BRANCH
ALLOWED_PUBLIC={'dbos':{'dbos'},'spicedb':{'spicedb'},'frappe-crm':{'frappe-crm'},'frappe-helpdesk':{'frappe-helpdesk'},'immich':{'immich'},'matrix':{'matrix','mas','element'},'novu':{'api','ws','novu'},'appflowy':{'storage','appflowy'},'appwrite':{'appwrite'},'ragflow':{'ragflow'}}
for app in CATALOG:
    config=json.loads((ROOT/'templates'/app/'template.json').read_text());services={s['name']:s for s in config['services'].values()}
    for name,s in services.items():
        assert s['source'].get('image') or s['source'].get('repo'),(app,name,'missing source')
        if 'image' in s['source']:assert re.search(r'@sha256:[a-f0-9]{64}$',s['source']['image']),(app,name,'image not pinned')
        else:
            assert s['source']['branch']==BRANCH
            path=s['variables']['RAILWAY_DOCKERFILE_PATH']['defaultValue'];assert s['build']['dockerfilePath']==path
            assert (ROOT/path).is_file(),path
        domains=s['networking']['serviceDomains']
        assert bool(domains)==(name in ALLOWED_PUBLIC[app]),(app,name,'exposure changed')
        assert not s['networking'].get('tcpProxies')
        mounts=s.get('volumeMounts',{})
        assert len(mounts)<=1,(app,name,'Railway volume topology')
        if mounts:assert s['deploy']['requiredMountPath']==next(iter(mounts.values()))['mountPath']
        for key,var in s['variables'].items():
            assert len(var.get('description','').strip())>=15,(app,name,key,'missing explanation')
            value=var.get('defaultValue','')
            assert not re.search(r'\$\{(?!\{)',value),(app,name,key,'Compose variable left over')
            for token in re.findall(r'\$\{\{(.*?)\}\}',value):
                if token.startswith('secret('):assert re.fullmatch(r'secret\(\d+, "abcdef0123456789"\)',token);continue
                target,variable=token.split('.',1)
                assert target in services,(app,name,key,'unknown target')
                assert variable in services[target]['variables'] or variable in ('RAILWAY_PRIVATE_DOMAIN','RAILWAY_PUBLIC_DOMAIN'),(app,name,key,'unknown variable')
                if variable=='RAILWAY_PUBLIC_DOMAIN':assert services[target]['networking']['serviceDomains'],(app,target,'reference needs a public domain')
    print(app,len(services),'services: pins, references, variable descriptions, exposure, and volumes pass')
for app in CATALOG:
    for p in (ROOT/'templates'/app).rglob('*'):
        if not p.is_file():continue
        if p.suffix=='.py':ast.parse(p.read_text(),filename=str(p))
        elif p.suffix=='.sh':subprocess.run(['sh','-n',str(p)],check=True)
        elif p.suffix in ('.mjs','.cjs'):subprocess.run(['node','--check',str(p)],check=True)
        elif p.name.endswith('Dockerfile'):
            for image in re.findall(r'^FROM ([^\s]+)',p.read_text(),re.M):assert '@sha256:' in image,(p,'unlocked base')
print('Adapter syntax passed; these checks do not execute Docker builds or application workflows.')
