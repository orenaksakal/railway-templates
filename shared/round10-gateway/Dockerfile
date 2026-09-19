FROM nginx:1.28-alpine@sha256:a8b39bd9cf0f83869a2162827a0caf6137ddf759d50a171451b335cecc87d236
RUN apk add --no-cache apache2-utils
COPY --chmod=755 shared/round10-gateway/start.sh /start.sh
COPY shared/round10-gateway/default.conf.template /etc/nginx/templates/default.conf.template
COPY shared/round10-gateway/proxy.inc /etc/nginx/proxy.inc
ENV NGINX_ENVSUBST_FILTER="^(DNS_RESOLVER|UPSTREAM_HOST|UPSTREAM_PORT|AUTH_REALM|ACCESS_PASSWORD|OWNER_SCOPE|ACCESS_COOKIE_TOKEN)$"
ENTRYPOINT ["/start.sh"]
