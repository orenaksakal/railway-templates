#!/bin/sh
set -eu
: "${DATABASE_URL:?DATABASE_URL is required}"
: "${FORMBRICKS_MIGRATIONS_URL:?FORMBRICKS_MIGRATIONS_URL is required}"
ready=false
for attempt in $(seq 1 150); do
  if wget -q -T 5 -O /dev/null "$FORMBRICKS_MIGRATIONS_URL"; then ready=true; break; fi
  sleep 2
done
if [ "$ready" != true ]; then echo 'Formbricks migrations did not become ready' >&2; exit 1; fi
goose -dir /app/migrations postgres "$DATABASE_URL" up
river migrate-up --database-url "$DATABASE_URL"
exec /app/hub-api
