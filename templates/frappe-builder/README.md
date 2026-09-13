# Deploy and Host Frappe Builder on Railway

Visual website builder with Frappe, MariaDB and persistent assets.

**Validation scope: static configuration checks only. Image builds and Railway application workflows have not been validated.** Deploying this template incurs Railway usage and any external provider charges.

## About Hosting Frappe Builder

Three services. Builds Builder v1.34.0 at its recorded commit on the pinned framework. Admin/editor authentication is native Frappe, so published pages can be public. One site and one replica; custom domain/DNS setup is not automated. The Builder application is MIT-licensed; framework and dependency licenses still apply. Build compatibility and rendered custom-domain links need runtime checks. Backups must include MariaDB plus /data site configuration and assets.

## Setup

Open frappe-builder and sign in as Administrator with ADMIN_PASSWORD. Create a page, upload an asset and publish it. Configure a custom Railway domain and update PUBLIC_URL if using your own hostname. SMTP and optional AI-provider credentials are configured separately.

### Deployment Dependencies

| Service | Source | Persistent volume | Public HTTP port |
| --- | --- | --- | --- |
| mariadb | mariadb:10.11 | /var/lib/mysql | Private |
| redis | redis:7.4 | /data | Private |
| frappe-builder | Repository adapter: templates/frappe-builder/Dockerfile | /data | 8080 |

## Operator inputs

| Variable | Requirement |
| --- | --- |
| None | Initial credentials are generated; complete application setup above. |

Generated credentials: `mariadb.MARIADB_ROOT_PASSWORD`, `redis.REDIS_PASSWORD`, `frappe-builder.ADMIN_PASSWORD`. Never copy another deployment's secrets. Preserve encryption/signing keys with backups.

## Why Deploy Frappe Builder on Railway

The definition connects private dependencies, declares persistent volumes and exposes the listed application endpoints through Railway HTTPS. Repository adapters build from `codex/fifteen-template-drafts` with the repository root as Docker context. Configure one replica for each stateful service.

## Common Use Cases

Visual website builder with Frappe, MariaDB and persistent assets. Use a separate test project to verify the workflow below before putting real data into the instance.

## Dependencies for Frappe Builder

Reviewed upstream release: [v1.34.0](https://github.com/frappe/builder/tree/09c3effa10926e736a87d80f68880d81f498fbe2). Image digests are recorded in `images.round6.lock.json`; source receipts are in `sources.round6.lock.json`. A matching version label does not independently prove image-to-source provenance. Base-image pins do not lock later apt/apk or language-package resolution.

## Recommended acceptance checks

Build Python and frontend assets; create a fresh site; sign in; edit and preview a page; upload an image; publish and open it logged out; verify editor remains protected; test asset URLs and custom host redirects; restart and restore the page and files.

## Operations and recovery

Back up every listed persistent volume and export every application database, preserving the generated encryption/signing secrets. Restore into a separate test instance and repeat the functional workflow before relying on the backup. Keep internal databases private. An owner gateway `/healthz` response proves only that gateway is alive, not that its application or dependencies are ready. After changing a public domain, update all application origin and callback settings. Review upstream migrations before upgrading; record the old source/image pins and a recoverable backup. No scheduled backup service is configured by this draft.

## Validation status

The checked-in catalog supports static pin, reference, Docker COPY-path and script-syntax validation. Container builds, native proxy behavior, fresh Railway deployment, provider integrations, persistence and restore remain release gates. See `RELEASES-ROUND-6.md` for the publication record.
