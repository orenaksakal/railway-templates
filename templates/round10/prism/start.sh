#!/bin/sh
set -eu
mkdir -p /data
if [ ! -e /data/openapi.json ]; then
    cp /opt/template/openapi.json /data/openapi.json
fi
exec /sbin/tini -- node /usr/src/prism/packages/cli/dist/index.js mock /data/openapi.json --host :: --port 4010 --multiprocess false --errors --verboseLevel warn
