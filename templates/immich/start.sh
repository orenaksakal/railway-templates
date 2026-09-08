#!/bin/sh
set -eu
node /opt/railway-write-config.cjs
exec "$@"
