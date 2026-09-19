FROM caddy:2-alpine@sha256:de23def33b17fb5d1290b0f6c2add1d70780e52341896c00a4c8a2a2fe9d355e AS caddy
FROM chibisafe/chibisafe-server:v6.5.5@sha256:3da4fcbc1a183e6108cd3c02295fda5dc85acea4d6b830a0cfd7720c5d5d3c67
COPY --from=caddy /usr/bin/caddy /usr/bin/caddy
RUN mkdir -p /seed && for directory in database uploads logs; do mkdir -p "/app/$directory"; cp -a "/app/$directory" "/seed/$directory"; rm -rf "/app/$directory"; ln -s "/data/$directory" "/app/$directory"; done
COPY templates/round9/chibisafe/Caddyfile /etc/caddy/Caddyfile

COPY shared/round9-bootstrap/seed.sh /seed.sh
COPY --chmod=755 templates/round9/chibisafe/start.sh /railway-start.sh
ENTRYPOINT ["/railway-start.sh"]
