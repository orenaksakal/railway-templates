#!/bin/sh
set -eu
: "${DATABASE_URL:?DATABASE_URL is required}"
: "${FORMBRICKS_MIGRATIONS_WAIT_SECONDS:=600}"
case "$FORMBRICKS_MIGRATIONS_WAIT_SECONDS" in
  ''|*[!0-9]*) echo 'Migration wait timeout must be a positive integer' >&2; exit 1 ;;
esac
[ "$FORMBRICKS_MIGRATIONS_WAIT_SECONDS" -gt 0 ] || exit 1
release=$(cat /app/migration-version)
[ -n "$release" ] || { echo 'Migration release is missing' >&2; exit 1; }
deadline=$(( $(date +%s) + FORMBRICKS_MIGRATIONS_WAIT_SECONDS ))
ready=false
# Connect directly to PostgreSQL. Waiting for Formbricks HTTP/DNS here would
# make startup depend on a service that is itself waiting for Hub's healthcheck.
while [ "$(date +%s)" -lt "$deadline" ]; do
  if [ "$(PGCONNECT_TIMEOUT=5 PGOPTIONS='-c statement_timeout=5000' \
    psql --dbname="$DATABASE_URL" -X -A -t -v ON_ERROR_STOP=1 -v "release=$release" -f /app/migrations-ready.sql 2>/dev/null)" = t ]; then
    ready=true
    break
  fi
  sleep 2
done
if [ "$ready" != true ]; then echo 'Formbricks migrations did not become ready' >&2; exit 1; fi
goose -dir /app/migrations postgres "$DATABASE_URL" up
river migrate-up --database-url "$DATABASE_URL"
exec /app/hub-api
