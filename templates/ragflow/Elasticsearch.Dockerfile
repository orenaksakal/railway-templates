FROM elasticsearch:8.11.3@sha256:58a3a280935d830215802322e9a0373faaacdfd646477aa7e718939c2f29292a
USER root
COPY --chmod=755 templates/ragflow/elasticsearch-start.sh /railway-start.sh
RUN command -v runuser
ENTRYPOINT ["/bin/tini", "--", "/railway-start.sh"]
