"""Generate the configured user's bcrypt hash without storing plaintext in files."""
import os
import re
import bcrypt

user = os.environ.get('ADMIN_USERNAME', 'admin')
password = os.environ['ADMIN_PASSWORD']
if not re.fullmatch(r'[a-zA-Z0-9_-]{1,64}', user) or len(password) < 16 or len(password.encode()) > 72:
    raise SystemExit('Invalid administrator credentials')
os.environ['TIMETAGGER_CREDENTIALS'] = user + ':' + bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
os.execvp('python', ['python', '-m', 'timetagger'])
