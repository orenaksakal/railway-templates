"""Patch the pinned 2.0.0 publisher constructor to retain Redis authentication."""
from pathlib import Path
path=Path('/usr/src/code/app/init/registers.php')
source=path.read_text()
old=r'new Queue\Connection\Redis($dsn->getHost(), $dsn->getPort())'
new=r'new Queue\Connection\Redis($dsn->getHost(), $dsn->getPort(), $dsn->getUser() ?: null, $dsn->getPassword() ?: null)'
if source.count(old)!=1:
    raise SystemExit('Pinned Appwrite publisher constructor changed; review Redis authentication before updating')
path.write_text(source.replace(old,new))

# The bundled lazy connection accepts credentials but never authenticates.
path = Path('/usr/src/code/vendor/utopia-php/queue/src/Queue/Connection/Redis.php')
source = path.read_text()
old = '$redis->connect($this->host, $this->port, $connectTimeout);'
new = old + "\n                if ($this->password !== null && $this->password !== '') {\n                    $redis->auth($this->user ? [$this->user, $this->password] : $this->password);\n                }"
if source.count(old) != 1:
    raise SystemExit('Pinned queue connection changed; review authentication')
path.write_text(source.replace(old, new))
