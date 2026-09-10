# Deploy and Host Novu Community Edition on Railway

Novu Community Edition 3.19.0 supplies an API, worker, WebSocket service, and dashboard with MongoDB, authenticated Redis, and private S3-compatible storage. The four application images use the same version from the current Community Edition deployment source.

Release tested on Railway. See the validation scope below for verified workflows and remaining limitations.

## About Hosting Novu Community Edition

The template defines 7 services with pinned container digests, generated deployment secrets, explicit service references, and persistent volumes for stateful dependencies. Repository-backed adapters build from `main`. Railway terminates HTTPS for the public endpoints; databases and internal workers have no public TCP proxies. Fresh initialization was tested in an isolated Railway project. Each deployment has its own database and storage resources. Backups are not scheduled by this template, and filesystem-backed services should remain single-replica.

## Common Use Cases

- Trigger in-app notifications from application backends.
- Build notification workflows with your chosen delivery providers.
- Retain subscribers, workflow configuration, and delivery history.

## Dependencies for Novu Community Edition Hosting

### Deployment Dependencies

| Service | Source | Persistent path |
| --- | --- | --- |
| mongodb | `mongo:8.0.17` | `/data/db` |
| redis | `redis:7.4` | `/data` |
| storage | `shared/draft-storage/Dockerfile` | `/data` |
| api | `ghcr.io/novuhq/novu/api:3.19.0` | `None` |
| worker | `ghcr.io/novuhq/novu/worker:3.19.0` | `None` |
| ws | `ghcr.io/novuhq/novu/ws:3.19.0` | `None` |
| novu | `ghcr.io/novuhq/novu/dashboard:3.19.0` | `None` |

Required input before deployment: none; generated secrets and service references supply the template defaults.

## First Use

Open the novu dashboard domain and complete account setup. Its API and WebSocket domains are configured automatically. Create an application/workflow, add your own provider credentials, and trigger a test notification. STORE_ENCRYPTION_KEY is generated with exactly 32 characters as required upstream.



## Scope and Limitations

The service uses the Community Edition feature set, not Novu Cloud parity. SMTP/SMS/chat providers and their usage charges are separate. Storage uses a private bucket; browser attachment and asset delivery need functional verification before use. MongoDB is a single-node deployment.

## Backups and Upgrades

Back up MongoDB, object storage, Redis if pending jobs matter, and all encryption/signing secrets. Restoring provider records without STORE_ENCRYPTION_KEY can make credentials unreadable. Test restoration into an isolated project before depending on the backup. Image rollback alone does not revert database migrations.

## Validation Scope

Fresh Railway startup, account signup/login, organization/environment selection, workflow and subscriber creation, worker delivery of rendered in-app notifications, restart and volume-preserving redeploy passed. MongoDB was dumped and restored into a separate namespace and delivered messages were verified. The dashboard sign-in page rendered. External email/SMS/chat delivery, retry failure injection, authenticated browser workflows, attachment delivery, load testing and complete separate-project disaster recovery are not verified.

## Why Deploy Novu Community Edition on Railway?

Railway keeps the services, networking, environment references, deployment logs, and volumes together in one project. This template supplies the tested service configuration. Railway resources and volume storage are billed separately from external email, model, and other service providers. No deployment cost or revenue estimate has been measured.

## Support and Upstream

[Upstream source and release](https://github.com/novuhq/novu/tree/c7bc772fc0b7722909ef1bdb9bcf04991996fdd8/docker/community). This is an independent community integration; upstream licenses, trademarks, and paid-feature restrictions remain in effect. See the [draft readiness record](https://github.com/orenaksakal/railway-templates/blob/main/DRAFTS.md). Report issues with redacted logs and image versions; never share credentials.
