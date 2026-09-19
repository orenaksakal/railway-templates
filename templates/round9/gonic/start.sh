#!/bin/sh
set -eu
. /seed.sh
mkdir -p /data/music /data/cache /data/podcasts /data/playlists
exec /sbin/tini -- gonic
