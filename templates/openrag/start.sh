#!/bin/sh
set -eu
if [ ! -d /data/openrag-documents ]; then mkdir -p /data/openrag-documents; if [ -d /seed/openrag-documents ]; then cp -a /seed/openrag-documents/. /data/openrag-documents/; fi; fi
if [ ! -d /data/keys ]; then mkdir -p /data/keys; if [ -d /seed/keys ]; then cp -a /seed/keys/. /data/keys/; fi; fi
if [ ! -d /data/flows ]; then mkdir -p /data/flows; if [ -d /seed/flows ]; then cp -a /seed/flows/. /data/flows/; fi; fi
if [ ! -d /data/config ]; then mkdir -p /data/config; if [ -d /seed/config ]; then cp -a /seed/config/. /data/config/; fi; fi
if [ ! -d /data/data ]; then mkdir -p /data/data; if [ -d /seed/data ]; then cp -a /seed/data/. /data/data/; fi; fi
chown -R appuser /data
exec runuser -u appuser -- /entrypoint.sh "$@"
