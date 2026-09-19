#!/bin/sh
set -eu
mkdir -p /data
if [ ! -d /data/storage ]; then
  mkdir -p /data/storage
  cp -a /app/storage/. /data/storage/
  chown -R www-data:www-data /data/storage
fi
if [ ! -L /app/storage ]; then
  mv /app/storage /app/storage.image
  ln -s /data/storage /app/storage
fi
if [ ! -f /data/database.sqlite ]; then
  touch /data/database.sqlite
fi
chown www-data:www-data /data /data/database.sqlite
exec su-exec www-data /usr/bin/supervisord -c /etc/supervisor.d/supervisord.ini
