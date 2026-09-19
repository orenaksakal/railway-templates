FROM ghcr.io/bewcloud/bewcloud:v4.15.0@sha256:8ea552f5e335ba8772a731f598a58a4ecf2de72dfc618c2a825ec4e298a1d514
USER root
RUN command -v runuser
COPY templates/round9/bewcloud/bewcloud.config.ts /app/bewcloud.config.ts

COPY shared/round9-bootstrap/seed.sh /seed.sh
COPY --chmod=755 templates/round9/bewcloud/start.sh /railway-start.sh
ENTRYPOINT ["/railway-start.sh"]
