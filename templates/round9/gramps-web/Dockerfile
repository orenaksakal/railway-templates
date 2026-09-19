FROM ghcr.io/gramps-project/grampsweb:26.9.0@sha256:054b0cdf8003f1ae531ff7981a03ce374c3b13030ecc7ed38fc7f24be5b7acb2
ENV PYTHONPATH=/app/src
COPY --chmod=755 templates/round9/gramps-web/start.sh /railway-start.sh
COPY templates/round9/gramps-web/supervise.py /railway-supervise.py
ENTRYPOINT ["/railway-start.sh"]
