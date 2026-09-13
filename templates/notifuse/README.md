# Deploy and Host Notifuse Email Marketing on Railway

Email campaigns with PostgreSQL and a protected first-run setup.

**Unpublished draft. Image builds and Railway application workflows have not been validated.** The template defines services; saving a draft creates no running application. Deploying it later incurs Railway usage and any external provider charges.

## About Hosting Notifuse Email Marketing

Three services: core, PostgreSQL and gateway. Setup routes are owner-protected; native app authentication protects normal APIs while tracking and provider callbacks remain reachable. PostgreSQL is a dedicated cluster because Notifuse creates workspace databases. v40 uses the upstream Business Source License and the free self-host tier is limited to three workspaces. Paid permissions, SES tenant features, SSO and multilingual variants are not unlocked; NOTIFUSE_LICENSE_KEY is optional and operator supplied.

## Setup

Enter core.ROOT_EMAIL and configure SMTP delivery for login/setup email. Open /setup on the Notifuse domain using username admin and notifuse.ACCESS_PASSWORD. Complete the initial setup for ROOT_EMAIL, create a workspace, and configure its sending provider. SMTP credentials and a verified sender must be yours.

### Deployment Dependencies

| Service | Source | Persistent volume | Public HTTP port |
| --- | --- | --- | --- |
| postgres | postgres:17-alpine | /var/lib/postgresql/data | Private |
| core | notifuse/notifuse:v40.0 | /app/data | Private |
| notifuse | Repository adapter: shared/round6-gateway/Dockerfile | None | 8080 |

## Operator inputs

| Variable | Requirement |
| --- | --- |
| `core.ROOT_EMAIL` | Required. Required operator email. Complete the protected initial setup with this address. |
| `core.SMTP_HOST` | Optional. SMTP server for login/setup email. |
| `core.SMTP_PORT` | Optional. SMTP port, usually 587. |
| `core.SMTP_USERNAME` | Optional. SMTP username. |
| `core.SMTP_PASSWORD` | Optional. SMTP password. |
| `core.SMTP_FROM_EMAIL` | Optional. Verified sender address. |
| `core.NOTIFUSE_LICENSE_KEY` | Optional. Optional paid upstream license; no license is included. |

Generated credentials: `postgres.POSTGRES_PASSWORD`, `core.SECRET_KEY`, `notifuse.ACCESS_PASSWORD`. Never copy another deployment's secrets. Preserve encryption/signing keys with backups.

## Why Deploy Notifuse Email Marketing on Railway

The definition connects private dependencies, declares persistent volumes and exposes the listed application endpoints through Railway HTTPS. Repository adapters build from `codex/fifteen-template-drafts` with the repository root as Docker context. Configure one replica for each stateful service.

## Common Use Cases

Email campaigns with PostgreSQL and a protected first-run setup. Use a separate test project to verify the workflow below before putting real data into the instance.

## Dependencies for Notifuse Email Marketing

Reviewed upstream release: [v40.0](https://github.com/Notifuse/notifuse/tree/dc1d98622ec522d750c24a5cfa65e8cc075d37a9). Image digests are recorded in `images.round6.lock.json`; source receipts are in `sources.round6.lock.json`. A matching version label does not independently prove image-to-source provenance. Base-image pins do not lock later apt/apk or language-package resolution.

## Recommended acceptance checks

Fresh wizard access and anonymous setup rejection; login email; workspace creation and separate database; send a test campaign; exercise unsubscribe, tracking and provider callbacks without gateway credentials; check free-tier limits; preserve SECRET_KEY and restore every workspace database.

## Operations and recovery

Back up every listed persistent volume and export every application database, preserving the generated encryption/signing secrets. Restore into a separate test instance and repeat the functional workflow before relying on the backup. Keep internal databases private. An owner gateway `/healthz` response proves only that gateway is alive, not that its application or dependencies are ready. After changing a public domain, update all application origin and callback settings. Review upstream migrations before upgrading; record the old source/image pins and a recoverable backup. No scheduled backup service is configured by this draft.

## Validation status

The checked-in catalog supports static pin, reference, Docker COPY-path and script-syntax validation. Container builds, native proxy behavior, fresh Railway deployment, provider integrations, persistence and restore remain release gates. See `DRAFTS-ROUND-6.md` for the batch record.
