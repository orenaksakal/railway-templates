ARG POSTGRES_IMAGE=postgres:16
FROM ${POSTGRES_IMAGE}
COPY --chmod=755 shared/postgres/init.sh /docker-entrypoint-initdb.d/10-app.sh
