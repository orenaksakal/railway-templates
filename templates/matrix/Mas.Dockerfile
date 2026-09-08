FROM ghcr.io/element-hq/matrix-authentication-service:1.24.0@sha256:52c18ffcc940220a3b6aa5985b7e09d24ac27f5ed10a4d660c312e48f73ff105 AS upstream
FROM python:3.13-slim-trixie@sha256:9d2e5553305c7c7b0097999bb17187c69b921ccd6bc9d40e4bb5ebe652c00285
RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates libssl3t64 libgcc-s1 && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir PyYAML==6.0.2
COPY --from=upstream /usr/local/bin/mas-cli /usr/local/bin/mas-cli
COPY --from=upstream /usr/local/share/mas-cli /usr/local/share/mas-cli
COPY templates/matrix/mas-start.py /start.py
ENV MAS_CONFIG=/data/config.yaml
ENTRYPOINT ["python", "/start.py"]
