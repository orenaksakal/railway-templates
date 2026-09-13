"""Persist DB-GPT's whole pilot directory and render secrets as valid TOML."""
import json
import os
from pathlib import Path
import shutil

data = Path('/data/pilot')
source = Path('/app/pilot')
if not data.exists():
    if source.is_dir() and not source.is_symlink():
        shutil.copytree(source, data)
    else:
        data.mkdir(parents=True)
if source.is_dir() and not source.is_symlink():
    # Image-owned files only: user state is always in /data/pilot.
    shutil.rmtree(source)
if not source.is_symlink():
    source.symlink_to(data)
text = Path('/opt/railway/config.toml').read_text()
text = text.replace('"REPLACE_ENCRYPTION_KEY"', json.dumps(os.environ['ENCRYPTION_KEY']))
text = text.replace('"REPLACE_PUBLIC_URL"', json.dumps(os.environ['PUBLIC_URL']))
os.umask(0o077)
Path('/tmp/dbgpt.toml').write_text(text)
os.chdir('/app')
os.execvp('dbgpt', ['dbgpt', 'start', 'webserver', '--config', '/tmp/dbgpt.toml'])
