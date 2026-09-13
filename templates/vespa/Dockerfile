FROM vespaengine/vespa:8.751.13@sha256:371dd6b1ea51fb9fee30cfee70d1894ac02dbc7408318ce016eae1bb78b43a1e
USER root
COPY templates/vespa/application /opt/railway/application
COPY --chmod=755 templates/vespa/start.sh /opt/railway/start.sh
RUN command -v runuser && command -v curl && test -x /usr/local/bin/start-container.sh
ENTRYPOINT ["/opt/railway/start.sh"]
