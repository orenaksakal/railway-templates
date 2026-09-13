# Deploy and Host Vespa Search Starter on Railway

Single-node search with a starter document schema and protected API.

**Unpublished draft. Image builds and Railway application workflows have not been validated.** The template defines services; saving a draft creates no running application. Deploying it later incurs Railway usage and any external provider charges.

## About Hosting Vespa Search Starter

Two services: one Vespa node and an owner gateway. Data persists at /opt/vespa/var. The starter package is deployed only once; a marker prevents redeploys from overwriting an operator schema. This is a single-node example with no replication or high availability. Allocate sufficient memory/CPU for Vespa and measure it; no low-cost monthly estimate is provided. Runtime startup, hostname mapping and application activation still require verification. Apache-2.0 upstream license.

## Setup

Open the vespa endpoint using username admin and vespa.ACCESS_PASSWORD, or send X-Template-Key for API calls. The first boot installs the included title/body search schema. Feed a document of type document to /document/v1/default/document/docid/ID and query /search/. The configuration API on port 19071 stays private; deploy schema changes from within the project.

### Deployment Dependencies

| Service | Source | Persistent volume | Public HTTP port |
| --- | --- | --- | --- |
| core | Repository adapter: templates/vespa/Dockerfile | /opt/vespa/var | Private |
| vespa | Repository adapter: shared/round6-gateway/Dockerfile | None | 8080 |

## Operator inputs

| Variable | Requirement |
| --- | --- |
| None | Initial credentials are generated; complete application setup above. |

Generated credentials: `vespa.ACCESS_PASSWORD`. Never copy another deployment's secrets. Preserve encryption/signing keys with backups.

## Why Deploy Vespa Search Starter on Railway

The definition connects private dependencies, declares persistent volumes and exposes the listed application endpoints through Railway HTTPS. Repository adapters build from `codex/fifteen-template-drafts` with the repository root as Docker context. Configure one replica for each stateful service.

## Common Use Cases

Single-node search with a starter document schema and protected API. Use a separate test project to verify the workflow below before putting real data into the instance.

## Dependencies for Vespa Search Starter

Reviewed upstream release: [v8.751.13](https://github.com/vespa-engine/vespa/tree/40f6d816139431d1203e69dfaffbb9bd1af4fe53). Image digests are recorded in `images.round6.lock.json`; source receipts are in `sources.round6.lock.json`. A matching version label does not independently prove image-to-source provenance. Base-image pins do not lock later apt/apk or language-package resolution.

## Recommended acceptance checks

Build; wait for configuration health and starter activation; reject anonymous feed/query operations; feed a title/body document and retrieve it; run a BM25 query; restart and verify data; deploy an intentional schema revision privately; confirm redeploy does not reset it; test backup and restore.

## Operations and recovery

Back up every listed persistent volume and export every application database, preserving the generated encryption/signing secrets. Restore into a separate test instance and repeat the functional workflow before relying on the backup. Keep internal databases private. An owner gateway `/healthz` response proves only that gateway is alive, not that its application or dependencies are ready. After changing a public domain, update all application origin and callback settings. Review upstream migrations before upgrading; record the old source/image pins and a recoverable backup. No scheduled backup service is configured by this draft.

## Validation status

The checked-in catalog supports static pin, reference, Docker COPY-path and script-syntax validation. Container builds, native proxy behavior, fresh Railway deployment, provider integrations, persistence and restore remain release gates. See `DRAFTS-ROUND-6.md` for the batch record.
