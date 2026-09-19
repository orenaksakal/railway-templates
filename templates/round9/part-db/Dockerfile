FROM jbtronics/part-db1:2.17.0@sha256:fd68338829ed3d7850b9ac4dd7429c45c67d440da8e7d3cdd661a04c792f3d79 AS upstream
FROM scratch
COPY --from=upstream / /
ENV PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
ENV APACHE_CONFDIR="/etc/apache2"
ENV APACHE_ENVVARS="/etc/apache2/envvars"
ENV APP_ENV="docker"
ENV DATABASE_URL="sqlite:///%kernel.project_dir%/uploads/app.db"
WORKDIR /var/www/html
RUN mkdir -p /seed && cp -a /var/www/html/uploads /seed/uploads && cp -a /var/www/html/public/media /seed/media && rm -rf /var/www/html/uploads /var/www/html/public/media && ln -s /data/uploads /var/www/html/uploads && ln -s /data/media /var/www/html/public/media

COPY shared/round9-bootstrap/seed.sh /seed.sh
COPY --chmod=755 templates/round9/part-db/start.sh /railway-start.sh
ENTRYPOINT ["/railway-start.sh"]
