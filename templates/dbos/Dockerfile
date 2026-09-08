FROM node:24-bookworm-slim@sha256:ba849c60be29959425b8734d57b8b4b7d56f98edd9504c9af091d5281095a71e
WORKDIR /app
COPY templates/dbos/package*.json ./
RUN npm ci --omit=dev && npm cache clean --force
COPY templates/dbos/server.mjs ./
COPY shared/wait-for-dependencies.mjs ./
USER node
CMD ["node", "server.mjs"]
