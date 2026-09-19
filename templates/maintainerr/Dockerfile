FROM ghcr.io/maintainerr/maintainerr:3.29.0@sha256:7487d374290e59add65407ec295629e489f9057dbf18e2a9dff70d6201ffb6f9
USER root
RUN apk add --no-cache su-exec
COPY --chmod=755 templates/maintainerr/start.sh /railway-start.sh
ENTRYPOINT ["/railway-start.sh"]
