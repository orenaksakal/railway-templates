"""Initialize only an empty user database, then supervise web and task worker."""
import os
import signal
import subprocess
import time
from gramps_webapi.app import create_app
from gramps_webapi.auth import User, user_db, add_user
from gramps_webapi.const import ROLE_OWNER

app = create_app()
with app.app_context():
    if user_db.session.query(User).first() is None:
        add_user("owner", os.environ["OWNER_PASSWORD"], "Owner", os.environ["OWNER_EMAIL"], ROLE_OWNER)

children = []
def stop(signum=None, frame=None):
    for child in children:
        if child.poll() is None:
            child.terminate()
    for child in children:
        try:
            child.wait(timeout=20)
        except subprocess.TimeoutExpired:
            child.kill()
            child.wait()

signal.signal(signal.SIGTERM, lambda s, f: (stop(), exit(0)))
signal.signal(signal.SIGINT, lambda s, f: (stop(), exit(0)))
try:
    children.append(subprocess.Popen(["celery", "-A", "gramps_webapi.celery", "worker", "--loglevel=INFO", "--concurrency=1"]))
    children.append(subprocess.Popen(["gunicorn", "-w", os.environ.get("GUNICORN_NUM_WORKERS", "2"), "-b", "0.0.0.0:5000", "gramps_webapi.wsgi:app", "--timeout", "120", "--limit-request-line", "8190"]))
    while all(child.poll() is None for child in children):
        time.sleep(1)
    raise SystemExit(1)
finally:
    stop()
