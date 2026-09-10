# Deploy and Host AppFlowy Cloud on Railway

AppFlowy Cloud 0.18.3 is paired with worker 0.18.3, the digest-pinned administration service, GoTrue, web client 0.17.1, PostgreSQL/pgvector, Redis, S3-compatible storage, and a routing gateway. Storage receives a public HTTPS endpoint so signed upload/download URLs can be reached by clients.

Release tested on Railway for the workflows below. The unlicensed server reports a one-user and three-guest limit; review upstream licensing before planning a team deployment.

## About Hosting AppFlowy Cloud

The template defines 9 services with pinned container digests, generated deployment secrets, explicit service references, and persistent volumes for stateful dependencies. Repository-backed adapters build from `main`. Railway terminates HTTPS for the public endpoints; databases and internal workers have no public TCP proxies. Services initialize independently; wait for database migrations and the cloud API before opening the frontend. Each deployment has its own database and storage resources. Backups are not scheduled by this template, and filesystem-backed services should remain single-replica.

## Common Use Cases

- Host an AppFlowy workspace backend.
- Connect desktop/mobile clients to private workspace data.
- Store and share document attachments through signed object URLs.

## Dependencies for AppFlowy Cloud Hosting

### Deployment Dependencies

| Service | Source | Persistent path |
| --- | --- | --- |
| postgres | `templates/appflowy/Postgres.Dockerfile` | `/var/lib/postgresql/data` |
| redis | `redis:7.4` | `/data` |
| storage | `shared/draft-storage/Dockerfile` | `/data` |
| gotrue | `appflowyinc/gotrue:latest` | `None` |
| cloud | `appflowyinc/appflowy_cloud:0.18.3` | `None` |
| worker | `appflowyinc/appflowy_worker:0.18.3` | `None` |
| admin | `appflowyinc/admin_frontend:latest` | `None` |
| web | `appflowyinc/appflowy_web:0.17.1` | `None` |
| appflowy | `templates/appflowy/Gateway.Dockerfile` | `None` |

Required input before deployment: `gotrue.GOTRUE_ADMIN_EMAIL`

## First Use

Enter your own GOTRUE_ADMIN_EMAIL before deployment. Its generated password creates the GoTrue service administrator, which is separate from an end-user AppFlowy account. Open the application domain and create the end-user account separately. Email autoconfirm starts enabled because no SMTP is supplied. Restrict signup and configure email before inviting users.



## Scope and Limitations

The server enforces upstream self-hosting license limits. In the tested unlicensed 0.18.3 deployment it reports a maximum of one user and three guests. Do not assume unlimited team usage. Optional AI and search services are not included; visible client features may require additional services and licensing. Administration and GoTrue tags are pinned by immutable digest in the template. The storage endpoint uses authenticated access with no anonymous bucket policy.

## Backups and Upgrades

Back up PostgreSQL, object storage, and signing/encryption credentials. Keep backend, worker, frontend, and authentication image digests in the backup manifest. Test restoration into an isolated project before depending on the backup. Image rollback alone does not revert database migrations.

## Validation Scope

A clean Railway installation on cloud/worker 0.18.3 and web 0.17.1 passed signup, workspace/page creation and file roundtrip. A separate deployment was upgraded from 0.9.64 after a database backup. Password signup/login, authenticated workspace lookup, page creation/rename/read, and file upload with byte-identical authenticated download passed. PostgreSQL was restored into a separate database and four object backups were restored into a separate directory with byte comparisons. Restart and volume-preserving redeploy retained page and file data. Two-client content editing/sync, desktop/mobile clients, invitations, imports, email, AI, load testing and complete separate-project disaster recovery are not verified.

## Why Deploy AppFlowy Cloud on Railway?

Railway keeps the services, networking, environment references, deployment logs, and volumes together in one project. This template supplies the tested service configuration. Railway resources and volume storage are billed separately from external email, model, and other service providers. No deployment cost or revenue estimate has been measured.

## Support and Upstream

[Upstream source and release](https://hub.docker.com/r/appflowyinc/appflowy_cloud/tags). This is an independent community integration; upstream licenses, trademarks, and paid-feature restrictions remain in effect. See the [draft readiness record](https://github.com/orenaksakal/railway-templates/blob/main/DRAFTS.md). Report issues with redacted logs and image versions; never share credentials.
