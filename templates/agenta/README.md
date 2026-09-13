# Deploy and Host Agenta LLM Engineering on Railway

LLM evaluation and tracing with databases, workers and object storage.

**Unpublished draft. Image builds and Railway application workflows have not been validated.** The template defines services; saving a draft creates no running application. Deploying it later incurs Railway usage and any external provider charges.

## About Hosting Agenta LLM Engineering

Thirteen services adapted from the upstream Railway OSS layout: PostgreSQL, Redis, SeaweedFS 4.37, web/mobile, API/services/runner, two workers, cron, Supertokens and gateway. API migrations gate background startup, and its signing key persists on /data. SeaweedFS is pinned to the upstream-required STS-compatible version. Runner execution uses external Daytona; host Docker/FUSE is unavailable. No model or sandbox credits, enterprise features, HA or fixed hosting cost are included. The OSS code is MIT-licensed; enterprise code has separate terms. This is the largest and highest-validation-effort draft in this batch.

## Setup

Enter runner.AGENTA_RUNNER_DAYTONA_API_KEY for your own Daytona account. Open agenta using gateway username admin and agenta.ACCESS_PASSWORD, then create the application account. Configure a model provider in Agenta. External SDK calls require X-Template-Key with the gateway password in addition to the native API key; confirm your client supports this.

### Deployment Dependencies

| Service | Source | Persistent volume | Public HTTP port |
| --- | --- | --- | --- |
| postgres | Repository adapter: templates/agenta/Postgres.Dockerfile | /var/lib/postgresql/data | Private |
| redis | redis:7.4 | /data | Private |
| seaweedfs | Repository adapter: templates/agenta/Storage.Dockerfile | /data | Private |
| web | ghcr.io/agenta-ai/agenta-web:v0.118.0 | None | Private |
| web-mobile | ghcr.io/agenta-ai/agenta-web-mobile:v0.118.0 | None | Private |
| api | Repository adapter: templates/agenta/Api.Dockerfile | /data | Private |
| services | Repository adapter: templates/agenta/Services.Dockerfile | None | Private |
| runner | ghcr.io/agenta-ai/agenta-runner:v0.118.0 | None | Private |
| worker-streams | Repository adapter: templates/agenta/Api.Dockerfile | None | Private |
| worker-queues | Repository adapter: templates/agenta/Api.Dockerfile | None | Private |
| cron | Repository adapter: templates/agenta/Api.Dockerfile | None | Private |
| supertokens | supertokens/supertokens-postgresql:11 | None | Private |
| agenta | Repository adapter: templates/agenta/Gateway.Dockerfile | None | 8080 |

## Operator inputs

| Variable | Requirement |
| --- | --- |
| `runner.AGENTA_RUNNER_DAYTONA_API_KEY` | Required. Required operator-owned Daytona key. Agent execution uses a separate sandbox service; no host Docker socket or FUSE device is provisioned. |
| `runner.AGENTA_RUNNER_DAYTONA_SNAPSHOT` | Optional. Optional Daytona snapshot name for the chosen runtime. |
| `runner.AGENTA_RUNNER_DAYTONA_TARGET` | Optional. Optional Daytona target region. |

Generated credentials: `postgres.POSTGRES_PASSWORD`, `redis.REDIS_PASSWORD`, `api.AGENTA_AUTH_KEY`, `api.AGENTA_CRYPT_KEY`, `api.AGENTA_SERVICES_INTERNAL_KEY`, `api.AGENTA_RUNNER_TOKEN`, `api.AGENTA_STORE_ACCESS_KEY`, `api.AGENTA_STORE_SECRET_KEY`, `api.AGENTA_STORE_SIGNING_KEY`, `agenta.ACCESS_PASSWORD`. Never copy another deployment's secrets. Preserve encryption/signing keys with backups.

## Why Deploy Agenta LLM Engineering on Railway

The definition connects private dependencies, declares persistent volumes and exposes the listed application endpoints through Railway HTTPS. Repository adapters build from `codex/fifteen-template-drafts` with the repository root as Docker context. Configure one replica for each stateful service.

## Common Use Cases

LLM evaluation and tracing with databases, workers and object storage. Use a separate test project to verify the workflow below before putting real data into the instance.

## Dependencies for Agenta LLM Engineering

Reviewed upstream release: [v0.118.0](https://github.com/Agenta-AI/agenta/tree/dd55885f1d21b03c4c43a61a4df358efd743fdc6). Image digests are recorded in `images.round6.lock.json`; source receipts are in `sources.round6.lock.json`. A matching version label does not independently prove image-to-source provenance. Base-image pins do not lock later apt/apk or language-package resolution.

## Recommended acceptance checks

Build adapters; initialize all three databases; run core/tracing migrations; verify worker readiness; sign up and sign in through Supertokens; evaluate a prompt; ingest and view a trace; save and retrieve a stored artifact via STS; run a small Daytona task; verify native API auth plus owner header; restart all roles; restore databases, SeaweedFS and signing/encryption keys together.

## Operations and recovery

Back up every listed persistent volume and export every application database, preserving the generated encryption/signing secrets. Restore into a separate test instance and repeat the functional workflow before relying on the backup. Keep internal databases private. An owner gateway `/healthz` response proves only that gateway is alive, not that its application or dependencies are ready. After changing a public domain, update all application origin and callback settings. Review upstream migrations before upgrading; record the old source/image pins and a recoverable backup. No scheduled backup service is configured by this draft.

## Validation status

The checked-in catalog supports static pin, reference, Docker COPY-path and script-syntax validation. Container builds, native proxy behavior, fresh Railway deployment, provider integrations, persistence and restore remain release gates. See `DRAFTS-ROUND-6.md` for the batch record.
