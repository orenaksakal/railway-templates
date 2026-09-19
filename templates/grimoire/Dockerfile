FROM oven/bun:1.4.2@sha256:9114c058aeae42162ee16dd5084b95fe9473970bb6bcb5b232ab1630f0546895 AS builder
WORKDIR /app
ADD --checksum=sha256:9a69c48fae62eb1938cbe25b9d3a4f3276b9908b4576fd27938027ab0bc2022e https://codeload.github.com/goniszewski/grimoire/tar.gz/ca974f3561399302b56e2b2b7f52036766dc4117 /tmp/source.tar.gz
RUN tar -xzf /tmp/source.tar.gz --strip-components=1 -C /app && rm /tmp/source.tar.gz
RUN bun install --frozen-lockfile && cd daemon && bun install --frozen-lockfile
RUN bun run build
FROM oven/bun:1.4.2-slim@sha256:cb3bbbb08e13a4a2ff400f24c7a2a1d5efa83f6ef8544d52d95a519631e2fc61
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/daemon ./daemon
COPY --from=builder /app/package.json ./package.json
ENV HOST=0.0.0.0 PORT=3210 DATA_DIR=/data HOME=/data XDG_CONFIG_HOME=/data/config NODE_ENV=production LITTLEIMP_IN_CONTAINER=1
EXPOSE 3210
CMD ["bun", "run", "daemon:start"]
