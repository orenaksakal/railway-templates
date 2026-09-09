# FastGPT Core + RAG

FastGPT chat and RAG with MongoDB, pgvector, Redis and object storage.

**Deployment template.** Deployment incurs Railway charges. Supply your own required model, search and external-service credentials; no example provider credentials are included.

## Live verification — 2026-09-08

All nine services started. MongoDB replica became primary. Public web route and root password login passed. Model-backed chat, RAG quality, restore and external sandbox execution were not tested; the Docker-socket agent sandbox is excluded.

## Setup

Log in as root with fastgpt.DEFAULT_ROOT_PSW. Configure your model provider and embedding model in FastGPT before ingesting documents. Keep all generated encryption keys and MongoDB replica identity with your backups.

### Deployment Dependencies

| Service | Source | Persistent volume | Public HTTP |
|---|---|---|---|
| vector | pgvector/pgvector:0.8.0-pg15 (digest pinned) | /var/lib/postgresql/data | Private only |
| mongo | repository adapter: templates/fastgpt/Mongo.Dockerfile | /data | Private only |
| redis | redis:7.4 (digest pinned) | /data | Private only |
| storage | repository adapter: shared/round4-storage/Dockerfile | /data | Private only |
| aiproxy-db | postgres:15 (digest pinned) | /var/lib/postgresql/data | Private only |
| fastgpt | ghcr.io/labring/fastgpt:v4.16.2 (digest pinned) | None | 3000 |
| plugin | ghcr.io/labring/fastgpt-plugin:v1.1.2 (digest pinned) | None | Private only |
| code-sandbox | ghcr.io/labring/fastgpt-code-sandbox:v4.16.0 (digest pinned) | None | Private only |
| aiproxy | ghcr.io/labring/aiproxy:v0.6.5 (digest pinned) | None | Private only |

## Required inputs

No external secrets are required for initial configuration. Follow the setup instructions for application-level onboarding.

Generated credentials: `vector.POSTGRES_PASSWORD`, `mongo.MONGO_INITDB_ROOT_PASSWORD`, `redis.REDIS_PASSWORD`, `storage.MINIO_ROOT_USER`, `storage.MINIO_ROOT_PASSWORD`, `aiproxy-db.POSTGRES_PASSWORD`, `fastgpt.ROOT_KEY`, `fastgpt.DEFAULT_ROOT_PSW`, `fastgpt.FILE_TOKEN_KEY`, `fastgpt.AES256_SECRET_KEY`, `fastgpt.INVOKE_TOKEN_SECRET`, `fastgpt.PLUGIN_TOKEN`, `fastgpt.CODE_SANDBOX_TOKEN`, `fastgpt.AIPROXY_API_TOKEN`. Keep them private and preserve relevant encryption keys with backups. Every editor variable includes a description.

## Scope and limitations

Nine services. Full OpenSandbox agent execution, agent previews and Docker volume management are excluded: those upstream services require a Docker socket. The separate workflow code sandbox is included. Confirm the current UI handles unavailable agent features clearly. Both S3 buckets start private; confirm signed/proxied downloads and intended public assets.

## Recommended acceptance checks

Build and first boot; root login; model-provider configuration; document upload and retrieval; workflow execution; authenticated replica recovery; object downloads; restart and restore. Verify MongoDB 5 lifecycle/support before release.

## Operations

Keep database and internal service endpoints private. Railway provides HTTPS for the explicitly exposed HTTP services. Back up the listed persistent volumes and database exports, preserve encryption keys, and test a restore before relying on this instance. Review upstream migrations before upgrades. Single-volume services use one replica; no multi-region or high-availability guarantee is made. A gateway health response only proves the gateway is alive.

## Sources

- [Upstream project](https://github.com/labring/FastGPT)
- [Reviewed source snapshot](https://github.com/labring/FastGPT/tree/0058e223edfcb1035b437cadb9370462b562f685)
- Image digest pins: `images.round4.lock.json` in the template source repository. Source snapshots are research references; image digests do not prove the image was built from that same commit.
- Base-image pins do not lock every package installed by apt/apk/pip. See the verification scope above before relying on this deployment.
