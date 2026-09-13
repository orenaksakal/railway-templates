#!/bin/sh
set -eu
mkdir -p /data
chown frappe:frappe /data
exec runuser -u frappe -- python /opt/railway/start.py
