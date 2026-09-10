# Deploy and Host RAGFlow CPU on Railway

RAGFlow 0.27.1 with CPU processing, MySQL, Elasticsearch, authenticated Redis, and S3-compatible object storage. The adapter supplies a service configuration referencing Railway private hosts and avoids exposing the administration API.

Release tested on Railway with an operator-configured embedding provider. No model provider is bundled.

## About Hosting RAGFlow CPU

The template defines 5 services with pinned container digests, generated deployment secrets, explicit service references, and persistent volumes for stateful dependencies. Repository-backed adapters build from `main`. Railway terminates HTTPS for the public endpoints; databases and internal workers have no public TCP proxies. Fresh initialization was tested in an isolated Railway project. Each deployment has its own database and storage resources. Backups are not scheduled by this template, and filesystem-backed services should remain single-replica.

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

Fresh Railway startup, signup/login, authenticated profile, private dataset creation, text-document upload, parsing, embedding and semantic retrieval passed using a temporary private CPU embedding service. That test service is not part of this template; configure your own compatible provider. Restart and volume-preserving redeploy retained retrieval results. MySQL was restored into a separate database, object backups into a separate directory with byte comparison, and the test search document into a separate Elasticsearch index with all fields equal. Generated answers, external LLM billing, PDF/OCR/large-file parsing, load testing and complete separate-project disaster recovery are not verified. Search-document export testing does not replace a production Elasticsearch snapshot policy.

## Why Deploy RAGFlow CPU on Railway?

Railway keeps the services, networking, environment references, deployment logs, and volumes together in one project. This template supplies the tested service configuration. Railway resources and volume storage are billed separately from external email, model, and other service providers. No deployment cost or revenue estimate has been measured.

## Support and Upstream

[Upstream source and release](https://github.com/infiniflow/ragflow/tree/v0.27.1). This is an independent community integration; upstream licenses, trademarks, and paid-feature restrictions remain in effect. See the [draft readiness record](https://github.com/orenaksakal/railway-templates/blob/main/DRAFTS.md). Report issues with redacted logs and image versions; never share credentials.
