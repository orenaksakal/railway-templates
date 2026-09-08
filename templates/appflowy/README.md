# Deploy and Host AppFlowy Cloud on Railway

AppFlowy Cloud 0.9.64 is paired with its matching worker and administration service, GoTrue, a web client, PostgreSQL/pgvector, Redis, S3-compatible storage, and a routing gateway. Storage receives a public HTTPS endpoint so signed upload/download URLs can be reached by clients.

> Unpublished draft. This template is prepared for review; it has not been deployed on Railway or certified for production. See the validation scope below.

## About Hosting AppFlowy Cloud

The template defines 9 services with pinned container digests, generated deployment secrets, explicit service references, and persistent volumes for stateful dependencies. Repository-backed adapters build from `codex/remaining-template-drafts`. Railway terminates HTTPS for the public endpoints; databases and internal workers have no public TCP proxies. Services initialize independently, so cold-start and migration behavior must be verified in a new test project. Each deployment has its own database and storage resources. Backups are not scheduled by this template, and filesystem-backed services should remain single-replica.

## Common Use Cases

- Host an AppFlowy workspace backend.
- Connect desktop/mobile clients to private workspace data.
- Store and share document attachments through signed object URLs.

## Dependencies for AppFlowy Cloud Hosting

| Service | Source | Persistent path |
| --- | --- | --- |
| postgres | `templates/appflowy/Postgres.Dockerfile` | `/var/lib/postgresql/data` |
| redis | `redis:7.4` | `/data` |
| storage | `shared/draft-storage/Dockerfile` | `/data` |
| gotrue | `appflowyinc/gotrue:latest` | `None` |
| cloud | `appflowyinc/appflowy_cloud:0.9.64` | `None` |
| worker | `appflowyinc/appflowy_worker:0.9.64` | `None` |
| admin | `appflowyinc/admin_frontend:0.9.64` | `None` |
| web | `appflowyinc/appflowy_web:latest` | `None` |
| appflowy | `templates/appflowy/Gateway.Dockerfile` | `None` |

Required input before deployment: `gotrue.GOTRUE_ADMIN_EMAIL`

## First Use

Enter your own GOTRUE_ADMIN_EMAIL before deployment. Its generated password creates the GoTrue service administrator, which is separate from an end-user AppFlowy account. Open the application domain and create the end-user account separately. Email autoconfirm starts enabled because no SMTP is supplied. Restrict signup and configure email before inviting users.



## Scope and Limitations

The 0.9.64 web image tag does not exist. The draft instead pins the upstream web and GoTrue latest images by immutable digest; cross-version client compatibility is a specific release blocker. Optional AI services and indexing are excluded. The public storage endpoint is authenticated and no anonymous bucket policy is installed.

## Backups and Upgrades

Back up PostgreSQL, object storage, and signing/encryption credentials. Keep backend, worker, frontend, and authentication image digests in the backup manifest. Test restoration into an isolated project before depending on the backup. Image rollback alone does not revert database migrations.

## Validation Scope

Backend/worker/admin image versions and public presigned-URL configuration were checked. Frontend/GoTrue compatibility, user onboarding, signed uploads, two-client editing, invitations, import worker, and restore remain unverified. Full Railway startup and product workflows remain release gates.

## Why Deploy AppFlowy Cloud on Railway?

Railway keeps the services, networking, environment references, deployment logs, and volumes together in one project. This draft supplies a reviewable starting configuration. Railway resources and volume storage are billed separately from external email, model, and other service providers. No deployment cost or revenue estimate has been measured.

## Support and Upstream

[Upstream source and release](https://github.com/AppFlowy-IO/AppFlowy-Cloud/tree/0.9.64). This is an independent community integration; upstream licenses, trademarks, and paid-feature restrictions remain in effect. See the [draft readiness record](https://github.com/orenaksakal/railway-templates/blob/codex/remaining-template-drafts/DRAFTS.md). Report issues with redacted logs and image versions; never share credentials.
