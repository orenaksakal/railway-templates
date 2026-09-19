#!/bin/sh
set -eu
mkdir -p /data/www /data/config
if [ ! -e /data/www/index.sql ]; then
  cp /opt/starter/index.sql /data/www/index.sql
fi
exec /usr/local/bin/sqlpage
