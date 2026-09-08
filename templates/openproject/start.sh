#!/bin/bash
set -euo pipefail
: "${DATABASE_URL:?DATABASE_URL is required}"
: "${SECRET_KEY_BASE:?SECRET_KEY_BASE is required}"
: "${OPENPROJECT_HOST__NAME:?OPENPROJECT_HOST__NAME is required}"
: "${OPENPROJECT_SEED__ADMIN__USER__PASSWORD:?An initial admin password is required}"
if [[ "$DATABASE_URL" == *'@127.0.0.1/'* ]]; then
  echo 'This template requires the separate persistent Postgres service' >&2
  exit 1
fi
# Upstream supervises web, workers, cache, collaborative editing, and Apache.
# It skips its internal database when DATABASE_URL points at the Postgres service.
exec ./docker/prod/entrypoint.sh ./docker/prod/supervisord
