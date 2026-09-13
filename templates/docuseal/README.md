# Deploy and Host DocuSeal Document Signing on Railway

Document signing with PostgreSQL and an administrator created at startup.

**Validation scope: static configuration checks only. Image builds and Railway application workflows have not been validated.** Deploying this template incurs Railway usage and any external provider charges.

## About Hosting DocuSeal Document Signing

Two services: DocuSeal and PostgreSQL. Uploaded documents and generated artifacts are persisted in /data/docuseal; account data is in PostgreSQL. The bootstrap does not reset an existing account or password. Recipient links use native application authorization and need no gateway password. Preserve SECRET_KEY_BASE and the database-backed signing certificates. Review upstream AGPL-3.0 plus LICENSE_ADDITIONAL_TERMS; no paid license or legal compliance certification is included.

## Setup

Enter docuseal.ADMIN_EMAIL. First startup creates the account and administrator with ADMIN_PASSWORD before HTTP begins. Sign in, set the organization details and SMTP sender, upload a test PDF and create a signing template. Share a test signing link with a recipient you control.

### Deployment Dependencies

| Service | Source | Persistent volume | Public HTTP port |
| --- | --- | --- | --- |
| postgres | postgres:17-alpine | /var/lib/postgresql/data | Private |
| docuseal | Repository adapter: templates/docuseal/Dockerfile | /data/docuseal | 3000 |

## Operator inputs

| Variable | Requirement |
| --- | --- |
| `docuseal.ADMIN_EMAIL` | Required. Required first administrator email. Created before the public listener opens. |

Generated credentials: `postgres.POSTGRES_PASSWORD`, `docuseal.SECRET_KEY_BASE`, `docuseal.ADMIN_PASSWORD`, `docuseal.SIDEKIQ_BASIC_AUTH_PASSWORD`. Never copy another deployment's secrets. Preserve encryption/signing keys with backups.

## Why Deploy DocuSeal Document Signing on Railway

The definition connects private dependencies, declares persistent volumes and exposes the listed application endpoints through Railway HTTPS. Repository adapters build from `codex/fifteen-template-drafts` with the repository root as Docker context. Configure one replica for each stateful service.

## Common Use Cases

Document signing with PostgreSQL and an administrator created at startup. Use a separate test project to verify the workflow below before putting real data into the instance.

## Dependencies for DocuSeal Document Signing

Reviewed upstream release: [3.2.4](https://github.com/docusealco/docuseal/tree/11856a17ac0865128333a0ffe1fdfc44e4b8a982). Image digests are recorded in `images.round6.lock.json`; source receipts are in `sources.round6.lock.json`. A matching version label does not independently prove image-to-source provenance. Base-image pins do not lock later apt/apk or language-package resolution.

## Recommended acceptance checks

Build; verify automatic migrations and one-time admin creation; reject an anonymous setup takeover; upload a PDF; place fields; complete a signature as the test recipient; download the signed PDF and audit evidence; test SMTP; restart and restore database plus documents and keys.

## Operations and recovery

Back up every listed persistent volume and export every application database, preserving the generated encryption/signing secrets. Restore into a separate test instance and repeat the functional workflow before relying on the backup. Keep internal databases private. An owner gateway `/healthz` response proves only that gateway is alive, not that its application or dependencies are ready. After changing a public domain, update all application origin and callback settings. Review upstream migrations before upgrading; record the old source/image pins and a recoverable backup. No scheduled backup service is configured by this draft.

## Validation status

The checked-in catalog supports static pin, reference, Docker COPY-path and script-syntax validation. Container builds, native proxy behavior, fresh Railway deployment, provider integrations, persistence and restore remain release gates. See `RELEASES-ROUND-6.md` for the publication record.
