# Deploy and Host Frappe Insights on Railway

Business intelligence dashboards with Frappe, MariaDB and Redis.

**Unpublished draft. Image builds and Railway application workflows have not been validated.** The template defines services; saving a draft creates no running application. Deploying it later incurs Railway usage and any external provider charges.

## About Hosting Frappe Insights

Three services. Builds Insights v3.13.2 at its recorded commit on the pinned framework. Web, Socket.IO, worker and scheduler share one site volume. Server scripts are enabled because Insights needs them; treat application administrators as trusted. External analytics databases are not copied into this stack or included in its backups. AGPL-3.0 upstream terms apply. Test compatibility with your chosen connector; paid managed hosting and enterprise support are not included.

## Setup

Open frappe-insights and sign in as Administrator with ADMIN_PASSWORD. Connect a disposable read-only analytics datasource, create a query and save a dashboard. Configure SMTP for collaboration. Restrict datasource credentials to the data your users should see.

### Deployment Dependencies

| Service | Source | Persistent volume | Public HTTP port |
| --- | --- | --- | --- |
| mariadb | mariadb:10.11 | /var/lib/mysql | Private |
| redis | redis:7.4 | /data | Private |
| frappe-insights | Repository adapter: templates/frappe-insights/Dockerfile | /data | 8080 |

## Operator inputs

| Variable | Requirement |
| --- | --- |
| None | Initial credentials are generated; complete application setup above. |

Generated credentials: `mariadb.MARIADB_ROOT_PASSWORD`, `redis.REDIS_PASSWORD`, `frappe-insights.ADMIN_PASSWORD`. Never copy another deployment's secrets. Preserve encryption/signing keys with backups.

## Why Deploy Frappe Insights on Railway

The definition connects private dependencies, declares persistent volumes and exposes the listed application endpoints through Railway HTTPS. Repository adapters build from `codex/fifteen-template-drafts` with the repository root as Docker context. Configure one replica for each stateful service.

## Common Use Cases

Business intelligence dashboards with Frappe, MariaDB and Redis. Use a separate test project to verify the workflow below before putting real data into the instance.

## Dependencies for Frappe Insights

Reviewed upstream release: [v3.13.2](https://github.com/frappe/insights/tree/b7bf01ad60d5ae45a9863e81ab89c24785adfade). Image digests are recorded in `images.round6.lock.json`; source receipts are in `sources.round6.lock.json`. A matching version label does not independently prove image-to-source provenance. Base-image pins do not lock later apt/apk or language-package resolution.

## Recommended acceptance checks

Build all frontend and Python dependencies; fresh site installation; login; connect the selected database; execute a bounded query; save and share a dashboard; verify viewer permissions; scheduled refresh and worker processing; restart; restore site data and reconnect the read-only source.

## Operations and recovery

Back up every listed persistent volume and export every application database, preserving the generated encryption/signing secrets. Restore into a separate test instance and repeat the functional workflow before relying on the backup. Keep internal databases private. An owner gateway `/healthz` response proves only that gateway is alive, not that its application or dependencies are ready. After changing a public domain, update all application origin and callback settings. Review upstream migrations before upgrading; record the old source/image pins and a recoverable backup. No scheduled backup service is configured by this draft.

## Validation status

The checked-in catalog supports static pin, reference, Docker COPY-path and script-syntax validation. Container builds, native proxy behavior, fresh Railway deployment, provider integrations, persistence and restore remain release gates. See `DRAFTS-ROUND-6.md` for the batch record.
