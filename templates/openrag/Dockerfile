FROM langflowai/openrag-backend:0.7.1@sha256:65ab3d49bbe52178e501b0b472d1e14674777af10ab3efb8782ccb89aa14552e
USER root
RUN mkdir -p /seed && if [ -d /app/openrag-documents ]; then cp -a /app/openrag-documents /seed/openrag-documents; fi && rm -rf /app/openrag-documents && ln -s /data/openrag-documents /app/openrag-documents && if [ -d /app/keys ]; then cp -a /app/keys /seed/keys; fi && rm -rf /app/keys && ln -s /data/keys /app/keys && if [ -d /app/flows ]; then cp -a /app/flows /seed/flows; fi && rm -rf /app/flows && ln -s /data/flows /app/flows && if [ -d /app/config ]; then cp -a /app/config /seed/config; fi && rm -rf /app/config && ln -s /data/config /app/config && if [ -d /app/data ]; then cp -a /app/data /seed/data; fi && rm -rf /app/data && ln -s /data/data /app/data
COPY --chmod=755 templates/openrag/start.sh /railway-start.sh
ENTRYPOINT ["/railway-start.sh"]
CMD ["/app/.venv/bin/python", "src/main.py"]
