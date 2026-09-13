#!/bin/sh
set -eu
# Fixed database identifiers; the dedicated cluster is owned by POSTGRES_USER.
for db in agenta_oss_core agenta_oss_tracing agenta_oss_supertokens; do
  psql --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" --set=ON_ERROR_STOP=1 \
    --command "CREATE DATABASE \"$db\";"
done
