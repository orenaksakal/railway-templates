FROM librebooking/librebooking:5.3.0@sha256:a055c211880a178a7eb048f51048bfe23808816623feb94245fe66b9fcc8dd5d
USER root
# Upstream's entrypoint traces expanded DB and installer secrets. Disable xtrace.
RUN sed -i 's/^set -ex$/set -e/' /usr/local/bin/entrypoint.sh \
    && ! grep -q '^set -ex$' /usr/local/bin/entrypoint.sh \
    && cp -a /config /opt/librebooking-config \
    && rm -rf /config && ln -s /data/config /config \
    && cp -a /var/www/html/Web/uploads/images /opt/librebooking-images \
    && rm -rf /var/www/html/Web/uploads/images \
    && ln -s /data/images /var/www/html/Web/uploads/images \
    && printf 'SetEnvIf X-Forwarded-Proto https HTTPS=on\n' > /etc/apache2/conf-enabled/railway.conf
COPY --chmod=755 templates/round10/librebooking/start.sh /start.sh
ENTRYPOINT ["/start.sh"]
CMD ["apache2-foreground"]
