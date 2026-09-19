FROM getpinry/pinry:2.1.13@sha256:9a619749ec5246e04694adc479a135e654a7ac5f34c15d6d134d917a62b4889b
USER root
COPY templates/round10/pinry/local_settings.py /usr/local/share/railway-pinry-settings.py
COPY templates/round10/pinry/start.py /usr/local/bin/railway-pinry.py
RUN sed -i 's|access_log /data/nginx-access.log;|access_log /dev/stdout;|; s|error_log /data/nginx-error.log;|error_log /dev/stderr;|' /etc/nginx/sites-enabled/default
ENTRYPOINT ["python", "/usr/local/bin/railway-pinry.py"]
