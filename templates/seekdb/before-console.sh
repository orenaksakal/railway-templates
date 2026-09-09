#!/bin/bash
# The data-version file appears before the SQL listener is ready.
ready=false
for attempt in $(seq 1 180); do
  if MYSQL_PWD="$ROOT_PASSWORD" mysql --connect-timeout=2 -h127.0.0.1 -P2881 -uroot -e 'SELECT 1' >/dev/null 2>&1 || mysql --connect-timeout=2 -h127.0.0.1 -P2881 -uroot -e 'SELECT 1' >/dev/null 2>&1; then
    ready=true; break
  fi
  sleep 2
done
if [ "$ready" != true ]; then echo 'seekdb SQL readiness timed out' >&2; exit 1; fi
