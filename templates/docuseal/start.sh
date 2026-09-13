#!/bin/sh
set -eu
: "${DATABASE_URL:?}" "${ADMIN_EMAIL:?}" "${ADMIN_PASSWORD:?}" "${PUBLIC_URL:?}"
# Rails initializes and migrates before running the bootstrap script. Transient
# database failures cause a bounded Railway restart; no listener opens early.
cd /app
/app/bin/bundle exec rails runner /opt/railway/bootstrap.rb
exec /app/bin/bundle exec puma -C /app/config/puma.rb --dir /app
