#!/bin/sh
set -eu
: "${SPICEDB_DATASTORE_CONN_URI:?Database connection is required}"
: "${SPICEDB_GRPC_PRESHARED_KEY:?Authentication key is required}"
# Never serve an unmigrated datastore. Retry handles a cold database start.
attempt=0
until spicedb migrate head; do
  attempt=$((attempt + 1))
  [ "$attempt" -lt 60 ] || exit 1
  sleep 5
done
exec spicedb serve
