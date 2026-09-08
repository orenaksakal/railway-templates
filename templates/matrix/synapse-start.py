import os,subprocess
from pathlib import Path
import yaml
os.umask(0o077)
p=Path('/data/homeserver.yaml')
if not p.exists():subprocess.run(['python','/start.py','generate'],check=True)
c=yaml.safe_load(p.read_text())
if c['server_name']!=os.environ['SYNAPSE_SERVER_NAME']:raise SystemExit('Server name is immutable; restore the original server name')
c.update(public_baseurl=os.environ['PUBLIC_URL'].rstrip('/')+'/',enable_registration=False,report_stats=False)
c['database']={'name':'psycopg2','args':{'user':os.environ['DB_USER'],'password':os.environ['DB_PASSWORD'],'host':os.environ['DB_HOST'],'port':5432,'database':'synapse','cp_min':2,'cp_max':5}}
c['listeners']=[{'port':8008,'tls':False,'type':'http','x_forwarded':True,'bind_addresses':['::','0.0.0.0'],'resources':[{'names':['client','federation'],'compress':False}]}]
c['matrix_authentication_service']={'enabled':True,'endpoint':os.environ['MAS_URL'],'secret':os.environ['MATRIX_SHARED_SECRET']}
t=p.with_suffix('.tmp');t.write_text(yaml.safe_dump(c));t.replace(p)
os.execvp('python',['python','/start.py','run'])
