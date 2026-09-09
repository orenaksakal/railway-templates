# Deploy and Host OpenRAG CPU Stack on Railway

RAG workspace with OpenSearch, Langflow and CPU document processing.

**Deployment template.** Deployment incurs Railway charges. Supply your own required model, search and external-service credentials; no example provider credentials are included.

## About Hosting OpenRAG CPU Stack

This template provisions 6 services in one Railway project, with image digests or upstream source revisions pinned, generated internal credentials, linked environment variables and the persistent paths listed below. Public HTTP routes use Railway HTTPS. SQL and internal dependency endpoints stay private. Keep stateful services single-replica and configure your own backup policy.

## Live verification — 2026-09-08

All six services built and started. OpenSearch connection, Langflow authentication/key creation, global-variable initialization, backend health, public UI and gateway authentication passed. Model-backed ingestion/chat, optional connectors, flow-edit synchronization and restore were not tested.

## Setup

Enter OPENAI_API_KEY. OPENRAG_ENCRYPTION_KEY is generated for the upstream AES-256-GCM key derivation; preserve it with backups. Open the openrag gateway with its generated access credentials. Langflow has its own generated admin password, automatic login disabled and a separate authenticated public domain.

## Dependencies for OpenRAG CPU Stack Hosting

### Deployment Dependencies

| Service | Source | Persistent volume | Public HTTP |
|---|---|---|---|
| opensearch | repository adapter: templates/openrag/OpenSearch.Dockerfile | /usr/share/opensearch/data | Private only |
| backend | repository adapter: templates/openrag/Dockerfile | /data | Private only |
| langflow | repository adapter: templates/openrag/Langflow.Dockerfile | /app/langflow-data | 7860 |
| frontend | langflowai/openrag-frontend:0.7.1 (digest pinned) | None | Private only |
| docling | ghcr.io/docling-project/docling-serve-cpu:latest (digest pinned) | /data | Private only |
| openrag | repository adapter: shared/round4-gateway/Dockerfile | None | 8080 |

## Required inputs

`backend.OPENAI_API_KEY`

Generated credentials: `opensearch.OPENSEARCH_INITIAL_ADMIN_PASSWORD`, `backend.LANGFLOW_SUPERUSER_PASSWORD`, `backend.SESSION_SECRET`, `backend.OPENRAG_ENCRYPTION_KEY`, `langflow.LANGFLOW_SECRET_KEY`, `openrag.ACCESS_PASSWORD`. Keep them private and preserve relevant encryption keys with backups. Every editor variable includes a description.

## Scope and limitations

Six services. Backend directories are seeded into one volume; Langflow has its own database volume and image-provided flows. Railway volumes are not shared: verify API flow import and subsequent edits remain consistent across the two services. CPU Docling uses persistent model cache. No GPU, Azure emulator, OpenSearch dashboard or privileged Instana host agent is included. Some optional connectors need additional OAuth credentials. Upstream startup may run its own migrations; review these before upgrades.

## Recommended acceptance checks

All image builds and permissions; OpenSearch bootstrap/JWKS; authentication; Langflow key creation and flow import; document ingestion and chat; Docling model download; encryption recovery; saved connections and flows after restart; backup and restore.

## Operations

Keep database and internal service endpoints private. Railway provides HTTPS for the explicitly exposed HTTP services. Back up the listed persistent volumes and database exports, preserve encryption keys, and test a restore before relying on this instance. Review upstream migrations before upgrades. Single-volume services use one replica; no multi-region or high-availability guarantee is made. A gateway health response only proves the gateway is alive.

## Sources

- [Upstream project](https://github.com/langflow-ai/openrag)
- [Reviewed source snapshot](https://github.com/langflow-ai/openrag/tree/1e228bb0ef7e45959f241a6f3163fb2182303785)
- Image digest pins: `images.round4.lock.json` in the template source repository. Source snapshots are research references; image digests do not prove the image was built from that same commit.
- Base-image pins do not lock every package installed by apt/apk/pip. See the verification scope above before relying on this deployment.

## Common Use Cases

- Set up a document retrieval workspace with your own model credentials.
- Experiment with Langflow-based ingestion and chat over indexed documents.

## Why Deploy OpenRAG CPU Stack on Railway?

Railway groups service deployment, logs, private networking, generated environment references and persistent volumes in one project. This community template supplies the configuration and setup notes; Railway resource charges and external provider costs remain separate. No fixed cost or capacity guarantee is made.
