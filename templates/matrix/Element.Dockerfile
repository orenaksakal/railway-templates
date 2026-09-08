FROM ghcr.io/element-hq/element-web:v1.12.27@sha256:7050130b263bbcf0e4ad8da875a2821cd89dc55b2f04e93aaa13f682d013019e
COPY templates/matrix/element-config.json /etc/railway-element.json.template
COPY --chmod=755 templates/matrix/element-entrypoint.sh /docker-entrypoint.d/25-element-config.sh
