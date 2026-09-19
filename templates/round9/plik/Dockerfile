FROM rootgg/plik:1.4.2@sha256:d36651f60ec0dfd213ad3605eb9353f46be47d4d015b9104897acf362a9bd730
USER root
RUN apk add --no-cache su-exec
COPY templates/round9/plik/plikd.cfg /etc/plikd.cfg

COPY shared/round9-bootstrap/seed.sh /seed.sh
COPY --chmod=755 templates/round9/plik/start.sh /railway-start.sh
ENTRYPOINT ["/railway-start.sh"]
