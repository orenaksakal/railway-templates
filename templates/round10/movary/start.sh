#!/bin/sh
set -eu
: "${TMDB_API_KEY:?Set your TMDB API key before deployment}"
mkdir -p /app/storage
chown application:application /app/storage
# Initialize the Railway volume as root, then run migrations and the service as
# the upstream application user. A failed migration must stop startup.
exec su -s /bin/sh application -c '
  set -eu
  cd /app
  php bin/console.php database:migration:migrate
  php bin/console.php storage:link
  exec /usr/bin/supervisord -c /etc/supervisor/conf.d/supervisord.conf
'
