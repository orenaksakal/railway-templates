#!/bin/sh
set -eu
. /seed.sh
mkdir -p /app/data-files
chown -R deno:deno /app/data-files
cd /app
runuser -u deno -- deno task migrate-db
exec /tini -- runuser -u deno -- deno task preview
