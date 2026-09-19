FROM bytebase/dbhub:1.2.5@sha256:969e89e22d38e4114137e55e55c8db7b8640f6619d2ba9314c80d06c01f294c2
COPY templates/round9/dbhub/start.mjs /app/railway-start.mjs
COPY templates/round9/dbhub/config.mjs /app/config.mjs
ENTRYPOINT ["node", "/app/railway-start.mjs"]
