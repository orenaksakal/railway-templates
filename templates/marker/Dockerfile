FROM python:3.12-slim@sha256:78387bc3881b8273120a12ebe6c1ab22b018ccc2c9adf565ae1ac9b536e184ea
RUN apt-get update && apt-get install -y --no-install-recommends git libgl1 libglib2.0-0 && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir torch==2.10.0 torchvision==0.25.0 --index-url https://download.pytorch.org/whl/cpu
RUN pip install --no-cache-dir 'marker-pdf @ git+https://github.com/datalab-to/marker.git@36b3947d05b16787937fc77db47422c9a6bc0e29' fastapi uvicorn python-multipart
ENV HF_HOME=/data/huggingface XDG_CACHE_HOME=/data/cache TORCH_DEVICE=cpu
WORKDIR /app
COPY templates/marker/main.py /app/main.py
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]
