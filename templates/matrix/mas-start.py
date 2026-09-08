import os,subprocess,tempfile
from pathlib import Path
import yaml
os.umask(0o077)
p=Path('/data/config.yaml');p.parent.mkdir(exist_ok=True)
if p.exists():c=yaml.safe_load(p.read_text())
else:c=yaml.safe_load(subprocess.check_output(['mas-cli','config','generate'],text=True))
c['database']={'uri':os.environ['DATABASE_URL']}
c['http']['public_base']=os.environ['PUBLIC_URL'].rstrip('/')+'/'
c['http']['issuer']=c['http']['public_base']
c['http']['listeners']=[{'name':'web','resources':[{'name':n} for n in ['discovery','human','oauth','compat','graphql']]+[{'name':'assets','path':'/usr/local/share/mas-cli/assets/'}],'binds':[{'address':'[::]:8080'}]}]
c['matrix']={'kind':'synapse','homeserver':os.environ['SERVER_NAME'],'endpoint':os.environ['SYNAPSE_URL'],'secret':os.environ['MATRIX_SHARED_SECRET']}
c.setdefault('account',{}).update(password_registration_enabled=os.environ.get('REGISTRATION_ENABLED')=='true',password_registration_email_required=False)
# Signing and encryption keys generated above stay in the persistent volume.
t=p.with_suffix('.tmp');t.write_text(yaml.safe_dump(c));t.replace(p)
subprocess.run(['mas-cli','config','check'],check=True)
os.execvp('mas-cli',['mas-cli','server'])
