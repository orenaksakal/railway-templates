FROM busybox:1.37.0-uclibc@sha256:8d7b1636e974e0adfd8d945955fca609304f0a56c18799dfd032d6e661382d84 AS bootstrap
FROM mockserver/mockserver:8.0.0@sha256:b8426e0b3c8089d65928531376147067002e8be4e9f437210b10a0395aeff6ce
USER root
COPY --from=bootstrap /bin/busybox /bootstrap
COPY templates/mockserver/start.sh /start.sh
ENTRYPOINT ["/bootstrap", "sh", "/start.sh"]
