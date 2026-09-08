#!/bin/sh
set -eu
umask 077
: "${DATABASE_URL:?DATABASE_URL is required}"
: "${REDIS_SERVER_HOST:?REDIS_SERVER_HOST is required}"
# One volume retains both the private signing key and uploaded workspace files.
mkdir -p /root/.affine/config /root/.affine/storage
node /app/wait-for-dependencies.mjs
node ./scripts/self-host-predeploy.js
exec node ./dist/main.js
