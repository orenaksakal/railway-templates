#!/bin/sh
set -eu
: "${MINIO_ROOT_USER:?Required}"
: "${MINIO_ROOT_PASSWORD:?Required}"
: "${S3_BUCKET:?Required}"
minio server /data --console-address :9001 &
server=$!
trap 'kill -TERM "$server"; wait "$server"' TERM INT
attempt=0
until mc alias set local http://127.0.0.1:9000 "$MINIO_ROOT_USER" "$MINIO_ROOT_PASSWORD" >/dev/null 2>&1; do
  attempt=$((attempt + 1));[ "$attempt" -lt 90 ] || { kill "$server"; exit 1; };sleep 2
done
mc mb --ignore-existing "local/$S3_BUCKET" >/dev/null
# No anonymous bucket policy is installed.
wait "$server"
