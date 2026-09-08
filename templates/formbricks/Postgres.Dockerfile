FROM pgvector/pgvector:pg18@sha256:2ba9ca5f2e7daa0f0e7723cba1ee9167bab54efd3640516a44ac1a928dd67e7a
COPY --chmod=755 shared/postgres/init.sh /docker-entrypoint-initdb.d/10-app.sh
