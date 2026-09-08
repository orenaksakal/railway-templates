FROM authzed/spicedb:v1.56.1@sha256:db0d1a16e6a49e88c4e5dc183f98d8ef02b27cb728e62e94829fd64faacfb775 AS upstream
FROM alpine:3.22@sha256:14358309a308569c32bdc37e2e0e9694be33a9d99e68afb0f5ff33cc1f695dce
RUN apk add --no-cache ca-certificates
COPY --from=upstream /usr/local/bin/spicedb /usr/local/bin/spicedb
COPY --chmod=755 templates/spicedb/start.sh /start.sh
ENTRYPOINT ["/start.sh"]
