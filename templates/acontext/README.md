# Deploy and Host Acontext Agent Context Platform on Railway

Agent context management with sessions, queues and object storage.

**Deployment template.** Deployment incurs Railway charges. Supply your own required model, search and external-service credentials; no example provider credentials are included.

## About Hosting Acontext Agent Context Platform

This template provisions 9 services in one Railway project, with image digests or upstream source revisions pinned, generated internal credentials, linked environment variables and the persistent paths listed below. Public HTTP routes use Railway HTTPS. SQL and internal dependency endpoints stay private. Keep stateful services single-replica and configure your own backup policy.

## Live verification — 2026-09-08

All nine services started. Core database/queue initialization, API health, authenticated session create/list, public UI and gateway authentication passed. Provider-backed processing, external Cloudflare sandbox execution, full UI administration, signed assets and restore were not tested.

## Setup

Enter core.LLM_API_KEY and core.CLOUDFLARE_WORKER_URL for an existing Acontext sandbox Worker. Worker deployment is a separate prerequisite. Open acontext with the gateway access credentials. Create/select a project in the dashboard and use its project API key for API clients. ROOT_API_BEARER_TOKEN is an internal administrative credential; never put it into browser code.

## Dependencies for Acontext Agent Context Platform Hosting

### Deployment Dependencies

| Service | Source | Persistent volume | Public HTTP |
|---|---|---|---|
| postgres | pgvector/pgvector:pg16 (digest pinned) | /var/lib/postgresql/data | Private only |
| redis | redis:7.4 (digest pinned) | /data | Private only |
| rabbitmq | rabbitmq:4-management (digest pinned) | /var/lib/rabbitmq | Private only |
| storage | repository adapter: shared/round4-storage/Dockerfile | /data | 9000 |
| jaeger | jaegertracing/all-in-one:1.75.0 (digest pinned) | None | Private only |
| core | repository adapter: templates/acontext/Core.Dockerfile | None | Private only |
| api | ghcr.io/memodb-io/acontext-api:latest (digest pinned) | None | 8029 |
| ui | ghcr.io/memodb-io/acontext-ui:latest (digest pinned) | None | Private only |
| acontext | repository adapter: shared/round4-gateway/Dockerfile | None | 8080 |

## Required inputs

`core.LLM_API_KEY`, `core.CLOUDFLARE_WORKER_URL`

Generated credentials: `postgres.POSTGRES_PASSWORD`, `redis.REDIS_PASSWORD`, `rabbitmq.RABBITMQ_DEFAULT_PASS`, `storage.MINIO_ROOT_USER`, `storage.MINIO_ROOT_PASSWORD`, `api.ROOT_API_BEARER_TOKEN`, `api.ROOT_SECRET_PEPPER`, `acontext.ACCESS_PASSWORD`. Keep them private and preserve relevant encryption keys with backups. Every editor variable includes a description.

## Scope and limitations

Nine services. MinIO replaces upstream SeaweedFS for S3-compatible storage; bucket initialization is included. Public S3 endpoint supports signed asset URLs while the core uses the private endpoint. Jaeger is private, memory-only and capped at 10,000 traces; traces are intentionally ephemeral. Core config is an empty mapping so environment variables supply credentials. Sandbox execution cannot work until the external Worker is configured. Validate current UI/API root-token and pepper handling before release.

## Recommended acceptance checks

Clean image builds; DB migrations and vector extension; API auth; context/session lifecycle; worker queue processing; S3 upload and signed download; Cloudflare sandbox execution; UI login; private trace access; persistence and restore.

## Operations

Keep database and internal service endpoints private. Railway provides HTTPS for the explicitly exposed HTTP services. Back up the listed persistent volumes and database exports, preserve encryption keys, and test a restore before relying on this instance. Review upstream migrations before upgrades. Single-volume services use one replica; no multi-region or high-availability guarantee is made. A gateway health response only proves the gateway is alive.

## Sources

- [Upstream project](https://github.com/memodb-io/Acontext)
- [Reviewed source snapshot](https://github.com/memodb-io/Acontext/tree/259d73bfdebeed35ec2d4211ddc060a2d4126bc6)
- Image digest pins: `images.round4.lock.json` in the template source repository. Source snapshots are research references; image digests do not prove the image was built from that same commit.
- Base-image pins do not lock every package installed by apt/apk/pip. See the verification scope above before relying on this deployment.

## Common Use Cases

- Store agent sessions and manage context through the Acontext API.
- Connect your own model provider and external sandbox Worker to context processing.

## Why Deploy Acontext Agent Context Platform on Railway?

Railway groups service deployment, logs, private networking, generated environment references and persistent volumes in one project. This community template supplies the configuration and setup notes; Railway resource charges and external provider costs remain separate. No fixed cost or capacity guarantee is made.
