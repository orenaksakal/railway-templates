#!/bin/sh
set -eu
. /seed.sh
mkdir -p /data/files
chown -R plik:plik /data
exec su-exec plik ./plikd --config /etc/plikd.cfg
