FROM bbyars/mountebank:2.9.4@sha256:32c52e77eab3e075c485e1981512ef14fe35fb59f6bc65924b646ad373489139
USER root
COPY --chmod=755 templates/round10/mountebank/start.sh /opt/template/start.sh
ENTRYPOINT ["/opt/template/start.sh"]
