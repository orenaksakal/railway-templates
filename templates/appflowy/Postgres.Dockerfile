FROM pgvector/pgvector:pg16@sha256:ccc6e83d6e35e931dc7c5def2022729d5a6c370318d099181995567ff1fb4d6b
COPY --chmod=755 shared/postgres/init.sh /docker-entrypoint-initdb.d/10-app.sh
COPY templates/appflowy/auth-schema.sql /docker-entrypoint-initdb.d/20-auth.sql
