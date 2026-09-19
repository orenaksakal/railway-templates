"""Initialize an empty volume without printing keys or resetting existing users."""
import os
from pathlib import Path
import shutil
import subprocess
import sys

for key in ('PUBLIC_URL', 'PINRY_SECRET_KEY', 'ADMIN_USERNAME', 'ADMIN_PASSWORD', 'ADMIN_EMAIL'):
    if not os.environ.get(key):
        raise SystemExit('Required variable ' + key + ' is missing')
if len(os.environ['PINRY_SECRET_KEY']) < 32:
    raise SystemExit('PINRY_SECRET_KEY must be at least 32 characters')

Path('/data').mkdir(exist_ok=True)
settings = Path('/data/local_settings.py')
if not settings.exists():
    # Using x mode ensures an existing operator-managed configuration is retained.
    with settings.open('x') as dest:
        dest.write(Path('/usr/local/share/railway-pinry-settings.py').read_text())
shutil.copyfile(settings, '/pinry/pinry/settings/local_settings.py')
os.chdir('/pinry')
sys.path.insert(0, '/pinry')
os.environ['DJANGO_SETTINGS_MODULE'] = 'pinry.settings.docker'
import django
from django.core.management import call_command
from django.contrib.auth import get_user_model

django.setup()
call_command('migrate', interactive=False)
users = get_user_model().objects
if not users.exists():
    users.create_superuser(username=os.environ['ADMIN_USERNAME'],
                           email=os.environ['ADMIN_EMAIL'],
                           password=os.environ['ADMIN_PASSWORD'])
call_command('collectstatic', interactive=False)
subprocess.run(['chown', '-R', 'www-data:www-data', '/data'], check=True)
subprocess.run(['/usr/sbin/nginx'], check=True)
os.execvp('gunicorn', ['gunicorn', 'pinry.wsgi', '-b', '0.0.0.0:8000', '-w', '2',
                       '--capture-output', '--timeout', '30', '--user', 'www-data',
                       '--group', 'www-data', '--env', 'DJANGO_SETTINGS_MODULE=pinry.settings.docker'])
