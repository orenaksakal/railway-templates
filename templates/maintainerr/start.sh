#!/bin/sh
set -eu
mkdir -p /opt/data/logs
chown node:node /opt/data /opt/data/logs
exec su-exec node /opt/app/start.sh
