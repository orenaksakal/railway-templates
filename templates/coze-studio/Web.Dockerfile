FROM cozedev/coze-studio-web:latest@sha256:a137a16ab75b871b08911ca87359fc8981b225b63b94cf3e0979069fbd862aea
COPY templates/coze-studio/default.conf.template /etc/nginx/templates/default.conf.template
COPY --chmod=755 shared/draft-gateway/entrypoint.sh /start.sh
ENV NGINX_ENVSUBST_FILTER="^(DNS_RESOLVER|BACKEND_HOST|STORAGE_HOST)$"
ENTRYPOINT ["/start.sh"]
