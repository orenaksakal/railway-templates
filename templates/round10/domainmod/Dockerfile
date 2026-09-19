FROM php:8.2-apache@sha256:163407b1ceca31a3a17211e07ca80982438bad31280ba18093b185d93a762fd2
RUN apt-get update && apt-get install -y --no-install-recommends cron curl ca-certificates locales \
    && docker-php-ext-install pdo_mysql mysqli gettext \
    && echo 'en_US.UTF-8 UTF-8' > /etc/locale.gen && locale-gen \
    && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL https://codeload.github.com/domainmod/domainmod/tar.gz/9ff9e01070484c0fa519d4c43bf4d9192e081c37 -o /tmp/domainmod.tar.gz \
    && echo '6e407b2fc36d2a9912dd237645f1a0bf46b618957a5ff096693ccb46239cdbd2  /tmp/domainmod.tar.gz' | sha256sum -c - \
    && tar xzf /tmp/domainmod.tar.gz --strip-components=1 -C /var/www/html \
    && rm /tmp/domainmod.tar.gz \
    && mv /var/www/html/temp /opt/domainmod-temp \
    && ln -s /data/temp /var/www/html/temp
COPY templates/round10/domainmod/config.inc.php /var/www/html/_includes/config.inc.php
COPY templates/round10/domainmod/render-config.php /usr/local/bin/domainmod-render-config.php
COPY --chmod=755 templates/round10/domainmod/start.sh /start.sh
RUN printf 'ServerName localhost\nSetEnvIf X-Forwarded-Proto https HTTPS=on\n' > /etc/apache2/conf-enabled/railway.conf \
    && printf '*/10 * * * * root cd /var/www/html && su -s /bin/sh www-data -c "/usr/local/bin/php cron.php" > /proc/1/fd/1 2>/proc/1/fd/2\n' > /etc/cron.d/domainmod \
    && chmod 0644 /etc/cron.d/domainmod \
    && cp /usr/local/etc/php/php.ini-production /usr/local/etc/php/php.ini
ENV LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8
ENTRYPOINT ["/start.sh"]
CMD ["apache2-foreground"]
