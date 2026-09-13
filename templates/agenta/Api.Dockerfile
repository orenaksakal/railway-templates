FROM ghcr.io/agenta-ai/agenta-api:v0.118.0@sha256:e59f93e26692e126d7a3050502fbb798b586d46f3f5c0c3f6e682fe969d727b3
USER root
RUN command -v openssl
COPY templates/agenta/start.py /opt/railway/start.py
ENTRYPOINT ["python", "/opt/railway/start.py"]
