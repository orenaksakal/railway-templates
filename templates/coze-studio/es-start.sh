#!/bin/bash
set -euo pipefail
/opt/bitnami/scripts/elasticsearch/setup.sh
mkdir -p /bitnami/elasticsearch/data
chown -R elasticsearch:elasticsearch /bitnami/elasticsearch/data
cp /railway-elasticsearch.yml /opt/bitnami/elasticsearch/config/elasticsearch.yml
exec /opt/bitnami/scripts/elasticsearch/run.sh
