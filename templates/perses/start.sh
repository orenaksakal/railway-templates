#!/bin/sh
set -eu
umask 077
: "${ENCRYPTION_KEY:?}"
case "$ENCRYPTION_KEY" in *[!a-zA-Z0-9]*) exit 1;; esac
[ "${#ENCRYPTION_KEY}" -eq 32 ] || exit 1
mkdir -p /data/db /data/plugins
cat > /tmp/perses.yaml <<EOF
security:
  enable_auth: false
  encryption_key: "$ENCRYPTION_KEY"
database:
  file:
    folder: /data/db
    extension: json
plugin:
  path: /data/plugins
EOF
# The private service is reached only through the owner-authenticated gateway.
exec /bin/perses --config=/tmp/perses.yaml --log.level=info
