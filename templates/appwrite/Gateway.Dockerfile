FROM nginx:1.28-alpine@sha256:a8b39bd9cf0f83869a2162827a0caf6137ddf759d50a171451b335cecc87d236
COPY --chmod=755 shared/draft-gateway/entrypoint.sh /railway-entrypoint.sh
COPY templates/appwrite/gateway.conf.template /etc/nginx/templates/default.conf.template
ENTRYPOINT ["/railway-entrypoint.sh"]
