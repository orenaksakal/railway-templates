#!/bin/sh
set -eu
. /seed.sh
for directory in database uploads logs; do
  seed_dir "/seed/$directory" "/data/$directory"
done
: "${ADMIN_PASSWORD:?}"
: "${WEB_HOST:?}"
caddy run --config /etc/caddy/Caddyfile --adapter caddyfile &
proxy_pid=$!
yarn workspace @chibisafe/backend start &
app_pid=$!
trap 'kill "$proxy_pid" "$app_pid" 2>/dev/null || true; wait; exit 0' TERM INT
# BusyBox ash wait -n returns as soon as either process exits.
set +e
wait -n "$proxy_pid" "$app_pid"
status=$?
kill "$proxy_pid" "$app_pid" 2>/dev/null || true
wait
[ "$status" -ne 0 ] || status=1
exit "$status"
