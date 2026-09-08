"""Patch the pinned 2.0.0 publisher constructor to retain Redis authentication."""
from pathlib import Path
path=Path('/usr/src/code/app/init/registers.php')
source=path.read_text()
old=r'new Queue\Connection\Redis($dsn->getHost(), $dsn->getPort())'
new=r'new Queue\Connection\Redis($dsn->getHost(), $dsn->getPort(), $dsn->getUser() ?: null, $dsn->getPassword() ?: null)'
if source.count(old)!=1:
    raise SystemExit('Pinned Appwrite publisher constructor changed; review Redis authentication before updating')
path.write_text(source.replace(old,new))
