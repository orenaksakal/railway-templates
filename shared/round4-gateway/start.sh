#!/bin/sh
set -eu
: "${ACCESS_USER:?}" "${ACCESS_PASSWORD:?}" "${UPSTREAM_HOST:?}" "${UPSTREAM_PORT:?}"
printf '%s\n' "$ACCESS_PASSWORD" | htpasswd -ic /etc/nginx/htpasswd "$ACCESS_USER" >/dev/null
chmod 644 /etc/nginx/htpasswd
resolver=$(awk '/^nameserver / {print $2; exit}' /etc/resolv.conf)
case "$resolver" in *:*) resolver="[$resolver]";; esac
export DNS_RESOLVER="$resolver"
exec /docker-entrypoint.sh nginx -g 'daemon off;'
