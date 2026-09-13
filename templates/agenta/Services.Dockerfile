FROM ghcr.io/agenta-ai/agenta-services:v0.118.0@sha256:e5de8cce8a90ef41f8240bb49c519197406d606b9e07fa3495e203c5572d9213
COPY templates/agenta/start.py /opt/railway/start.py
ENTRYPOINT ["python", "/opt/railway/start.py"]
