FROM node:22-alpine@sha256:c610fcdfb1d5b4740dd70c284ed3cb16bb857e0f7166196e36a5501df7a3aa32
WORKDIR /app
COPY templates/firecrawl/gateway.mjs /app/gateway.mjs
USER node
EXPOSE 8080
CMD ["node", "/app/gateway.mjs"]
