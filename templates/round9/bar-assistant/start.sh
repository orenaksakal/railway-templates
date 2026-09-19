#!/bin/sh
set -eu
: "${APP_KEY:?}"
mkdir -p /var/www/cocktails/storage/bar-assistant
chown -R www-data:www-data /var/www/cocktails/storage/bar-assistant
exec runuser -u www-data -- docker-php-serversideup-entrypoint "$@"
