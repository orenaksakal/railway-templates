#!/bin/bash
set -euo pipefail
: "${PG_HOST:?PG_HOST is required}"
: "${PG_PASS:?PG_PASS is required}"
: "${REDIS_HOST:?REDIS_HOST is required}"
: "${SECRET_KEY_BASE:?SECRET_KEY_BASE is required}"
: "${LOCKBOX_MASTER_KEY:?LOCKBOX_MASTER_KEY is required}"
# The CE entrypoint starts an unused, non-persistent local Redis. Use the dedicated
# persistent service instead and retain upstream's database setup behavior.
./server/scripts/wait-for-it.sh "$PG_HOST:${PG_PORT:-5432}" --strict --timeout=300
./server/scripts/wait-for-it.sh "$REDIS_HOST:${REDIS_PORT:-6379}" --strict --timeout=180
npm run db:setup:prod
exec "$@"
