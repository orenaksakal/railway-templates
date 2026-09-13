FROM ghcr.io/useplunk/plunk:0.14.0@sha256:82784a77c97269a198778e6f5c50a4385356eee36d1b2928c281b9100ae2ec7a
USER root
RUN apk add --no-cache su-exec
COPY --chmod=755 templates/plunk/start.sh /opt/railway/start.sh
ENTRYPOINT ["/opt/railway/start.sh"]
