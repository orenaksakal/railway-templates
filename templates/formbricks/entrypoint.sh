#!/bin/sh
set -eu
mkdir -p /home/nextjs/apps/web/uploads
chown nextjs:nextjs /home/nextjs/apps/web/uploads
exec su-exec nextjs "$@"
