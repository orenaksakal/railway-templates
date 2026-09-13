#!/bin/bash
set -euo pipefail
umask 077
mkdir -p /data/storage /data/keys
if [ ! -s /data/keys/private.pem ]; then
  openssl genrsa -out /data/keys/private.pem.tmp 2048
  mv /data/keys/private.pem.tmp /data/keys/private.pem
fi
export LAGO_RSA_PRIVATE_KEY
LAGO_RSA_PRIVATE_KEY=$(openssl base64 -A -in /data/keys/private.pem)
# The image and this service share their assets; only /data is persistent.
if [ ! -L /app/storage ]; then
  cp -an /app/storage/. /data/storage/ 2>/dev/null || true
  rm -rf /app/storage
  ln -s /data/storage /app/storage
fi
cd /app
./scripts/migrate.sh
pids=()
stop() {
  trap - TERM INT
  kill -TERM "${pids[@]}" 2>/dev/null || true
  wait || true
}
trap stop TERM INT EXIT
./scripts/start.api.sh & pids+=("$!")
./scripts/start.worker.sh & pids+=("$!")
./scripts/start.clock.sh & pids+=("$!")
# Any required-process exit restarts the whole application unit.
wait -n "${pids[@]}" || true
exit 1
