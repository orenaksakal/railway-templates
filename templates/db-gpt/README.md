# Deploy and Host DB-GPT Data Assistant on Railway

Private AI data assistant with persistent metadata and vector storage.

**Validation scope: static configuration checks only. Image builds and Railway application workflows have not been validated.** Deploying this template incurs Railway usage and any external provider charges.

## About Hosting DB-GPT Data Assistant

Two services: DB-GPT and an owner gateway. SQLite metadata, Chroma vectors, uploaded data and model caches persist below /data. This is a trusted-owner CPU deployment using external LLM/embedding APIs; GPU inference, a Docker socket and a separate execution sandbox are not provisioned. Generated ENCRYPTION_KEY must survive recovery. Provider fees are separate. MIT upstream license. Extra database connectors may need additional drivers; arbitrary connector coverage is not claimed.

## Setup

Enter core.OPENAI_API_KEY. Set OPENAI_API_BASE, LLM_MODEL_NAME and embedding settings if using a compatible provider. Open db-gpt with username admin and db-gpt.ACCESS_PASSWORD. Add a small test dataset and a database connection with narrowly scoped read permissions.

### Deployment Dependencies

| Service | Source | Persistent volume | Public HTTP port |
| --- | --- | --- | --- |
| core | Repository adapter: templates/db-gpt/Dockerfile | /data | Private |
| db-gpt | Repository adapter: shared/round6-gateway/Dockerfile | None | 8080 |

## Operator inputs

| Variable | Requirement |
| --- | --- |
| `core.OPENAI_API_KEY` | Required. Required model-provider API key. Provider charges are separate from Railway. |

Generated credentials: `core.ENCRYPTION_KEY`, `db-gpt.ACCESS_PASSWORD`. Never copy another deployment's secrets. Preserve encryption/signing keys with backups.

## Why Deploy DB-GPT Data Assistant on Railway

The definition connects private dependencies, declares persistent volumes and exposes the listed application endpoints through Railway HTTPS. Repository adapters build from `codex/fifteen-template-drafts` with the repository root as Docker context. Configure one replica for each stateful service.

## Common Use Cases

Private AI data assistant with persistent metadata and vector storage. Use a separate test project to verify the workflow below before putting real data into the instance.

## Dependencies for DB-GPT Data Assistant

Reviewed upstream release: [v0.8.2](https://github.com/eosphoros-ai/DB-GPT/tree/83609c471266607490b24e72188311efa23a0d16). Image digests are recorded in `images.round6.lock.json`; source receipts are in `sources.round6.lock.json`. A matching version label does not independently prove image-to-source provenance. Base-image pins do not lock later apt/apk or language-package resolution.

## Recommended acceptance checks

Build; reject anonymous UI/API access; use an actual model request; upload and retrieve a document; ask a query against a disposable read-only database; verify SQL review behavior and connector support; confirm persistent metadata and vectors after restart; back up and restore /data and ENCRYPTION_KEY.

## Operations and recovery

Back up every listed persistent volume and export every application database, preserving the generated encryption/signing secrets. Restore into a separate test instance and repeat the functional workflow before relying on the backup. Keep internal databases private. An owner gateway `/healthz` response proves only that gateway is alive, not that its application or dependencies are ready. After changing a public domain, update all application origin and callback settings. Review upstream migrations before upgrading; record the old source/image pins and a recoverable backup. No scheduled backup service is configured by this draft.

## Validation status

The checked-in catalog supports static pin, reference, Docker COPY-path and script-syntax validation. Container builds, native proxy behavior, fresh Railway deployment, provider integrations, persistence and restore remain release gates. See `RELEASES-ROUND-6.md` for the publication record.
