FROM sentriz/gonic:v0.22.0@sha256:516fd9645614ba3a596d86174216c3e944808b9ec970c581678713be4c8b1d49 AS upstream
FROM scratch
COPY --from=upstream / /
ENV PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
ENV TZ=""
ENV GONIC_DB_PATH="/data/gonic.db"
ENV GONIC_LISTEN_ADDR=":80"
ENV GONIC_MUSIC_PATH="/music"
ENV GONIC_PODCAST_PATH="/podcasts"
ENV GONIC_CACHE_PATH="/cache"
ENV GONIC_PLAYLISTS_PATH="/playlists"
WORKDIR /

COPY shared/round9-bootstrap/seed.sh /seed.sh
COPY --chmod=755 templates/round9/gonic/start.sh /railway-start.sh
ENTRYPOINT ["/railway-start.sh"]
