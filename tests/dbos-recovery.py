"""Opt-in DBOS recovery test using a cached PostgreSQL image and tmpfs data."""
import hashlib,json,os,secrets,shutil,socket,subprocess,time,urllib.request,urllib.error
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];scratch=ROOT/'.local/dbos-runtime';scratch.mkdir(exist_ok=True)
if not (scratch/'node_modules/@dbos-inc/dbos-sdk').exists():raise SystemExit('Install the locked DBOS package in .local/dbos-runtime first')
shutil.copy2(ROOT/'templates/dbos/server.mjs',scratch/'server.mjs')
shutil.copy2(ROOT/'shared/wait-for-dependencies.mjs',scratch/'wait-for-dependencies.mjs')
password=secrets.token_hex(32);key=secrets.token_hex(32)
envfile=scratch/'postgres.env';envfile.write_text(f'POSTGRES_USER=postgres\nPOSTGRES_PASSWORD={password}\nAPP_USER=dbos\nAPP_PASSWORD={password}\nAPP_DB=dbos\n');envfile.chmod(0o600)
name='rt-round3-dbos-recovery';node=None;container=None;log=(scratch/'runtime.log').open('w')
def docker(*args):return subprocess.check_output(['docker',*args],text=True,stderr=subprocess.DEVNULL).strip()
def call(path,body=None,auth=True):
 headers={'Authorization':'Bearer '+key} if auth else {}
 if body is not None:headers.update({'Content-Type':'application/json','Idempotency-Key':'recovery-check'})
 req=urllib.request.Request(base+path,data=json.dumps(body).encode() if body is not None else None,headers=headers)
 try:
  with urllib.request.urlopen(req,timeout=3) as r:return r.status,json.load(r)
 except urllib.error.HTTPError as e:return e.code,json.load(e)
def start():return subprocess.Popen(['node','server.mjs'],cwd=scratch,env=env,stdout=log,stderr=log)
def ready():
 for _ in range(100):
  if node.poll() is not None:raise RuntimeError('DBOS exited; see private runtime log')
  try:
   if call('/healthz')[0]==200:return
  except OSError:pass
  time.sleep(.2)
 raise RuntimeError('DBOS readiness timed out')
try:
 container=docker('run','-d','--pull=never','--name',name,'--tmpfs','/var/lib/postgresql/data','--env-file',str(envfile),'-p','127.0.0.1::5432','railway-templates/openproject-postgres:test')
 port=int(docker('port',container,'5432/tcp').rsplit(':',1)[1])
 for _ in range(100):
  if subprocess.run(['docker','exec',container,'pg_isready','-h','127.0.0.1','-U','postgres','-d','dbos'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL).returncode==0:break
  time.sleep(.2)
 with socket.socket() as sock:sock.bind(('127.0.0.1',0));webport=sock.getsockname()[1]
 env={**os.environ,'DATABASE_URL':f'postgresql://dbos:{password}@127.0.0.1:{port}/dbos','API_KEY':key,'HOST':'127.0.0.1','PORT':str(webport)};base=f'http://127.0.0.1:{webport}'
 node=start();ready();assert call('/events',{},False)[0]==401;print('Authentication rejection passed',flush=True)
 body={'event':{'action':'restore-check'},'delaySeconds':6};status,event=call('/events',body);assert status==202
 status,same=call('/events',body);assert status==202 and event['workflowID']==same['workflowID'];print('Durable event acceptance and idempotent replay passed',flush=True)
 node.kill();node.wait();node=start();ready()
 for _ in range(120):
  status,result=call(event['statusUrl'])
  if status==200 and result['status']=='SUCCESS':break
  time.sleep(.25)
 else:raise RuntimeError('Workflow did not recover after process termination')
 expected=hashlib.sha256(json.dumps(body['event'],separators=(',',':')).encode()).hexdigest()
 assert result['result']['digest']==expected and result['result']['event']==body['event'];print('Interrupted workflow recovered and returned the correct result',flush=True)
finally:
 if node and node.poll() is None:node.terminate();node.wait(timeout=15)
 if container:subprocess.run(['docker','rm','-f',container],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
 log.close();envfile.unlink(missing_ok=True)
