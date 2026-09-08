FROM postgres:16@sha256:f1c3376c26f2609ab9f29f71f824103fe2fcd8ee0346485cb6122a4f93df6f94
COPY --chmod=755 shared/postgres/init.sh /docker-entrypoint-initdb.d/10-app.sh
