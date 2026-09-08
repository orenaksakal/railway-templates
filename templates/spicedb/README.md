# Deploy and Host SpiceDB with PostgreSQL on Railway

SpiceDB 1.56.1 provides relationship-based authorization backed by a dedicated PostgreSQL database. The startup adapter migrates the datastore before serving and retries while a cold database becomes available.

> Unpublished draft. This template is prepared for review; it has not been deployed on Railway or certified for production. See the validation scope below.

## About Hosting SpiceDB with PostgreSQL

The template defines 2 services with pinned container digests, generated deployment secrets, explicit service references, and persistent volumes for stateful dependencies. Repository-backed adapters build from `codex/remaining-template-drafts`. Railway terminates HTTPS for the public endpoints; databases and internal workers have no public TCP proxies. Services initialize independently, so cold-start and migration behavior must be verified in a new test project. Each deployment has its own database and storage resources. Backups are not scheduled by this template, and filesystem-backed services should remain single-replica.

## Common Use Cases

- Check resource permissions from application backends.
- Model team membership and shared-document access.
- Store relationships separately from application business data.

## Dependencies for SpiceDB with PostgreSQL Hosting

| Service | Source | Persistent path |
| --- | --- | --- |
| postgres | `postgres:17` | `/var/lib/postgresql/data` |
| spicedb | `templates/spicedb/Dockerfile` | `None` |

Required input before deployment: none; generated secrets and service references supply the template defaults.

## First Use

Read `SPICEDB_GRPC_PRESHARED_KEY` from the spicedb service. Use the Railway HTTPS domain for the authenticated HTTP gateway; gRPC listens privately on port 50051. Write a schema and relationships, then perform a permission check. Keep the API key on trusted servers.

The HTTP API accepts `Authorization: Bearer <SPICEDB_GRPC_PRESHARED_KEY>`. Start with the upstream [HTTP API guide](https://authzed.com/docs/spicedb/getting-started/protecting-a-blog) and its matching schema and relationship examples.

## Scope and Limitations

Public raw gRPC and a public TCP proxy are not configured. Private gRPC is authenticated but uses the private network transport. The preshared key grants administrative API access and must not be placed in a browser application.

## Backups and Upgrades

Back up PostgreSQL and retain the preshared key. Review upstream migration compatibility before changing image versions. Test restoration into an isolated project before depending on the backup. Image rollback alone does not revert database migrations.

## Validation Scope

Image digest and static configuration verified. Live migration, schema write, relationship write, permission check, and upgrade/recovery tests remain required. Full Railway startup and product workflows remain release gates.

## Why Deploy SpiceDB with PostgreSQL on Railway?

Railway keeps the services, networking, environment references, deployment logs, and volumes together in one project. This draft supplies a reviewable starting configuration. Railway resources and volume storage are billed separately from external email, model, and other service providers. No deployment cost or revenue estimate has been measured.

## Support and Upstream

[Upstream source and release](https://github.com/authzed/spicedb/tree/v1.56.1). This is an independent community integration; upstream licenses, trademarks, and paid-feature restrictions remain in effect. See the [draft readiness record](https://github.com/orenaksakal/railway-templates/blob/codex/remaining-template-drafts/DRAFTS.md). Report issues with redacted logs and image versions; never share credentials.
