#!/bin/sh
set -eu
mkdir -p /data
if [ ! -e /data/openapi.json ]; then
    cp /opt/template/openapi.json /data/openapi.json
fi
ln -sf /data/openapi.json /usr/share/nginx/html/openapi.json
export SPEC_URL=/openapi.json
export PAGE_TITLE='Private API documentation'
export PORT=8080
exec /bin/sh /usr/local/bin/docker-run.sh
