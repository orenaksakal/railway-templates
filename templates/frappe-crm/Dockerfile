FROM ghcr.io/frappe/crm:v1.83.0@sha256:d32697412d4ccd3b7042a8d757000375a1daa6be76347a267d5261a1809eab3b
USER frappe
ARG APP_NAME=crm
ARG APP_VERSION=v1.83.0
ARG TELEPHONY_COMMIT=unused
ENV FRAPPE_APP=${APP_NAME} TEMPLATE_RELEASE=${APP_VERSION}
WORKDIR /home/frappe/frappe-bench
# Upstream's tagged image contains the framework only. Install the actual app at build time.
RUN bench set-config -g socketio_port 9000
RUN if [ "$APP_NAME" = helpdesk ]; then \
      test -n "$TELEPHONY_COMMIT" && \
      git clone https://github.com/frappe/telephony.git apps/telephony && \
      git -C apps/telephony checkout "$TELEPHONY_COMMIT" && \
      bench setup requirements --python; \
    fi \
    && bench get-app --branch "$APP_VERSION" "https://github.com/frappe/$APP_NAME.git" \
    && bench build --production \
    && env/bin/python -c "import importlib; importlib.import_module('$APP_NAME')" \
    && test -d "apps/$APP_NAME/$APP_NAME/public" \
    && ls -1 apps > sites/apps.txt \
    && cp -a sites /home/frappe/sites-template
USER root
COPY shared/frappe/start.py /opt/railway/start.py
COPY shared/frappe/nginx.conf /opt/railway/nginx.conf
COPY shared/frappe/entrypoint.sh /opt/railway/entrypoint.sh
RUN mkdir -p /logs && chown frappe:frappe /logs \
    && chmod 755 /opt/railway/entrypoint.sh \
    && rm -rf /home/frappe/frappe-bench/sites \
    && ln -s /data /home/frappe/frappe-bench/sites
EXPOSE 8080
ENTRYPOINT ["/opt/railway/entrypoint.sh"]
