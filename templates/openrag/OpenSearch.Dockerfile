FROM langflowai/openrag-opensearch:0.7.1@sha256:e63b97ec056022048229befdb7a13a487c006efdca2dc9e2a5ff3884c945e2ba
USER root
COPY --chmod=755 templates/openrag/search-start.sh /railway-search-start.sh
ENTRYPOINT ["/railway-search-start.sh"]
