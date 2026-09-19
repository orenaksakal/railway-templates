#!/bin/sh
set -eu
mkdir -p /data
chown mountebank:mountebank /data
exec su -s /bin/sh mountebank -c 'exec mb start --host :: --port 2525 --datadir /data --pidfile /tmp/mb.pid --nologfile --loglevel warn'
