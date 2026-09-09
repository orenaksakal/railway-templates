#!/bin/bash
set -euo pipefail
/opt/bitnami/scripts/etcd/setup.sh
mkdir -p /bitnami/etcd/data
chown -R etcd:etcd /bitnami/etcd
chmod 700 /bitnami/etcd/data
exec /opt/bitnami/scripts/etcd/run.sh
