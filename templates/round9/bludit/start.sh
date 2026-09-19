#!/bin/sh
set -eu
. /seed.sh
for directory in bl-content bl-themes bl-plugins; do
  seed_dir "/seed/$directory" "/data/$directory"
  chown -R www-data:www-data "/data/$directory"
done
exec /docker-entrypoint.sh
