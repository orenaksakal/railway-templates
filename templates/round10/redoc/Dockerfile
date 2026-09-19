FROM redocly/redoc:v2.5.3@sha256:2e26bb660574c9b85eacd8e67b4e7a78641f5b63252859450688aeec6d918807
COPY templates/round10/redoc/openapi.json /opt/template/openapi.json
COPY --chmod=755 templates/round10/redoc/start.sh /opt/template/start.sh
ENTRYPOINT ["/opt/template/start.sh"]
