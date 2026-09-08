#!/bin/sh
set -eu
mkdir -p /tmp/element-web-config
envsubst '${HOMESERVER_URL} ${SERVER_NAME}' < /etc/railway-element.json.template > /tmp/element-web-config/config.json
