# Deploy and Host Appwrite 2 Core on Railway

An Appwrite 2.0.0 core-services template with its console, PostgreSQL, a MongoDB replica-set adapter, Redis, geolocation service, and a public routing gateway. API, combined workers, and scheduled tasks share one persistent /storage volume inside a supervised core service. Realtime runs privately in its own service to avoid conflicting with the API listener.

Release tested on Railway for the core workflows below. Functions and Sites execution are excluded.

## About Hosting Appwrite 2 Core

The template defines 8 services with pinned container digests, generated deployment secrets, explicit service references, and persistent volumes for stateful dependencies. Repository-backed adapters build from `main`. Railway terminates HTTPS for the public endpoints; databases and internal workers have no public TCP proxies. Services initialize independently. Let databases become ready before checking the API after a full-stack restart. Each deployment has its own database and storage resources. Backups are not scheduled by this template, and filesystem-backed services should remain single-replica.

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
| realtime | `templates/appwrite/Realtime.Dockerfile` | `None` |
| console | `appwrite/new:1.1.16` | `None` |
| geo | `appwrite/geo:0.3.1` | `None` |
| appwrite | `templates/appwrite/Gateway.Dockerfile` | `None` |

Required input before deployment: none; generated secrets and service references supply the template defaults.

## First Use

Open the appwrite gateway domain to create the first console administrator, then create a project and test the matching SDK. Keep the core service private. Database and encryption secrets are generated, and the MongoDB service initializes its replica identity using its private Railway hostname.



## Scope and Limitations

Functions/Sites execution and build workers require an executor that is not included. Usage analytics and embedding services are excluded. The core and realtime images carry exact-match patches for the pinned upstream queue connection to retain Redis authentication. Uploads have a 30 MB service ceiling; configure each bucket's file-size limit within it. Use one core replica.

## Backups and Upgrades

Back up PostgreSQL, MongoDB including its replica key, the complete core /storage volume, Redis, and encryption keys. Keep one core replica. Upgrades require a backed-up migration plan. Test restoration into an isolated project before depending on the backup. Image rollback alone does not revert database migrations.

## Validation Scope

Fresh Railway builds/startup, console account signup/login, organization/project/API-key creation, database/collection creation, asynchronous schema completion, document write/read, private file upload and byte-identical download, and unauthenticated file denial passed. Restart and volume-preserving redeploy retained records and files. PostgreSQL was restored into a separate database with 151 application tables; storage archives were restored into a separate directory and compared byte-for-byte. MongoDB startup/replica initialization and dump passed; its application document workload and restore are not verified. SDK compatibility, realtime event delivery, email/OAuth, broader permission scenarios, load testing and complete separate-project disaster recovery are not verified.

## Why Deploy Appwrite 2 Core on Railway?

Railway keeps the services, networking, environment references, deployment logs, and volumes together in one project. This template supplies the tested service configuration. Railway resources and volume storage are billed separately from external email, model, and other service providers. No deployment cost or revenue estimate has been measured.

## Support and Upstream

[Upstream source and release](https://github.com/appwrite/appwrite/tree/2.0.0). This is an independent community integration; upstream licenses, trademarks, and paid-feature restrictions remain in effect. See the [draft readiness record](https://github.com/orenaksakal/railway-templates/blob/main/DRAFTS.md). Report issues with redacted logs and image versions; never share credentials.
