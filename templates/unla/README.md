# Deploy and Host Unla MCP Gateway on Railway

MCP gateway and management UI with persistent SQLite and owner access.

**Validation scope: static configuration checks only. Image builds and Railway application workflows have not been validated.** Deploying this template incurs Railway usage and any external provider charges.

## About Hosting Unla MCP Gateway

Two services. The pinned all-in-one image runs UI, API and MCP gateway; SQLite persists at /app/data/unla.db. The whole public origin is owner-protected. The inner proxy forwards streaming responses and WebSocket upgrades. Remote clients must support the additional header; a bare URL will not bypass the owner gate. OAuth/session behavior follows upstream defaults and must be verified across restarts; this is not a multi-replica topology. MIT upstream license.

## Setup

Open unla using gateway username admin and unla.ACCESS_PASSWORD. Sign into the application using core.SUPER_ADMIN_USERNAME and SUPER_ADMIN_PASSWORD. Register a harmless remote HTTP tool and connect an MCP client. Clients send X-Template-Key with the gateway password alongside any native Authorization credential.

### Deployment Dependencies

| Service | Source | Persistent volume | Public HTTP port |
| --- | --- | --- | --- |
| core | Repository adapter: templates/unla/Dockerfile | /app/data | Private |
| unla | Repository adapter: shared/round6-gateway/Dockerfile | None | 8080 |

## Operator inputs

| Variable | Requirement |
| --- | --- |
| None | Initial credentials are generated; complete application setup above. |

Generated credentials: `core.SUPER_ADMIN_PASSWORD`, `core.APISERVER_JWT_SECRET_KEY`, `unla.ACCESS_PASSWORD`. Never copy another deployment's secrets. Preserve encryption/signing keys with backups.

## Why Deploy Unla MCP Gateway on Railway

The definition connects private dependencies, declares persistent volumes and exposes the listed application endpoints through Railway HTTPS. Repository adapters build from `codex/fifteen-template-drafts` with the repository root as Docker context. Configure one replica for each stateful service.

## Common Use Cases

MCP gateway and management UI with persistent SQLite and owner access. Use a separate test project to verify the workflow below before putting real data into the instance.

## Dependencies for Unla MCP Gateway

Reviewed upstream release: [v0.10.0](https://github.com/AmoyLab/Unla/tree/5da380b8d883165def1c0a19ec55025ef12db8a5). Image digests are recorded in `images.round6.lock.json`; source receipts are in `sources.round6.lock.json`. A matching version label does not independently prove image-to-source provenance. Base-image pins do not lock later apt/apk or language-package resolution.

## Recommended acceptance checks

Build; verify both gateway and application login; register and invoke an HTTP-backed tool; exercise SSE/streamable HTTP and WebSocket paths; reject missing/incorrect owner keys; verify native Bearer auth passes through; restart and verify gateway configuration and session behavior; restore SQLite.

## Operations and recovery

Back up every listed persistent volume and export every application database, preserving the generated encryption/signing secrets. Restore into a separate test instance and repeat the functional workflow before relying on the backup. Keep internal databases private. An owner gateway `/healthz` response proves only that gateway is alive, not that its application or dependencies are ready. After changing a public domain, update all application origin and callback settings. Review upstream migrations before upgrading; record the old source/image pins and a recoverable backup. No scheduled backup service is configured by this draft.

## Validation status

The checked-in catalog supports static pin, reference, Docker COPY-path and script-syntax validation. Container builds, native proxy behavior, fresh Railway deployment, provider integrations, persistence and restore remain release gates. See `RELEASES-ROUND-6.md` for the publication record.
