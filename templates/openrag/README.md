# OpenRAG CPU Stack

OpenRAG with OpenSearch, Langflow, CPU Docling and an authenticated frontend.

**Unpublished draft — not runtime-validated or approved for release.** Saving this template does not deploy services. Deployment later incurs Railway and provider charges.

## Setup

Enter OPENAI_API_KEY and a Fernet OPENRAG_ENCRYPTION_KEY. Generate the latter using cryptography.fernet.Fernet.generate_key().decode() on a trusted machine. Open the openrag gateway with its generated access credentials. Langflow has its own generated admin password, automatic login disabled and a separate authenticated public domain.

### Deployment Dependencies

| Service | Source | Persistent volume | Public HTTP |
|---|---|---|---|
| opensearch | langflowai/openrag-opensearch:0.7.1 (digest pinned) | /usr/share/opensearch/data | Private only |
| backend | repository adapter: templates/openrag/Dockerfile | /data | Private only |
| langflow | repository adapter: templates/openrag/Langflow.Dockerfile | /app/langflow-data | 7860 |
| frontend | langflowai/openrag-frontend:0.7.1 (digest pinned) | None | Private only |
| docling | ghcr.io/docling-project/docling-serve-cpu:latest (digest pinned) | /data | Private only |
| openrag | repository adapter: shared/round4-gateway/Dockerfile | None | 8080 |

## Required inputs

`backend.OPENAI_API_KEY`, `backend.OPENRAG_ENCRYPTION_KEY`

Generated credentials: `opensearch.OPENSEARCH_INITIAL_ADMIN_PASSWORD`, `backend.LANGFLOW_SUPERUSER_PASSWORD`, `backend.SESSION_SECRET`, `langflow.LANGFLOW_SECRET_KEY`, `openrag.ACCESS_PASSWORD`. Keep them private and preserve relevant encryption keys with backups. Every editor variable includes a description.

## Scope and limitations

Six services. Backend directories are seeded into one volume; Langflow has its own database volume and image-provided flows. Railway volumes are not shared: verify API flow import and subsequent edits remain consistent across the two services. CPU Docling uses persistent model cache. No GPU, Azure emulator, OpenSearch dashboard or privileged Instana host agent is included. Some optional connectors need additional OAuth credentials. Upstream startup may run its own migrations; review these before upgrades.

## Release gates

All image builds and permissions; OpenSearch bootstrap/JWKS; authentication; Langflow key creation and flow import; document ingestion and chat; Docling model download; encryption recovery; saved connections and flows after restart; backup and restore.

## Operations

Keep database and internal service endpoints private. Railway provides HTTPS for the explicitly exposed HTTP services. Back up the listed persistent volumes and database exports, preserve encryption keys, and test a restore before relying on this instance. Review upstream migrations before upgrades. Single-volume services use one replica; no multi-region or high-availability guarantee is made. A gateway health response only proves the gateway is alive.

## Sources

- [Upstream project](https://github.com/langflow-ai/openrag)
- [Reviewed source snapshot](https://github.com/langflow-ai/openrag/tree/1e228bb0ef7e45959f241a6f3163fb2182303785)
- Image digest pins: `images.round4.lock.json` in the template source repository. Source snapshots are research references; image digests do not prove the image was built from that same commit.
- Build and runtime verification remain pending. Base-image pins do not lock packages installed by apt/apk/pip.
