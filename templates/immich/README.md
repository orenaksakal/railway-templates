# Deploy and Host Immich with Machine Learning on Railway

Immich v3.1.0 provides self-hosted photo and video backup with a matching CPU machine-learning service. The stack includes the upstream VectorChord/pgvecto.rs PostgreSQL image, an authenticated persistent Redis service, media storage, and a persistent model cache.

Verified in an isolated Railway deployment. See the validation scope below for the checks performed and operational limits.

## About Hosting Immich with Machine Learning

The template defines 4 services with pinned container digests, generated deployment secrets, explicit service references, and persistent volumes for stateful dependencies. Repository-backed adapters build from `main`. Railway terminates HTTPS for the public endpoints; databases and internal workers have no public TCP proxies. Cold-start initialization was verified in a fresh Railway project. Each deployment has its own database and storage resources. Backups are not scheduled by this template, and filesystem-backed services should remain single-replica.

## Common Use Cases

- Back up mobile photos and videos.
- Browse personal media libraries.
- Use CPU-powered search and face processing after model initialization.

## Dependencies for Immich with Machine Learning Hosting

### Deployment Dependencies

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

Fresh Railway startup, generated credentials, administrator signup/login, unauthorized-access rejection, photo upload, metadata, thumbnail generation, and byte-identical original download passed. CPU semantic search returned the uploaded image, with its embedding persisted in PostgreSQL. All four services passed restart and volume-preserving redeploy checks. A PostgreSQL dump restored into a separate database, and a media archive restored into a separate directory with all nine test files passing hash verification. Mobile clients, video transcoding, GPU inference, large libraries, and full separate-project disaster recovery were not tested. Backups are not scheduled automatically.

## Why Deploy Immich with Machine Learning on Railway?

Railway keeps the services, networking, environment references, deployment logs, and volumes together in one project. This template supplies the tested service configuration. Railway resources and volume storage are billed separately from external email, model, and other service providers. No deployment cost or revenue estimate has been measured.

## Support and Upstream

[Upstream source and release](https://github.com/immich-app/immich/tree/v3.1.0). This is an independent community integration; upstream licenses, trademarks, and paid-feature restrictions remain in effect. See the [draft readiness record](https://github.com/orenaksakal/railway-templates/blob/main/DRAFTS.md). Report issues with redacted logs and image versions; never share credentials.
