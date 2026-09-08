# Deploy and Host RAGFlow CPU on Railway

RAGFlow 0.27.1 with CPU processing, MySQL, Elasticsearch, authenticated Redis, and S3-compatible object storage. The adapter supplies a service configuration referencing Railway private hosts and avoids exposing the administration API.

> Unpublished draft. This template is prepared for review; it has not been deployed on Railway or certified for production. See the validation scope below.

## About Hosting RAGFlow CPU

The template defines 5 services with pinned container digests, generated deployment secrets, explicit service references, and persistent volumes for stateful dependencies. Repository-backed adapters build from `codex/remaining-template-drafts`. Railway terminates HTTPS for the public endpoints; databases and internal workers have no public TCP proxies. Services initialize independently, so cold-start and migration behavior must be verified in a new test project. Each deployment has its own database and storage resources. Backups are not scheduled by this template, and filesystem-backed services should remain single-replica.

## Common Use Cases

- Ingest documents into retrieval datasets.
- Configure model providers for retrieval-augmented applications.
- Evaluate document parsing and answers with citations.

## Dependencies for RAGFlow CPU Hosting

### Deployment Dependencies

| Service | Source | Persistent path |
| --- | --- | --- |
| mysql | `mysql:8.0.40` | `/var/lib/mysql` |
| elasticsearch | `elasticsearch:8.11.3` | `/usr/share/elasticsearch/data` |
| redis | `redis:7.4` | `/data` |
| storage | `shared/draft-storage/Dockerfile` | `/data` |
| ragflow | `templates/ragflow/Dockerfile` | `None` |

Required input before deployment: none; generated secrets and service references supply the template defaults.

## First Use

Open the ragflow domain, create the intended accounts, and configure your own model-provider credentials in the application. Disable further registration when onboarding is complete. Upload a small document and wait for parsing/indexing before testing retrieval.



## Scope and Limitations

GPU acceleration, TEI inference, optional Go services, and the Docker-socket sandbox executor are excluded. Elasticsearch memory mapping is disabled to avoid a host sysctl dependency. Upstream capacity requirements are substantial; this image was not pulled locally because its expected size could consume the available disk budget. No measured Railway cost or capacity claim is made.

## Backups and Upgrades

Back up MySQL, Elasticsearch data, object storage, Redis if jobs matter, and provider credentials. The application service itself holds no authoritative persistent uploads in this topology. Test restoration into an isolated project before depending on the backup. Image rollback alone does not revert database migrations.

## Validation Scope

Pinned application/dependency images and private endpoints were checked. Startup, parser/model downloads, document ingestion, retrieval/citations, queue restart, resource requirements, and restore remain untested. Full Railway startup and product workflows remain release gates.

## Why Deploy RAGFlow CPU on Railway?

Railway keeps the services, networking, environment references, deployment logs, and volumes together in one project. This draft supplies a reviewable starting configuration. Railway resources and volume storage are billed separately from external email, model, and other service providers. No deployment cost or revenue estimate has been measured.

## Support and Upstream

[Upstream source and release](https://github.com/infiniflow/ragflow/tree/v0.27.1). This is an independent community integration; upstream licenses, trademarks, and paid-feature restrictions remain in effect. See the [draft readiness record](https://github.com/orenaksakal/railway-templates/blob/codex/remaining-template-drafts/DRAFTS.md). Report issues with redacted logs and image versions; never share credentials.
