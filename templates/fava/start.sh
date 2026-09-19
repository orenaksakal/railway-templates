#!/bin/sh
set -eu
mkdir -p /data
if [ ! -e /data/main.beancount ]; then
  cp /opt/starter.beancount /data/main.beancount
fi
exec fava --host 0.0.0.0 --port 5000 /data/main.beancount
