FROM postgres:17-alpine@sha256:18cfe3ef5e6815560c98237d6216d1e5119702fb0f3894c8785dd58b8bbe5d73
COPY --chmod=755 templates/agenta/init-databases.sh /docker-entrypoint-initdb.d/10-agenta.sh
