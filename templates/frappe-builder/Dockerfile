FROM ghcr.io/frappe/crm:v1.83.0@sha256:d32697412d4ccd3b7042a8d757000375a1daa6be76347a267d5261a1809eab3b
USER frappe
WORKDIR /home/frappe/frappe-bench
ENV FRAPPE_APP=builder TEMPLATE_RELEASE=v1.34.0
RUN git clone --no-checkout https://github.com/frappe/builder.git apps/builder \
    && git -C apps/builder checkout 09c3effa10926e736a87d80f68880d81f498fbe2 \
    && ls -1 apps > sites/apps.txt \
    && bench setup requirements \
    && bench build --production \
    && env/bin/python -c "import builder" \
    && cp -a sites /home/frappe/sites-template
USER root
COPY shared/round6-frappe/start.py /opt/railway/start.py
COPY shared/round6-frappe/nginx.conf /opt/railway/nginx.conf
COPY --chmod=755 shared/round6-frappe/entrypoint.sh /opt/railway/entrypoint.sh
RUN mkdir -p /logs && chown frappe:frappe /logs \
    && rm -rf /home/frappe/frappe-bench/sites \
    && ln -s /data /home/frappe/frappe-bench/sites
EXPOSE 8080
ENTRYPOINT ["/opt/railway/entrypoint.sh"]
