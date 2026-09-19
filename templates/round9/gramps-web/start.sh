#!/bin/sh
set -eu
: "${OWNER_EMAIL:?Set the initial owner email}"
: "${OWNER_PASSWORD:?}"
mkdir -p /data/users /data/media /data/index /data/thumbnail_cache /data/cache /data/grampsdb /data/home
exec /docker-entrypoint.sh python3 /railway-supervise.py
