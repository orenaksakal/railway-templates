FROM ghcr.io/formbricks/hub:0.8.7@sha256:027537bc6f3025aa3603a73fc741989fcf52105129e11959eec4e80ce65c037c
USER root
RUN apk add --no-cache postgresql17-client
USER app
COPY templates/formbricks/migration-version templates/formbricks/migrations-ready.sql /app/
COPY --chmod=755 templates/formbricks/hub-start.sh /app/railway-start.sh
ENTRYPOINT ["/app/railway-start.sh"]
