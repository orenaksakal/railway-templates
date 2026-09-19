#!/bin/sh
set -eu
. /seed.sh
for directory in uploads media; do
  seed_dir "/seed/$directory" "/data/$directory"
  chown -R www-data:www-data "/data/$directory"
done
mkdir -p /data/db
chown www-data:www-data /data/db
# Upstream migrations initialize the administrator; never run password-reset commands.
sudo -E -u www-data php bin/console doctrine:migrations:migrate --no-interaction
exec partdb-entrypoint.sh /usr/local/bin/apache2-foreground
