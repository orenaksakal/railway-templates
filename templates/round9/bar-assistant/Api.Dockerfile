FROM barassistant/server:6.7.0@sha256:286d2f7d52bef72307471deb19d2daf7e0f639ad438693b022f7ebe900065184
USER root
RUN command -v runuser
RUN test -f /etc/entrypoint.d/99-bass.sh && sed -i '/^php artisan key:generate$/d' /etc/entrypoint.d/99-bass.sh && ! grep -q '^php artisan key:generate' /etc/entrypoint.d/99-bass.sh
COPY --chmod=755 templates/round9/bar-assistant/start.sh /railway-start.sh
ENTRYPOINT ["/railway-start.sh"]
CMD ["/init"]
