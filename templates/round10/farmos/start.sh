#!/bin/sh
set -eu
seed() {
    destination=$1
    source=$2
    if [ ! -d "$destination" ]; then
        staging=$(mktemp -d /data/.farmos-init.XXXXXX)
        trap 'rm -rf "$staging"' 0 HUP INT TERM
        cp -a "$source/." "$staging/"
        chown -R www-data:www-data "$staging"
        mv "$staging" "$destination"
        trap - 0 HUP INT TERM
    fi
}
seed /data/sites /var/farmOS/web/sites
seed /data/keys /opt/farmos-keys
# Apache reads the trusted private gateway's HTTPS header. The site installer
# sees the external HTTPS scheme and original Host without a fixed proxy IP.
exec /usr/local/bin/docker-entrypoint.sh "$@"
