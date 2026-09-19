FROM leepeuker/movary:0.72.0@sha256:f5eab178e732d73acf5ec674f8657a6524c73c53bd284e68f13469de21d6fda4
USER root
COPY --chmod=755 templates/round10/movary/start.sh /usr/local/bin/railway-movary.sh
ENTRYPOINT ["/usr/local/bin/railway-movary.sh"]
