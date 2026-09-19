#!/bin/sh
set -eu
mkdir -p /config
if [ ! -e /config/config.yaml ]; then
  cp /opt/railway-config.yaml /config/config.yaml
fi
chown olivetin:olivetin /config /config/config.yaml
exec su -s /bin/sh olivetin -c 'exec /usr/bin/OliveTin'
