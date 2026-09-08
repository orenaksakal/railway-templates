# Deploy and Host Matrix Synapse with MAS on Railway

This draft combines Synapse 1.160.0, Matrix Authentication Service 1.24.0, Element Web 1.12.27, and separate PostgreSQL databases for the homeserver and authentication service. A routing gateway directs legacy login/logout/refresh endpoints to MAS and other Matrix endpoints to Synapse.

> Unpublished draft. This template is prepared for review; it has not been deployed on Railway or certified for production. See the validation scope below.

## About Hosting Matrix Synapse with MAS

The template defines 6 services with pinned container digests, generated deployment secrets, explicit service references, and persistent volumes for stateful dependencies. Repository-backed adapters build from `codex/remaining-template-drafts`. Railway terminates HTTPS for the public endpoints; databases and internal workers have no public TCP proxies. Services initialize independently, so cold-start and migration behavior must be verified in a new test project. Each deployment has its own database and storage resources. Backups are not scheduled by this template, and filesystem-backed services should remain single-replica.

## Common Use Cases

- Host a private Matrix community.
- Use delegated authentication with Element Web.
- Exchange messages and media over a self-hosted homeserver.

## Dependencies for Matrix Synapse with MAS Hosting

| Service | Source | Persistent path |
| --- | --- | --- |
| synapse-db | `postgres:17` | `/var/lib/postgresql/data` |
| mas-db | `postgres:17` | `/var/lib/postgresql/data` |
| synapse | `templates/matrix/Synapse.Dockerfile` | `/data` |
| mas | `templates/matrix/Mas.Dockerfile` | `/data` |
| matrix | `templates/matrix/Gateway.Dockerfile` | `None` |
| element | `templates/matrix/Element.Dockerfile` | `None` |

Required input before deployment: none; generated secrets and service references supply the template defaults.

## First Use

Choose the final SYNAPSE_SERVER_NAME before the first deployment; Matrix server names are immutable. For a custom domain, configure the gateway domain, MAS public URL, and Element homeserver settings together. Registration starts closed. Use the MAS CLI to create users or deliberately enable REGISTRATION_ENABLED during onboarding, then close it again. The MAS service has its own public HTTPS domain.



## Scope and Limitations

Signing and encryption keys are generated locally on first startup and persist in the service volumes. Federation configuration is included through well-known responses but has not been tested against another homeserver. Voice/video, TURN, UDP networking, bridges, and push infrastructure are not provided. Keep one homeserver and one MAS replica.

## Backups and Upgrades

Back up both PostgreSQL databases, the Synapse /data volume, and the MAS /data volume together. Losing signing/encryption keys or changing the server name can make restoration unusable. Test restoration into an isolated project before depending on the backup. Image rollback alone does not revert database migrations.

## Validation Scope

Upstream delegated-auth configuration and Element runtime paths were checked. Image builds, account creation/login, encrypted two-client messaging, media, federation, and backup/restore remain unverified. Full Railway startup and product workflows remain release gates.

## Why Deploy Matrix Synapse with MAS on Railway?

Railway keeps the services, networking, environment references, deployment logs, and volumes together in one project. This draft supplies a reviewable starting configuration. Railway resources and volume storage are billed separately from external email, model, and other service providers. No deployment cost or revenue estimate has been measured.

## Support and Upstream

[Upstream source and release](https://github.com/element-hq/matrix-authentication-service/tree/v1.24.0). This is an independent community integration; upstream licenses, trademarks, and paid-feature restrictions remain in effect. See the [draft readiness record](https://github.com/orenaksakal/railway-templates/blob/codex/remaining-template-drafts/DRAFTS.md). Report issues with redacted logs and image versions; never share credentials.
