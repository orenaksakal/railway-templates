# Deploy and Host Frappe Learning on Railway

Learning management with Frappe, MariaDB, Redis and persistent courses.

**Validation scope: static configuration checks only. Image builds and Railway application workflows have not been validated.** Deploying this template incurs Railway usage and any external provider charges.

## About Hosting Frappe Learning

Three services. The adapter builds LMS v2.63.0 and Payments at recorded commits on the pinned Frappe framework image. It runs web, Socket.IO, queue worker and scheduler with one /data volume. Database and Redis are private. AGPL-3.0 applies to LMS. The framework/app build and dependency compatibility still require a real image build. Upgrades to an existing site require a backup followed by ALLOW_MIGRATION=true; reset it after validation. Paid course billing requires a supported external payment provider.

## Setup

Open frappe-learning and sign in as Administrator with ADMIN_PASSWORD. A single site is created automatically. Configure outgoing email, create an instructor and learner, then publish a test course. Payments is installed as the upstream LMS dependency; payment-provider credentials are configured separately.

### Deployment Dependencies

| Service | Source | Persistent volume | Public HTTP port |
| --- | --- | --- | --- |
| mariadb | mariadb:10.11 | /var/lib/mysql | Private |
| redis | redis:7.4 | /data | Private |
| frappe-learning | Repository adapter: templates/frappe-learning/Dockerfile | /data | 8080 |

## Operator inputs

| Variable | Requirement |
| --- | --- |
| None | Initial credentials are generated; complete application setup above. |

Generated credentials: `mariadb.MARIADB_ROOT_PASSWORD`, `redis.REDIS_PASSWORD`, `frappe-learning.ADMIN_PASSWORD`. Never copy another deployment's secrets. Preserve encryption/signing keys with backups.

## Why Deploy Frappe Learning on Railway

The definition connects private dependencies, declares persistent volumes and exposes the listed application endpoints through Railway HTTPS. Repository adapters build from `codex/fifteen-template-drafts` with the repository root as Docker context. Configure one replica for each stateful service.

## Common Use Cases

Learning management with Frappe, MariaDB, Redis and persistent courses. Use a separate test project to verify the workflow below before putting real data into the instance.

## Dependencies for Frappe Learning

Reviewed upstream release: [v2.63.0](https://github.com/frappe/lms/tree/2ee61568603d0b081e9d98c8bf39b18f4464e3b5). Image digests are recorded in `images.round6.lock.json`; source receipts are in `sources.round6.lock.json`. A matching version label does not independently prove image-to-source provenance. Base-image pins do not lock later apt/apk or language-package resolution.

## Recommended acceptance checks

Build LMS and Payments; create a clean site; verify Administrator login; create a course with a file lesson and quiz; enroll a learner and record completion; test realtime/worker jobs and email; verify Payments installation; restart; use bench backups and prove recovery of database, site config, public and private files.

## Operations and recovery

Back up every listed persistent volume and export every application database, preserving the generated encryption/signing secrets. Restore into a separate test instance and repeat the functional workflow before relying on the backup. Keep internal databases private. An owner gateway `/healthz` response proves only that gateway is alive, not that its application or dependencies are ready. After changing a public domain, update all application origin and callback settings. Review upstream migrations before upgrading; record the old source/image pins and a recoverable backup. No scheduled backup service is configured by this draft.

## Validation status

The checked-in catalog supports static pin, reference, Docker COPY-path and script-syntax validation. Container builds, native proxy behavior, fresh Railway deployment, provider integrations, persistence and restore remain release gates. See `RELEASES-ROUND-6.md` for the publication record.
