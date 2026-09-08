# Deploy and Host Immich with Machine Learning on Railway

Immich v3.1.0 provides self-hosted photo and video backup with a matching CPU machine-learning service. The stack includes the upstream VectorChord/pgvecto.rs PostgreSQL image, an authenticated persistent Redis service, media storage, and a persistent model cache.

> Unpublished draft. This template is prepared for review; it has not been deployed on Railway or certified for production. See the validation scope below.

## About Hosting Immich with Machine Learning

The template defines 4 services with pinned container digests, generated deployment secrets, explicit service references, and persistent volumes for stateful dependencies. Repository-backed adapters build from `codex/remaining-template-drafts`. Railway terminates HTTPS for the public endpoints; databases and internal workers have no public TCP proxies. Services initialize independently, so cold-start and migration behavior must be verified in a new test project. Each deployment has its own database and storage resources. Backups are not scheduled by this template, and filesystem-backed services should remain single-replica.

## Common Use Cases

- Back up mobile photos and videos.
- Browse personal media libraries.
- Use CPU-powered search and face processing after model initialization.

## Dependencies for Immich with Machine Learning Hosting

| Service | Source | Persistent path |
| --- | --- | --- |
| postgres | `ghcr.io/immich-app/postgres:14-vectorchord0.4.3-pgvectors0.2.0` | `/var/lib/postgresql/data` |
| redis | `redis:7.4` | `/data` |
| machine-learning | `ghcr.io/immich-app/immich-machine-learning:v3.1.0` | `/cache` |
| immich | `templates/immich/Dockerfile` | `/data` |

Required input before deployment: none; generated secrets and service references supply the template defaults.

## First Use

Open the Immich domain and create the first administrator. Connect the mobile client to that same HTTPS URL and test an upload and download. The server adapter configures the private machine-learning URL through IMMICH_CONFIG_FILE. Model downloads need disk, memory, and outbound network access.



## Scope and Limitations

CPU-only processing is configured. GPU acceleration, hardware transcoding, external libraries, and external ML services are not configured. Keep one server replica with local media storage. Resource use depends strongly on library size and processing backlog.

## Backups and Upgrades

Back up PostgreSQL and the complete server /data volume. The machine-learning cache can be regenerated, but retain it to avoid repeat model downloads. Follow the upstream upgrade order. Test restoration into an isolated project before depending on the backup. Image rollback alone does not revert database migrations.

## Validation Scope

Matching server/ML tags, database image, configuration shape, and storage paths were checked. Build, mobile backup, search, face recognition, video processing, restart, and full recovery still require validation. Full Railway startup and product workflows remain release gates.

## Why Deploy Immich with Machine Learning on Railway?

Railway keeps the services, networking, environment references, deployment logs, and volumes together in one project. This draft supplies a reviewable starting configuration. Railway resources and volume storage are billed separately from external email, model, and other service providers. No deployment cost or revenue estimate has been measured.

## Support and Upstream

[Upstream source and release](https://github.com/immich-app/immich/tree/v3.1.0). This is an independent community integration; upstream licenses, trademarks, and paid-feature restrictions remain in effect. See the [draft readiness record](https://github.com/orenaksakal/railway-templates/blob/codex/remaining-template-drafts/DRAFTS.md). Report issues with redacted logs and image versions; never share credentials.
