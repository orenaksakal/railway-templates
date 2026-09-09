#!/bin/bash
set -euo pipefail
mkdir -p /usr/share/opensearch/data
chown -R opensearch:opensearch /usr/share/opensearch/data
exec runuser -u opensearch -- /usr/share/opensearch/opensearch-entrypoint-wrapper.sh "$@"
