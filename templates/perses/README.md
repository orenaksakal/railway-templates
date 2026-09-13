# Deploy and Host Perses Dashboards on Railway

Observability dashboards with persistent storage and owner access.

**Validation scope: static configuration checks only. Image builds and Railway application workflows have not been validated.** Deploying this template incurs Railway usage and any external provider charges.

## About Hosting Perses Dashboards

Two services. Perses runs privately with native auth disabled and every public application route protected by the owner gateway. This is a shared-owner workspace, not per-user RBAC. File database and extracted plugins persist on /data; ENCRYPTION_KEY must remain exactly 32 alphanumeric characters and be preserved with backups. Upstream plugin archives are included. This template does not collect or store metrics itself; supply a datasource. Apache-2.0 upstream license.

## Setup

Open perses using username admin and perses.ACCESS_PASSWORD. Add a project, configure a reachable Prometheus-compatible datasource and create a dashboard. Keep datasource credentials private and use read-only access where possible.

### Deployment Dependencies

| Service | Source | Persistent volume | Public HTTP port |
| --- | --- | --- | --- |
| core | Repository adapter: templates/perses/Dockerfile | /data | Private |
| perses | Repository adapter: shared/round6-gateway/Dockerfile | None | 8080 |

## Operator inputs

| Variable | Requirement |
| --- | --- |
| None | Initial credentials are generated; complete application setup above. |

Generated credentials: `core.ENCRYPTION_KEY`, `perses.ACCESS_PASSWORD`. Never copy another deployment's secrets. Preserve encryption/signing keys with backups.

## Why Deploy Perses Dashboards on Railway

The definition connects private dependencies, declares persistent volumes and exposes the listed application endpoints through Railway HTTPS. Repository adapters build from `codex/fifteen-template-drafts` with the repository root as Docker context. Configure one replica for each stateful service.

## Common Use Cases

Observability dashboards with persistent storage and owner access. Use a separate test project to verify the workflow below before putting real data into the instance.

## Dependencies for Perses Dashboards

Reviewed upstream release: [v0.54.0](https://github.com/perses/perses/tree/4c719fc19fa21d333797e84c4fe7e3d81c25f4f5). Image digests are recorded in `images.round6.lock.json`; source receipts are in `sources.round6.lock.json`. A matching version label does not independently prove image-to-source provenance. Base-image pins do not lock later apt/apk or language-package resolution.

## Recommended acceptance checks

Build and extract the packaged plugins; reject anonymous requests; create a datasource and query real metrics; save/reload a dashboard; verify plugin assets load; restart with encrypted datasource credentials intact; restore /data with the same encryption key.

## Operations and recovery

Back up every listed persistent volume and export every application database, preserving the generated encryption/signing secrets. Restore into a separate test instance and repeat the functional workflow before relying on the backup. Keep internal databases private. An owner gateway `/healthz` response proves only that gateway is alive, not that its application or dependencies are ready. After changing a public domain, update all application origin and callback settings. Review upstream migrations before upgrading; record the old source/image pins and a recoverable backup. No scheduled backup service is configured by this draft.

## Validation status

The checked-in catalog supports static pin, reference, Docker COPY-path and script-syntax validation. Container builds, native proxy behavior, fresh Railway deployment, provider integrations, persistence and restore remain release gates. See `RELEASES-ROUND-6.md` for the publication record.
