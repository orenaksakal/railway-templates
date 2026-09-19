#!/bin/sh
set -eu
. /seed.sh
cd /rails
: "${ERRBIT_ADMIN_EMAIL:?Set the initial administrator email}"
: "${ERRBIT_ADMIN_PASSWORD:?}"
bundle exec rails runner /railway-bootstrap.rb
exec /rails/bin/docker-entrypoint bundle exec rails server -b 0.0.0.0 -p "${PORT:-3000}"
