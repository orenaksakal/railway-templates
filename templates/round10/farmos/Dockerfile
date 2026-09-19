FROM farmos/farmos:4.0.6@sha256:500843a3ed35d837d6f3c50a744444f61ce7b3b25bca55375d20f62f0f6a861b
USER root
RUN rm -rf /opt/drupal/web/sites && ln -s /data/sites /opt/drupal/web/sites \
    && mkdir -p /opt/drupal/keys && mv /opt/drupal/keys /opt/farmos-keys \
    && ln -s /data/keys /opt/drupal/keys \
    && printf 'SetEnvIf X-Forwarded-Proto https HTTPS=on\n' > /etc/apache2/conf-enabled/railway.conf
COPY --chmod=755 templates/round10/farmos/start.sh /start.sh
ENTRYPOINT ["/start.sh"]
CMD ["apache2-foreground"]
