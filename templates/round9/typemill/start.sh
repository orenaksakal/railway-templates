#!/bin/sh
set -eu
. /seed.sh
for directory in settings media cache plugins data content themes; do
  seed_dir "/seed/$directory" "/data/$directory"
  chown -R www-data:www-data "/data/$directory"
done
exec apache2-foreground
