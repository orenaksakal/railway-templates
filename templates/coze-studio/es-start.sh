#!/bin/bash
set -euo pipefail
mkdir -p /bitnami/elasticsearch/data
chown -R elasticsearch:elasticsearch /bitnami/elasticsearch/data
exec su -s /bin/bash elasticsearch -c "/opt/bitnami/elasticsearch/bin/elasticsearch"
