#!/bin/bash
set -euo pipefail
# Preserve packaged configuration when Railway mounts an initially empty volume.
cp -an /railway-seed/. /var/lib/seekdb/
exec /root/start.sh "$@"
