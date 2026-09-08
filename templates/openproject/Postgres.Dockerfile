FROM postgres:17@sha256:67f41722b7a8cbdb868a44a4995c846eddfdc2973bccb291ce937dce88ad5675
COPY --chmod=755 shared/postgres/init.sh /docker-entrypoint-initdb.d/10-app.sh
