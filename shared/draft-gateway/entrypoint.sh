#!/bin/sh
set -eu
# Use the container's resolver, including Railway's IPv6 private resolver.
resolver=$(awk '/^nameserver / {print $2; exit}' /etc/resolv.conf)
case "$resolver" in *:*) resolver="[$resolver]";; esac
export DNS_RESOLVER="$resolver"
exec /docker-entrypoint.sh nginx -g 'daemon off;'
