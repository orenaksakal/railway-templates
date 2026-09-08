"""Keep API and workers on one volume; Railway volumes cannot be shared."""
import os,signal,subprocess,time
from pathlib import Path
os.chdir('/usr/src/code')
marker=Path('/storage/.railway-release')
if marker.exists() and marker.read_text()!='2.0.0':
    if os.environ.get('ALLOW_MIGRATION')!='true':raise SystemExit('Back up all stores before enabling ALLOW_MIGRATION for this upgrade')
    subprocess.run(['migrate'],check=True)
marker.write_text('2.0.0')
commands=[['php','app/http.php'],['worker'],['schedule'],['maintenance'],['interval']]
children=[];stopping=False;status=0

def stop(*_):
    global stopping
    stopping=True
for sig in [signal.SIGTERM,signal.SIGINT]:signal.signal(sig,stop)
try:
    for command in commands:
        # The combined worker needs one pool slot per queue coroutine (upstream: 78).
        # Keep that budget local to the worker process, not the HTTP server.
        child_env=dict(os.environ)
        if command==['worker']:child_env['_APP_WORKER_MAX_COROUTINES']=os.environ.get('APPWRITE_WORKER_POOL_SIZE','78')
        children.append(subprocess.Popen(command,start_new_session=True,env=child_env))
    while not stopping:
        for p in children:
            if p.poll() is not None:status=1;stopping=True;print('Required Appwrite process exited',flush=True);break
        time.sleep(.5)
finally:
    for p in children:
        if p.poll() is None:os.killpg(p.pid,signal.SIGTERM)
    deadline=time.monotonic()+25
    for p in children:
        try:p.wait(timeout=max(.1,deadline-time.monotonic()))
        except subprocess.TimeoutExpired:os.killpg(p.pid,signal.SIGKILL);p.wait()
raise SystemExit(status)
