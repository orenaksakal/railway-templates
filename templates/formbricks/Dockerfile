FROM ghcr.io/formbricks/formbricks:5.4.2@sha256:4c32097d49ae9b5c53ffb42716f1302e0e5a26e6ea43914333feb4c53211a139
USER root
RUN apk add --no-cache su-exec
COPY templates/formbricks/start.mjs /home/nextjs/railway-start.mjs
COPY templates/formbricks/record-migrations.mjs templates/formbricks/migration-version /home/nextjs/
COPY shared/wait-for-dependencies.mjs /home/nextjs/wait-for-dependencies.mjs
COPY --chmod=755 templates/formbricks/entrypoint.sh /home/nextjs/railway-entrypoint.sh
ENV HOSTNAME=0.0.0.0
ENTRYPOINT ["/home/nextjs/railway-entrypoint.sh"]
CMD ["node", "/home/nextjs/railway-start.mjs"]
