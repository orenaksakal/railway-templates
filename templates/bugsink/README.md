# Deploy and Host Bugsink Error Tracking on Railway

Self-hosted error tracking with private MySQL and generated admin access.

**Unpublished draft. Image builds and Railway application workflows have not been validated.** The template defines services; saving a draft creates no running application. Deploying it later incurs Railway usage and any external provider charges.

## About Hosting Bugsink Error Tracking

Two services: Bugsink and private MySQL 8.4. Retention defaults to 30 days and 100,000 events; tune after measuring your workload. No separate event volume is used: back up MySQL. The upstream PolyForm Shield license has restrictions; this listing does not grant rights to offer a competing hosted service. SDK ingestion is intentionally public and uses the application DSN.

## Setup

Enter bugsink.ADMIN_EMAIL. On first boot the image creates the administrator with bugsink.ADMIN_PASSWORD. Open the public Bugsink URL, sign in, create a project and copy its DSN into a test Sentry-compatible SDK. Configure optional SMTP variables for invitations and alerts.

### Deployment Dependencies

| Service | Source | Persistent volume | Public HTTP port |
| --- | --- | --- | --- |
| mysql | mysql:8.4 | /var/lib/mysql | Private |
| bugsink | bugsink/bugsink:2.5.1 | None | 8000 |

## Operator inputs

| Variable | Requirement |
| --- | --- |
| `bugsink.ADMIN_EMAIL` | Required. Required administrator email for first startup. |
| `bugsink.EMAIL_HOST` | Optional. Optional SMTP server for invitations and alerts. |
| `bugsink.EMAIL_HOST_USER` | Optional. SMTP username. |
| `bugsink.EMAIL_HOST_PASSWORD` | Optional. SMTP password. |
| `bugsink.DEFAULT_FROM_EMAIL` | Optional. Verified sender email. |

Generated credentials: `mysql.MYSQL_PASSWORD`, `mysql.MYSQL_ROOT_PASSWORD`, `bugsink.SECRET_KEY`, `bugsink.ADMIN_PASSWORD`. Never copy another deployment's secrets. Preserve encryption/signing keys with backups.

## Why Deploy Bugsink Error Tracking on Railway

The definition connects private dependencies, declares persistent volumes and exposes the listed application endpoints through Railway HTTPS. Repository adapters build from `codex/fifteen-template-drafts` with the repository root as Docker context. Configure one replica for each stateful service.

## Common Use Cases

Self-hosted error tracking with private MySQL and generated admin access. Use a separate test project to verify the workflow below before putting real data into the instance.

## Dependencies for Bugsink Error Tracking

Reviewed upstream release: [2.5.1](https://github.com/bugsink/bugsink/tree/68803af03ff09f1a9a5368fa5b9e79fa59902f1e). Image digests are recorded in `images.round6.lock.json`; source receipts are in `sources.round6.lock.json`. A matching version label does not independently prove image-to-source provenance. Base-image pins do not lock later apt/apk or language-package resolution.

## Recommended acceptance checks

Fresh database initialization; admin login; ingest a test exception through the actual SDK; view the stack trace; process queued events; confirm application registration policy; send one test alert; check retention; restart and restore the database into a separate instance.

## Operations and recovery

Back up every listed persistent volume and export every application database, preserving the generated encryption/signing secrets. Restore into a separate test instance and repeat the functional workflow before relying on the backup. Keep internal databases private. An owner gateway `/healthz` response proves only that gateway is alive, not that its application or dependencies are ready. After changing a public domain, update all application origin and callback settings. Review upstream migrations before upgrading; record the old source/image pins and a recoverable backup. No scheduled backup service is configured by this draft.

## Validation status

The checked-in catalog supports static pin, reference, Docker COPY-path and script-syntax validation. Container builds, native proxy behavior, fresh Railway deployment, provider integrations, persistence and restore remain release gates. See `DRAFTS-ROUND-6.md` for the batch record.
