FROM linkace/linkace:v2.6.1@sha256:8a8359cae576a2eb68b58ece3acc4c1d56a0a45b3f01c151508287125acdfda5
USER root
RUN apk add --no-cache su-exec
COPY --chmod=755 templates/linkace/start.sh /railway-start.sh
ENTRYPOINT ["/railway-start.sh"]
