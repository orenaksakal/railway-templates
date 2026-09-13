# Deploy and Host Lago Usage Billing on Railway

Usage billing with PostgreSQL, Redis, background jobs and invoice PDFs.

**Validation scope: static configuration checks only. Image builds and Railway application workflows have not been validated.** Deploying this template incurs Railway usage and any external provider charges.

## About Hosting Lago Usage Billing

Five services. The API adapter supervises the API, Sidekiq worker and clock in one service so the RSA key and local file storage share /data. PostgreSQL partman, Redis and PDF rendering are private; frontend and authenticated API are public. General signup and the Sidekiq web UI are disabled. Preserve all encryption variables and /data/keys/private.pem. Upstream AGPL-3.0 applies to community code; enterprise features and payment-provider accounts are not included. Invoice correctness and jurisdiction-specific billing setup are the operator's responsibility.

## Setup

Enter api.LAGO_ORG_USER_EMAIL. The migration task creates the organization using LAGO_ORG_USER_PASSWORD and LAGO_ORG_API_KEY before opening the API. Open lago and sign in. Configure billing currency, plans, a test customer and optional SMTP. Integrate payment-provider credentials inside Lago only when needed.

### Deployment Dependencies

| Service | Source | Persistent volume | Public HTTP port |
| --- | --- | --- | --- |
| postgres | getlago/postgres-partman:15.0-alpine | /var/lib/postgresql/data | Private |
| redis | redis:7.4 | /data | Private |
| api | Repository adapter: templates/lago/Dockerfile | /data | 3000 |
| lago | getlago/front:v1.53.0 | None | 80 |
| pdf | getlago/lago-gotenberg:8.15 | None | Private |

## Operator inputs

| Variable | Requirement |
| --- | --- |
| `api.LAGO_ORG_USER_EMAIL` | Required. Required first organization administrator email. |
| `api.LAGO_SMTP_ADDRESS` | Optional. SMTP host for invoices and account emails. |
| `api.LAGO_SMTP_USERNAME` | Optional. SMTP username. |
| `api.LAGO_SMTP_PASSWORD` | Optional. SMTP password. |
| `api.LAGO_FROM_EMAIL` | Optional. Verified sender email. |

Generated credentials: `postgres.POSTGRES_PASSWORD`, `redis.REDIS_PASSWORD`, `api.SECRET_KEY_BASE`, `api.LAGO_ENCRYPTION_PRIMARY_KEY`, `api.LAGO_ENCRYPTION_DETERMINISTIC_KEY`, `api.LAGO_ENCRYPTION_KEY_DERIVATION_SALT`, `api.LAGO_ORG_USER_PASSWORD`, `api.LAGO_ORG_API_KEY`. Never copy another deployment's secrets. Preserve encryption/signing keys with backups.

## Why Deploy Lago Usage Billing on Railway

The definition connects private dependencies, declares persistent volumes and exposes the listed application endpoints through Railway HTTPS. Repository adapters build from `codex/fifteen-template-drafts` with the repository root as Docker context. Configure one replica for each stateful service.

## Common Use Cases

Usage billing with PostgreSQL, Redis, background jobs and invoice PDFs. Use a separate test project to verify the workflow below before putting real data into the instance.

## Dependencies for Lago Usage Billing

Reviewed upstream release: [v1.53.0](https://github.com/getlago/lago/tree/ba292b669781714f33b3029267e9a6c17010b75d). Image digests are recorded in `images.round6.lock.json`; source receipts are in `sources.round6.lock.json`. A matching version label does not independently prove image-to-source provenance. Base-image pins do not lock later apt/apk or language-package resolution.

## Recommended acceptance checks

Build and run upstream migration scripts; verify owner seeding is idempotent; configure a usage metric and plan; ingest a test event; generate and download an invoice PDF; confirm jobs and clock run; test webhook delivery; restart without changing keys; restore the database and file volume together.

## Operations and recovery

Back up every listed persistent volume and export every application database, preserving the generated encryption/signing secrets. Restore into a separate test instance and repeat the functional workflow before relying on the backup. Keep internal databases private. An owner gateway `/healthz` response proves only that gateway is alive, not that its application or dependencies are ready. After changing a public domain, update all application origin and callback settings. Review upstream migrations before upgrading; record the old source/image pins and a recoverable backup. No scheduled backup service is configured by this draft.

## Validation status

The checked-in catalog supports static pin, reference, Docker COPY-path and script-syntax validation. Container builds, native proxy behavior, fresh Railway deployment, provider integrations, persistence and restore remain release gates. See `RELEASES-ROUND-6.md` for the publication record.
