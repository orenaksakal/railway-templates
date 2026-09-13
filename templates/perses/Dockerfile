FROM persesdev/perses:v0.54.0@sha256:a0e34ddaf9d7599d96036611af205b948c1179646844202d869f3bcf3d5d9e9c AS upstream
FROM nginx:1.28-alpine@sha256:a8b39bd9cf0f83869a2162827a0caf6137ddf759d50a171451b335cecc87d236
COPY --from=upstream /bin/perses /bin/perses
COPY --from=upstream /etc/perses /etc/perses
COPY --from=upstream /LICENSE /LICENSE
COPY --from=upstream /etc/mime.types /etc/mime.types
COPY --chmod=755 templates/perses/start.sh /start.sh
ENTRYPOINT ["/start.sh"]
