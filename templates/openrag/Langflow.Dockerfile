FROM langflowai/openrag-langflow:0.7.1@sha256:6824cdc6fa89b9dfecf18c29c333c46695e04fccea1b6012e33a76372908d32a
USER root
RUN mkdir -p /app/flows && if [ -f /app/component_index.json ]; then cp /app/component_index.json /app/flows/component_index.json; fi
