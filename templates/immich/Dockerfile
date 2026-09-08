FROM ghcr.io/immich-app/immich-server:v3.1.0@sha256:b434cb9287eea1471c9974845914d4dd328c9c2d652e446ed4930f99944f0ceb
COPY templates/immich/write-config.cjs /opt/railway-write-config.cjs
COPY --chmod=755 templates/immich/start.sh /opt/railway-start.sh
ENTRYPOINT ["tini", "--", "/opt/railway-start.sh"]
CMD ["start.sh"]
