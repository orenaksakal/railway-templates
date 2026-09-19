FROM errbit/errbit:0.11.5@sha256:e8352bd84af1e86d4b28a5c788a460b9b216b180d3a46867051e9d6252325cec
COPY templates/round9/errbit/bootstrap.rb /railway-bootstrap.rb

COPY shared/round9-bootstrap/seed.sh /seed.sh
COPY --chmod=755 templates/round9/errbit/start.sh /railway-start.sh
ENTRYPOINT ["/railway-start.sh"]
