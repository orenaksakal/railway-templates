# Deploy and Host Appwrite 2 Core on Railway

An Appwrite 2.0.0 core-services draft with its console, PostgreSQL, a MongoDB replica-set adapter, Redis, geolocation service, and a public routing gateway. API, combined workers, and scheduled tasks share one persistent /storage volume inside a supervised core service. Realtime runs privately in its own service to avoid conflicting with the API listener.

> Unpublished draft. This template is prepared for review; it has not been deployed on Railway or certified for production. See the validation scope below.

## About Hosting Appwrite 2 Core

The template defines 8 services with pinned container digests, generated deployment secrets, explicit service references, and persistent volumes for stateful dependencies. Repository-backed adapters build from `codex/remaining-template-drafts`. Railway terminates HTTPS for the public endpoints; databases and internal workers have no public TCP proxies. Services initialize independently, so cold-start and migration behavior must be verified in a new test project. Each deployment has its own database and storage resources. Backups are not scheduled by this template, and filesystem-backed services should remain single-replica.

## Common Use Cases

- Evaluate self-hosted account and database APIs.
- Test file storage and realtime integration.
- Prototype an Appwrite backend without Functions or Sites execution.

## Dependencies for Appwrite 2 Core Hosting

### Deployment Dependencies

| Service | Source | Persistent path |
| --- | --- | --- |
| postgres | `appwrite/postgres:0.1.0` | `/var/lib/postgresql` |
| mongodb | `templates/appwrite/Mongo.Dockerfile` | `/data` |
| redis | `redis:7.4` | `/data` |
| core | `templates/appwrite/Dockerfile` | `/storage` |
| realtime | `appwrite/appwrite:2.0.0` | `None` |
| console | `appwrite/new:1.1.16` | `None` |
| geo | `appwrite/geo:0.3.1` | `None` |
| appwrite | `templates/appwrite/Gateway.Dockerfile` | `None` |

Required input before deployment: none; generated secrets and service references supply the template defaults.

## First Use

Open the appwrite gateway domain to create the first console administrator, then create a project and test the matching SDK. Keep the core service private. Database and encryption secrets are generated, and the MongoDB service initializes its replica identity using its private Railway hostname.



## Scope and Limitations

This is the highest-risk draft. Functions/Sites execution and build workers cannot provide their advertised functionality without the unsupported Docker-socket executor, which is excluded. Usage analytics and embedding services are also excluded. Co-located core-process behavior, database adapter compatibility, and first-boot initialization are not validated; do not treat the presence of these settings as a working Appwrite deployment.

## Backups and Upgrades

Back up PostgreSQL, MongoDB including its replica key, the complete core /storage volume, Redis, and encryption keys. Keep one core replica. Upgrades require a backed-up migration plan. Test restoration into an isolated project before depending on the backup. Image rollback alone does not revert database migrations.

## Validation Scope

Upstream service commands, storage-sharing requirements, and database adapter configuration were inspected. The image build, first boot, SDK auth, CRUD/permissions across database types, uploads, realtime, background tasks, and recovery must pass before this draft is deploy-ready. Full Railway startup and product workflows remain release gates.

## Why Deploy Appwrite 2 Core on Railway?

Railway keeps the services, networking, environment references, deployment logs, and volumes together in one project. This draft supplies a reviewable starting configuration. Railway resources and volume storage are billed separately from external email, model, and other service providers. No deployment cost or revenue estimate has been measured.

## Support and Upstream

[Upstream source and release](https://github.com/appwrite/appwrite/tree/2.0.0). This is an independent community integration; upstream licenses, trademarks, and paid-feature restrictions remain in effect. See the [draft readiness record](https://github.com/orenaksakal/railway-templates/blob/codex/remaining-template-drafts/DRAFTS.md). Report issues with redacted logs and image versions; never share credentials.
