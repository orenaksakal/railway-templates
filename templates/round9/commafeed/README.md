# Deploy and Host CommaFeed

Self-hosted RSS reader with PostgreSQL and private gateway access.

## About Hosting

| Service | Access | Persistent storage |
| --- | --- | --- |
| commafeed | Public HTTPS | None |
| app | Private | None |
| postgres | Private | /var/lib/postgresql/data |

Railway provides the public HTTPS endpoint. Dependencies stay on private networking. Keep each volume-backed service at one replica.

## Why Deploy CommaFeed on Railway

This definition includes pinned container sources, documented storage paths and generated credentials where required. It restores the missing repository adapters from the previous draft and keeps the application setup steps explicit.

## Common Use Cases

Self-hosted RSS reader with PostgreSQL and private gateway access.

## First use

No mandatory operator-supplied variables. Retrieve generated credentials from the service variables.

No mandatory operator-supplied variables. Generated credentials are available in service variables after deployment.

Open the public gateway using ACCESS_USER and ACCESS_PASSWORD from its variables. Sign in to CommaFeed with the upstream initial admin/admin account and immediately change its password. Public self-registration and demo accounts are disabled. Add feeds or import OPML.

Where an owner gateway is included, the username is admin. API clients can use `X-Template-Key: YOUR_ACCESS_PASSWORD`. The gateway consumes Basic Authorization, preserves Bearer authorization and WebSocket upgrades, and caps requests at 32 MiB; check compatibility with native clients. Generated credentials must remain private.

## Scope and limitations

The gateway protects the initial default account. Native RSS clients must support the additional HTTP Basic credentials. SMTP/password recovery is not configured. Feed fetching requires outbound Internet access.

This is a prepared, unpublished draft. Source and static configuration checks are recorded in the repository's preparation report. Container builds, fresh Railway startup, native-client compatibility, full application workflows, backup restoration and costs have not been verified. A proxy healthcheck is not application readiness.

## Acceptance checks

Import an OPML file, refresh a feed, mark an entry read, star an entry, restart both services, and verify subscriptions and reading state persist.

Verify first use, unauthorized rejection where applicable, and a volume-preserving redeploy. Back up every persistent volume, generated application key and consistent database export. Restore into a separate instance and verify accounts, records and uploaded bytes before using important data. Container rollback does not revert database migrations.

## Dependencies for CommaFeed

### Deployment Dependencies

A Railway account with capacity for 3 services, access to the selected registries and repository source, and the inputs listed above. External provider accounts and optional integrations are operator-supplied.

### Source and maintenance

- [Upstream project](https://github.com/Athou/commafeed)
- [Reviewed application source](https://github.com/Athou/commafeed/tree/689c20d3672dce9e6bc40f64f737b38a66db2aa0)
- [Deployment adapter](https://github.com/orenaksakal/railway-templates/tree/codex/unique-template-drafts/templates/round9/commafeed)
- Repository services build from `orenaksakal/railway-templates`, branch `codex/unique-template-drafts`, with repository-root build context. Keep the branch available.
- Image digests and source references are tracked separately. A source revision is not asserted to match a rolling image unless the image metadata establishes it.

Upstream software retains its own license and trademarks. This community integration does not imply endorsement.
