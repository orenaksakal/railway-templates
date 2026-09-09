"""Bounded static checks for the unpublished round-four catalog."""
import ast, json, re, subprocess
from pathlib import Path
from catalog_round4 import ROOT,CATALOG
errors=[];count=0
for name,factory in CATALOG.items():
 p=ROOT/'templates'/name
 config=json.loads((p/'template.json').read_text());services=list(config['services'].values());byname={s['name']:s for s in services}
 assert len(byname)==len(services),name
 for service in services:
  count+=1;label=name+'/'+service['name'];source=service['source']
  if 'image' in source:assert re.search(r'@sha256:[0-9a-f]{64}$',source['image']),label
  else:
   assert source['repo']=='orenaksakal/railway-templates'
   docker=ROOT/service['build']['dockerfilePath'];assert docker.is_file(),str(docker)
   for line in docker.read_text().splitlines():
    if line.startswith('FROM '):assert '@sha256:' in line,(docker,line)
    if line.startswith('COPY ') and '--from=' not in line:
     paths=line.split();paths=[x for x in paths[1:-1] if not x.startswith('--')]
     for x in paths:assert (ROOT/x).exists(),(docker,x)
  assert len(service.get('volumeMounts',{}))<=1,label
  for k,v in service['variables'].items():
   assert v.get('description'),(label,k)
   val=v.get('defaultValue','')
   assert 'host.docker.internal' not in val,(label,k)
   for other,key in re.findall(r'\$\{\{([\w-]+)\.([\w]+)\}\}',val):
    assert other in byname,(label,k,other)
    assert key in byname[other]['variables'] or key in ('RAILWAY_PRIVATE_DOMAIN','RAILWAY_PUBLIC_DOMAIN'),(label,k,other,key)
    if key=='RAILWAY_PUBLIC_DOMAIN':assert byname[other]['networking']['serviceDomains'],(label,k,other)
  assert not service['networking'].get('tcpProxies'),label
 assert '### Deployment Dependencies' in (p/'README.md').read_text()
 assert any(x in (p/'README.md').read_text() for x in ['Release gates','Recommended acceptance checks'])
 for f in p.glob('*.sh'):subprocess.run(['bash','-n',str(f)],check=True)
 for f in p.glob('*.py'):ast.parse(f.read_text())
for f in (ROOT/'shared').glob('round4-*/*.sh'):subprocess.run(['sh','-n',str(f)],check=True)
print(f'PASS: {len(CATALOG)} drafts, {count} services; pins, references, sources, descriptions, volumes and script syntax')

for metadata in json.loads((ROOT/"marketplace.round4.json").read_text()).values():
    assert len(metadata["description"]) <= 75
    assert metadata["category"] in {"AI/ML","Analytics","Authentication","Automation","Blogs","Bots","CMS","Observability","Other","Starters","Storage","Queues"}

for name in CATALOG:
    readme=(ROOT/"templates"/name/"README.md").read_text()
    for heading in ["# Deploy and Host", "## About Hosting", "## Why Deploy", "## Common Use Cases", "## Dependencies for"]:
        assert heading in readme, (name,heading)
