"""Gate workers on migrations; keep the API's store signing key on its volume."""
import os
import asyncio
from pathlib import Path
import subprocess
import time
import urllib.request

COMMANDS={
 'api':['gunicorn','entrypoints.routers:app','--bind','0.0.0.0:8000','--worker-class','uvicorn.workers.UvicornWorker','--workers','2','--timeout','60','--access-logfile','-','--error-logfile','-'],
 'services':['gunicorn','entrypoints.main:app','--bind','0.0.0.0:8080','--worker-class','uvicorn.workers.UvicornWorker','--workers','2','--timeout','60','--access-logfile','-','--error-logfile','-'],
 'worker-streams':['python','-m','entrypoints.worker_streams'],
 'worker-queues':['python','-m','entrypoints.worker_queues'],
 'cron':['/usr/local/bin/supercronic','/app/crontab'],
}
role=os.environ['START_ROLE']
command=COMMANDS[role]
if os.geteuid()==0:
 data=Path('/data')
 data.mkdir(parents=True,exist_ok=True)
 os.chown(data,10001,10001)
 os.setgroups([])
 os.setgid(10001)
 os.setuid(10001)
if role=='api':
 os.umask(0o077)
 key=Path('/data/store-private.pem')
 key.parent.mkdir(parents=True,exist_ok=True)
 if not key.exists():
  temp=key.with_suffix('.tmp')
  subprocess.run(['openssl','genpkey','-algorithm','RSA','-pkeyopt','rsa_keygen_bits:2048','-out',str(temp)],check=True,stderr=subprocess.DEVNULL)
  temp.replace(key)
 os.environ['AGENTA_STORE_JWT_PRIVATE_KEY']=key.read_text()
 async def wait_databases():
  import asyncpg
  for _ in range(180):
   try:
    for name in ('POSTGRES_URI_CORE','POSTGRES_URI_TRACING','POSTGRES_URI_SUPERTOKENS'):
     uri=os.environ[name].replace('postgresql+asyncpg://','postgresql://')
     connection=await asyncpg.connect(uri,timeout=3)
     try:await connection.fetchval('SELECT 1')
     finally:await connection.close()
    return
   except (OSError,asyncio.TimeoutError,asyncpg.PostgresError):
    await asyncio.sleep(2)
  raise SystemExit('Database initialization timed out')
 asyncio.run(wait_databases())
 # The module applies both core and tracing migrations. A failure never opens HTTP.
 subprocess.run(['/opt/venv/bin/python','-m','oss.databases.postgres.migrations.runner'],check=True)
else:
 for _ in range(300):
  try:
   with urllib.request.urlopen(os.environ['API_HEALTH_URL'],timeout=3) as r:
    if r.status==200:break
  except OSError:pass
  time.sleep(2)
 else:raise SystemExit('API migrations/startup did not become ready')
os.execvp(command[0],command)
