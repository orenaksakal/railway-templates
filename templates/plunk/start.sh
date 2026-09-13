#!/bin/sh
set -eu
mkdir -p /app/data
chown plunk:nodejs /app/data
exec su-exec plunk:nodejs /usr/local/bin/docker-entrypoint-nginx.sh "$@"
