# Round 4 template releases

Published 2026-09-08. All ten Railway listings report `PUBLISHED`; their public pages returned HTTP 200 and contained the expected template names. Saved configurations and listing README content matched local source after publication.

The twelve required external inputs have no default values. Deployers supply their own model/search credentials and Acontext Worker URL. Internal passwords and keys are generated per deployment; no example provider credentials are embedded.

| Template | Services | Public listing |
|---|---:|---|
| FastGPT Core + RAG | 9 | [Deploy](https://railway.com/deploy/fastgpt-core-rag) |
| Dolt SQL Server | 1 | [Deploy](https://railway.com/deploy/dolt-sql-server) |
| Xberg / Kreuzberg Document API | 2 | [Deploy](https://railway.com/deploy/xberg-kreuzberg-document-api) |
| AgentScope Service API | 3 | [Deploy](https://railway.com/deploy/agentscope-service-api) |
| Coze Studio | 11 | [Deploy](https://railway.com/deploy/coze-studio) |
| BettaFish Research Reports | 3 | [Deploy](https://railway.com/deploy/bettafish-research-reports) |
| OpenRAG CPU Stack | 6 | [Deploy](https://railway.com/deploy/openrag-cpu-stack) |
| Marker PDF to Markdown API | 2 | [Deploy](https://railway.com/deploy/marker-pdf-to-markdown-api) |
| Acontext Agent Context Platform | 9 | [Deploy](https://railway.com/deploy/acontext-agent-context-platform) |
| OceanBase seekdb | 1 | [Deploy](https://railway.com/deploy/oceanbase-seekdb) |

## Verification scope

47-service static validation and 10 Python tests passed. The running stacks exposed startup, port, volume, resource-sizing and cryptographic-key issues that were fixed before publication. Runtime evidence is scoped below; provider-backed end-to-end workflows were not exercised with sample credentials.

### FastGPT Core + RAG

All nine services started. MongoDB replica became primary. Public web route and root password login passed. Model-backed chat, RAG quality, restore and external sandbox execution were not tested; the Docker-socket agent sandbox is excluded.

### Dolt SQL Server

Authenticated SQL write, Dolt add/commit, and record/history persistence across service restart passed. SQL remains private. Offsite backup, restore and public TLS were not tested.

### Xberg / Kreuzberg Document API

Public gateway rejected anonymous requests. Authenticated OpenAPI and real PDF extraction passed. MCP transport, optional formats and sustained load were not tested.

### AgentScope Service API

Source build, gateway authentication, agent creation and Redis-backed session creation/listing passed. Model inference was not tested. This is a trusted-owner API service, without the separate upstream UI or a multi-tenant security claim.

### Coze Studio

All eleven services built and started after runtime fixes. etcd committed a health probe. Elasticsearch smartcn/index initialization, Milvus recovery, backend HTTP startup, and gateway authentication passed. Model inference, workflows, OAuth, full schema parity, restore and signed-file behavior were not tested. The documented operator setup remains required.

### BettaFish Research Reports

Container build, PostgreSQL startup, public report UI and gateway authentication passed. Real model/search calls, full report generation, source-data collection and direct Streamlit routing were not tested; deployers supply their own provider credentials and data.

### OpenRAG CPU Stack

All six services built and started. OpenSearch connection, Langflow authentication/key creation, global-variable initialization, backend health, public UI and gateway authentication passed. Model-backed ingestion/chat, optional connectors, flow-edit synchronization and restore were not tested.

### Marker PDF to Markdown API

Source build with compatible CPU Torch/Torchvision, public authentication and real digital-PDF-to-Markdown conversion passed. Unit tests cover temporary-path isolation, cleanup on failure, invalid/oversized file rejection and concurrent-job rejection. OCR is disabled. Scanned PDFs, load capacity and model-license suitability for each deployer were not tested.

### Acontext Agent Context Platform

All nine services started. Core database/queue initialization, API health, authenticated session create/list, public UI and gateway authentication passed. Provider-backed processing, external Cloudflare sandbox execution, full UI administration, signed assets and restore were not tested.

### OceanBase seekdb

Fresh build and startup, public console route, authenticated SQL writes and record persistence across restart passed with 4G database memory and 2G redo allocation. Vector/full-text ranking quality, restore, high availability and public SQL TLS were not tested. SQL remains private.

## Cleanup

All 13 temporary projects created for this release run, including three superseded seekdb attempts, were deleted with their attached service storage. Each recorded project ID was subsequently inaccessible. The temporary Railway SSH key was revoked and its local key files removed. No release-test projects remain.

The fifteen pre-existing listings were independently verified as still published. Existing user projects outside the recorded test IDs were not modified.

Detailed API receipts, public-page checks and cleanup confirmations remain in ignored `.local/round4/`. Public configuration and verification summaries are tracked in `release-validation.round4.json`, the image/source lock files, and each template README.
