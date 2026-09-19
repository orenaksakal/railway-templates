FROM lovasoa/sqlpage:v0.46.3@sha256:354c683a50f541be01d427b3b664f1d5b36c28739f45bfb809be14b99b6ff649
USER root
COPY templates/sqlpage/index.sql /opt/starter/index.sql
COPY --chmod=755 templates/sqlpage/start.sh /start.sh
ENTRYPOINT ["/start.sh"]
