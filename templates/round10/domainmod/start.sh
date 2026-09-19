#!/bin/sh
set -eu
if [ ! -d /data/temp ]; then
    staging=$(mktemp -d /data/.domainmod-init.XXXXXX)
    trap 'rm -rf "$staging"' 0 HUP INT TERM
    cp -a /opt/domainmod-temp/. "$staging/"
    chown -R www-data:www-data "$staging"
    mv "$staging" /data/temp
    trap - 0 HUP INT TERM
fi
php /usr/local/bin/domainmod-render-config.php
cron
exec docker-php-entrypoint "$@"
