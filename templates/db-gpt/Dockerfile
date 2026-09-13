FROM eosphorosai/dbgpt-openai:v0.8.2@sha256:bd7d35ce7994f0f977007c28c839fffcdc80cfa810fa12ead9aecfd4e9b3d11f
COPY templates/db-gpt/config.toml /opt/railway/config.toml
COPY templates/db-gpt/start.py /opt/railway/start.py
ENTRYPOINT ["python", "/opt/railway/start.py"]
