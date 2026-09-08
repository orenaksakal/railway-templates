#!/bin/sh
set -eu
: "${MINIO_ROOT_USER:?}" "${MINIO_ROOT_PASSWORD:?}" "${S3_BUCKETS:?}"
minio server /data --console-address ':9001' &
pid=$!
trap 'kill -TERM "$pid"; wait "$pid"' TERM INT
ready=false
for attempt in $(seq 1 90); do
 if mc alias set local http://127.0.0.1:9000 "$MINIO_ROOT_USER" "$MINIO_ROOT_PASSWORD" >/dev/null 2>&1; then ready=true; break; fi
 sleep 2
done
if [ "$ready" != true ]; then kill "$pid"; exit 1; fi
for bucket in $S3_BUCKETS; do mc mb --ignore-existing "local/$bucket"; done
if [ -d /seed ]; then
 for dir in /seed/*; do [ -d "$dir" ] || continue; mc cp --recursive "$dir/" "local/opencoze/$(basename "$dir")/"; done
fi
wait "$pid"
