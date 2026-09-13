#!/bin/bash
set -euo pipefail
# Railway volumes are mounted at runtime; initialize ownership before dropping privileges.
mkdir -p /opt/vespa/var
chown vespa:vespa /opt/vespa/var
runuser -u vespa -- /usr/local/bin/start-container.sh &
pid=$!
trap 'kill -TERM "$pid" 2>/dev/null || true; wait "$pid" || true' TERM INT EXIT
ready=false
for attempt in $(seq 1 240); do
  kill -0 "$pid" 2>/dev/null || exit 1
  if curl -fsS http://127.0.0.1:19071/state/v1/health >/dev/null; then ready=true; break; fi
  sleep 2
done
[ "$ready" = true ] || exit 1
marker=/opt/vespa/var/.railway-starter-deployed
if [ ! -f "$marker" ]; then
  runuser -u vespa -- /opt/vespa/bin/vespa-deploy prepare /opt/railway/application
  runuser -u vespa -- /opt/vespa/bin/vespa-deploy activate
  touch "$marker"
fi
# Never overwrite an operator's application schema on restart/redeploy.
wait "$pid"
