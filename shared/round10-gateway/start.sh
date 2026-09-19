#!/bin/sh
set -eu
: "${UPSTREAM_HOST:?}" "${UPSTREAM_PORT:?}"
case "$UPSTREAM_HOST" in *[!a-zA-Z0-9.:-]*|'') exit 1;; esac
case "$UPSTREAM_PORT" in *[!0-9]*|'') exit 1;; esac
resolver=$(awk '/^nameserver / {print $2; exit}' /etc/resolv.conf)
case "$resolver" in *:*) resolver="[$resolver]";; esac
export DNS_RESOLVER="$resolver"
export OWNER_SCOPE="${OWNER_SCOPE:-all}"
case "$OWNER_SCOPE" in all) ;; *) echo "Round10 owner cookies require OWNER_SCOPE=all" >&2; exit 1;; esac
export AUTH_REALM=off
export ACCESS_COOKIE_TOKEN=disabled-owner-cookie
if [ "${OWNER_AUTH:-true}" = true ]; then
  : "${ACCESS_PASSWORD:?}"
  case "$ACCESS_PASSWORD" in *[!a-zA-Z0-9]*|'') echo 'Owner password must be alphanumeric' >&2; exit 1;; esac
  printf '%s\n' "$ACCESS_PASSWORD" | htpasswd -ic /etc/nginx/htpasswd admin >/dev/null
  chmod 644 /etc/nginx/htpasswd
  export ACCESS_COOKIE_TOKEN=$(printf 'round10-owner-session:%s' "$ACCESS_PASSWORD" | sha256sum | cut -d ' ' -f 1)
  case "$ACCESS_COOKIE_TOKEN" in ''|*[!a-f0-9]*) echo 'Owner cookie derivation failed' >&2; exit 1;; esac
  [ "${#ACCESS_COOKIE_TOKEN}" -eq 64 ] || exit 1
  export AUTH_REALM='Template owner'
else
  export ACCESS_PASSWORD=disabled-header-auth
fi
exec /docker-entrypoint.sh nginx -g 'daemon off;'
