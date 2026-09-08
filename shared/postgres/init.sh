#!/bin/bash
set -euo pipefail
: "${APP_USER:?APP_USER is required}"
: "${APP_PASSWORD:?APP_PASSWORD is required}"
: "${APP_DB:?APP_DB is required}"
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname postgres \
  --set=app_user="$APP_USER" --set=app_password="$APP_PASSWORD" --set=app_db="$APP_DB" <<'SQL'
CREATE ROLE :"app_user" LOGIN PASSWORD :'app_password' NOSUPERUSER NOCREATEDB NOCREATEROLE;
CREATE DATABASE :"app_db" OWNER :"app_user" TEMPLATE template0 ENCODING 'UTF8' LC_COLLATE 'C' LC_CTYPE 'C';
REVOKE ALL ON DATABASE :"app_db" FROM PUBLIC;
SQL
if [ "${ALLOW_APP_DATABASE_CREATION:-false}" = true ]; then
  # ToolJet creates its tenant roles and its two additional databases.
  psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname postgres --set=app_user="$APP_USER" <<'SQL'
ALTER ROLE :"app_user" CREATEDB CREATEROLE;
SQL
fi
if [ "${ENABLE_VECTOR:-false}" = true ]; then
  psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$APP_DB" -c 'CREATE EXTENSION IF NOT EXISTS vector;'
fi
