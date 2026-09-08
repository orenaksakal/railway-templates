#!/bin/bash
set -euo pipefail
mkdir -p /data/replica
if [ ! -s /data/replica/key ]; then
  openssl rand -base64 756 > /data/replica/key
  chmod 400 /data/replica/key
fi
chown -R mongodb:mongodb /data/replica
/usr/local/bin/docker-entrypoint.sh mongod --bind_ip_all --replSet rs0 --keyFile /data/replica/key &
server=$!
trap 'kill -TERM "$server"; wait "$server"' TERM INT
ready=false
for attempt in $(seq 1 90); do
  if mongosh --quiet --host 127.0.0.1 --username "$MONGO_INITDB_ROOT_USERNAME" --password "$MONGO_INITDB_ROOT_PASSWORD" --authenticationDatabase admin --eval 'try { rs.status(); } catch (e) { if (e.code !== 94) throw e; rs.initiate({_id:"rs0",members:[{_id:0,host:process.env.MONGO_PRIVATE_HOST+":27017"}]}); }' >/dev/null 2>&1; then
    ready=true; break
  fi
  sleep 2
done
if [ "$ready" != true ]; then kill "$server"; echo 'MongoDB replica initialization failed' >&2; exit 1; fi
wait "$server"
