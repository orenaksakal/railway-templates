# Deploy and Host Plunk Email Platform on Railway

Email campaigns and transactional delivery with AWS SES and storage.

**Unpublished draft. Image builds and Railway application workflows have not been validated.** The template defines services; saving a draft creates no running application. Deploying it later incurs Railway usage and any external provider charges.

## About Hosting Plunk Email Platform

Seven services include the API/dashboard, background processes, PostgreSQL, Redis, MinIO, and protected landing/docs endpoints. Only the uploads bucket is anonymously readable, to render email images; it must never contain confidential documents. Recipient unsubscribe, preference, public-contact and SNS callback routes bypass the owner gateway and rely on upstream validation. SMTP inbound/TCP delivery is not exposed; this template is for SES-backed HTTP sending. SES production access, sending reputation, DNS and provider fees belong to the operator. AGPL-3.0 upstream terms apply.

## Setup

Enter core.AWS_SES_REGION, AWS_SES_ACCESS_KEY_ID, AWS_SES_SECRET_ACCESS_KEY and SES_CONFIGURATION_SET for your own SES account. Open plunk with Basic-auth username admin and plunk.ACCESS_PASSWORD, create the first application account, then set core.DISABLE_SIGNUPS=true. Configure and verify the sending domain in SES. Configure signed SNS notifications to https://YOUR-PLUNK-DOMAIN/api/webhooks/sns. API clients use the application API credential plus X-Template-Key containing the gateway password.

### Deployment Dependencies

| Service | Source | Persistent volume | Public HTTP port |
| --- | --- | --- | --- |
| postgres | postgres:16-alpine | /var/lib/postgresql/data | Private |
| redis | redis:7.4 | /data | Private |
| storage | Repository adapter: shared/round6-storage/Dockerfile | /data | 9000 |
| core | Repository adapter: templates/plunk/Dockerfile | /app/data | Private |
| plunk | Repository adapter: templates/plunk/Gateway.Dockerfile | None | 8080 |
| landing | Repository adapter: shared/round6-gateway/Dockerfile | None | 8080 |
| docs | Repository adapter: shared/round6-gateway/Dockerfile | None | 8080 |

## Operator inputs

| Variable | Requirement |
| --- | --- |
| `core.AWS_SES_REGION` | Required. Required region of your configured AWS SES account. |
| `core.AWS_SES_ACCESS_KEY_ID` | Required. Required operator-owned SES access key. Never use a template author credential. |
| `core.AWS_SES_SECRET_ACCESS_KEY` | Required. Required operator-supplied aws ses secret access key. Enter your own value before deployment. |
| `core.SES_CONFIGURATION_SET` | Required. Required SES configuration set with the SNS callback described below. |

Generated credentials: `postgres.POSTGRES_PASSWORD`, `redis.REDIS_PASSWORD`, `storage.MINIO_ROOT_USER`, `storage.MINIO_ROOT_PASSWORD`, `core.JWT_SECRET`, `plunk.ACCESS_PASSWORD`. Never copy another deployment's secrets. Preserve encryption/signing keys with backups.

## Why Deploy Plunk Email Platform on Railway

The definition connects private dependencies, declares persistent volumes and exposes the listed application endpoints through Railway HTTPS. Repository adapters build from `codex/fifteen-template-drafts` with the repository root as Docker context. Configure one replica for each stateful service.

## Common Use Cases

Email campaigns and transactional delivery with AWS SES and storage. Use a separate test project to verify the workflow below before putting real data into the instance.

## Dependencies for Plunk Email Platform

Reviewed upstream release: [v0.14.0](https://github.com/useplunk/plunk/tree/ee0efe0974014cf9bf13ccee8610501a93ea9a03). Image digests are recorded in `images.round6.lock.json`; source receipts are in `sources.round6.lock.json`. A matching version label does not independently prove image-to-source provenance. Base-image pins do not lock later apt/apk or language-package resolution.

## Recommended acceptance checks

Build the adapter; create the owner account; verify unauthenticated admin requests fail; send to a consented test recipient; render a stored image; process signed SNS delivery/bounce events; test one-click unsubscribe and preferences without owner credentials; confirm forged SNS messages are rejected; restart and verify campaigns, contacts and assets.

## Operations and recovery

Back up every listed persistent volume and export every application database, preserving the generated encryption/signing secrets. Restore into a separate test instance and repeat the functional workflow before relying on the backup. Keep internal databases private. An owner gateway `/healthz` response proves only that gateway is alive, not that its application or dependencies are ready. After changing a public domain, update all application origin and callback settings. Review upstream migrations before upgrading; record the old source/image pins and a recoverable backup. No scheduled backup service is configured by this draft.

## Validation status

The checked-in catalog supports static pin, reference, Docker COPY-path and script-syntax validation. Container builds, native proxy behavior, fresh Railway deployment, provider integrations, persistence and restore remain release gates. See `DRAFTS-ROUND-6.md` for the batch record.
