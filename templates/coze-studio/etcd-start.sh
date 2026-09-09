#!/bin/bash
set -euo pipefail
mkdir -p /bitnami/etcd/data
chown -R 1001:1001 /bitnami/etcd
exec /opt/bitnami/scripts/etcd/entrypoint.sh /opt/bitnami/scripts/etcd/run.sh
