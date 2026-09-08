#!/bin/bash
set -euo pipefail
mkdir -p /usr/share/elasticsearch/data
chown -R elasticsearch:root /usr/share/elasticsearch/data
exec runuser -u elasticsearch -g root -- /usr/local/bin/docker-entrypoint.sh eswrapper
