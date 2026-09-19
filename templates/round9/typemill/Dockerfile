FROM kixote/typemill:v2.26.2@sha256:4e9dff1795190fb3f09fc9e967643a030a0b8ee51e5e57aff086c270976ada07 AS upstream
FROM scratch
COPY --from=upstream / /
ENV PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
ENV PHPIZE_DEPS="autoconf \t\tdpkg-dev \t\tfile \t\tg++ \t\tgcc \t\tlibc-dev \t\tmake \t\tpkg-config \t\tre2c"
ENV PHP_INI_DIR="/usr/local/etc/php"
ENV APACHE_CONFDIR="/etc/apache2"
ENV APACHE_ENVVARS="/etc/apache2/envvars"
ENV PHP_CFLAGS="-fstack-protector-strong -fpic -fpie -O2 -D_LARGEFILE_SOURCE -D_FILE_OFFSET_BITS=64"
ENV PHP_CPPFLAGS="-fstack-protector-strong -fpic -fpie -O2 -D_LARGEFILE_SOURCE -D_FILE_OFFSET_BITS=64"
ENV PHP_LDFLAGS="-Wl,-O1 -pie"
ENV GPG_KEYS="1198C0117593497A5EC5C199286AF1F9897469DC 49D9AF6BC72A80D6691719C8AA23F5BE9C7097D4 D95C03BC702BE9515344AE3374E44BC9067701A5"
ENV PHP_VERSION="8.5.9"
ENV PHP_URL="https://www.php.net/distributions/php-8.5.9.tar.xz"
ENV PHP_ASC_URL="https://www.php.net/distributions/php-8.5.9.tar.xz.asc"
ENV PHP_SHA256="0db7855f25bcd0ab1d592cdb35e284d6f6a5d2ae0f6f621122e364cc39b708f4"
ENV TYPEMILL_PROXY_DETECTION="true"
WORKDIR /var/www/html
RUN mkdir -p /seed && for directory in settings media cache plugins data content themes; do cp -a "/var/www/html/$directory" "/seed/$directory"; rm -rf "/var/www/html/$directory"; ln -s "/data/$directory" "/var/www/html/$directory"; done

COPY shared/round9-bootstrap/seed.sh /seed.sh
COPY --chmod=755 templates/round9/typemill/start.sh /railway-start.sh
ENTRYPOINT ["/railway-start.sh"]
