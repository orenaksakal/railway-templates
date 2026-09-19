#!/bin/sh
set -eu
seed() {
    destination=$1
    source=$2
    if [ ! -d "$destination" ]; then
        staging=$(mktemp -d /data/.librebooking-init.XXXXXX)
        trap 'rm -rf "$staging"' 0 HUP INT TERM
        cp -a "$source/." "$staging/"
        chown -R www-data:root "$staging"
        mv "$staging" "$destination"
        trap - 0 HUP INT TERM
    fi
}
seed /data/config /opt/librebooking-config
seed /data/images /opt/librebooking-images
mkdir -p /data/reservations
chown www-data:root /data/reservations
# No login shell: preserve Railway's environment for upstream configuration.
exec su -s /bin/sh www-data -c 'exec /usr/local/bin/entrypoint.sh "$@"' -- sh "$@"
