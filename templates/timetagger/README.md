# Deploy and Host TimeTagger on Railway

Personal time tracking with generated credentials and persistent data.

**Validation scope: static configuration checks only. Image builds and Railway application workflows have not been validated.** Deploying this template incurs Railway usage and any external provider charges.

## About Hosting TimeTagger

One service with persistent /opt/_timetagger storage. This draft provisions one configured account, not a team subscription/billing system. Change ADMIN_PASSWORD in Railway to rotate the configured credential; keep it at least 16 characters and no more than 72 UTF-8 bytes. TimeTagger uses the GPL-3.0 license. Railway usage is separate from the upstream service.

## Setup

Open timetagger and sign in using ADMIN_USERNAME (admin by default) and ADMIN_PASSWORD. The startup adapter generates a bcrypt credential from that password without writing its plaintext to a file. Create a few time records and tags, then view a report.

### Deployment Dependencies

| Service | Source | Persistent volume | Public HTTP port |
| --- | --- | --- | --- |
| timetagger | Repository adapter: templates/timetagger/Dockerfile | /opt/_timetagger | 8080 |

## Operator inputs

| Variable | Requirement |
| --- | --- |
| None | Initial credentials are generated; complete application setup above. |

Generated credentials: `timetagger.ADMIN_PASSWORD`. Never copy another deployment's secrets. Preserve encryption/signing keys with backups.

## Why Deploy TimeTagger on Railway

The definition connects private dependencies, declares persistent volumes and exposes the listed application endpoints through Railway HTTPS. Repository adapters build from `codex/fifteen-template-drafts` with the repository root as Docker context. Configure one replica for each stateful service.

## Common Use Cases

Personal time tracking with generated credentials and persistent data. Use a separate test project to verify the workflow below before putting real data into the instance.

## Dependencies for TimeTagger

Reviewed upstream release: [v26.1.3](https://github.com/almarklein/timetagger/tree/681720d84c94be660f30947db4b23e52d36cbe32). Image digests are recorded in `images.round6.lock.json`; source receipts are in `sources.round6.lock.json`. A matching version label does not independently prove image-to-source provenance. Base-image pins do not lock later apt/apk or language-package resolution.

## Recommended acceptance checks

Build; validate bcrypt dependency and native login; reject a wrong password; create and edit time records; check tags and report totals; test browser sync; restart without record loss; restore the data volume; verify a credential rotation.

## Operations and recovery

Back up every listed persistent volume and export every application database, preserving the generated encryption/signing secrets. Restore into a separate test instance and repeat the functional workflow before relying on the backup. Keep internal databases private. An owner gateway `/healthz` response proves only that gateway is alive, not that its application or dependencies are ready. After changing a public domain, update all application origin and callback settings. Review upstream migrations before upgrading; record the old source/image pins and a recoverable backup. No scheduled backup service is configured by this draft.

## Validation status

The checked-in catalog supports static pin, reference, Docker COPY-path and script-syntax validation. Container builds, native proxy behavior, fresh Railway deployment, provider integrations, persistence and restore remain release gates. See `RELEASES-ROUND-6.md` for the publication record.
