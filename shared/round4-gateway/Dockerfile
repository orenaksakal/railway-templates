FROM nginx:1.28-alpine@sha256:a8b39bd9cf0f83869a2162827a0caf6137ddf759d50a171451b335cecc87d236
RUN apk add --no-cache apache2-utils
COPY --chmod=755 shared/round4-gateway/start.sh /start.sh
COPY shared/round4-gateway/default.conf.template /etc/nginx/templates/default.conf.template
ENV NGINX_ENVSUBST_FILTER="^(DNS_RESOLVER|UPSTREAM_HOST|UPSTREAM_PORT)$"
ENTRYPOINT ["/start.sh"]
