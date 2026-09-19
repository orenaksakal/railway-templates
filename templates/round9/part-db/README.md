# Deploy and Host Part-DB

Electronic parts inventory with SQLite, attachments, and persistent media.

## About Hosting

| Service | Access | Persistent storage |
| --- | --- | --- |
| part-db | Public HTTPS | /data |

Railway provides the public HTTPS endpoint. Dependencies stay on private networking. Keep each volume-backed service at one replica.

## Why Deploy Part-DB on Railway

This definition includes pinned container sources, documented storage paths and generated credentials where required. It restores the missing repository adapters from the previous draft and keeps the application setup steps explicit.

## Common Use Cases

Electronic parts inventory with SQLite, attachments, and persistent media.

## First use

No mandatory operator-supplied variables. Retrieve generated credentials from the service variables.

Choose BASE_CURRENCY before first deployment. Sign in as admin using INITIAL_ADMIN_PW after the initial migration completes, then change that password in the application. The adapter initializes the database with upstream migrations and preserves uploads, media and SQLite together under /data.

Where an owner gateway is included, the username is admin. API clients can use `X-Template-Key: YOUR_ACCESS_PASSWORD`. The gateway consumes Basic Authorization, preserves Bearer authorization and WebSocket upgrades, and caps requests at 32 MiB; check compatibility with native clients. Generated credentials must remain private.

## Scope and limitations

One replica with SQLite. Startup applies upstream database migrations; back up before updating the pinned image. Existing administrator passwords are not reset by the adapter. Currency changes do not convert recorded prices.

Source and static configuration checks are recorded in the repository's release report. Container builds, fresh Railway startup, native-client compatibility, full application workflows, backup restoration and costs have not been verified. A proxy healthcheck is not application readiness.

## Acceptance checks

Create a component and storage location, adjust stock, attach a datasheet and image, export data, restart, and verify stock counts and attachment bytes.

Verify first use, unauthorized rejection where applicable, and a volume-preserving redeploy. Back up every persistent volume, generated application key and consistent database export. Restore into a separate instance and verify accounts, records and uploaded bytes before using important data. Container rollback does not revert database migrations.

## Dependencies for Part-DB

### Deployment Dependencies

A Railway account with capacity for 1 services, access to the selected registries and repository source, and the inputs listed above. External provider accounts and optional integrations are operator-supplied.

### Source and maintenance

- [Upstream project](https://github.com/Part-DB/Part-DB-server)
- [Reviewed application source](https://github.com/Part-DB/Part-DB-server/tree/0f0ee60dd887e141c480f9caa30e0d576ce8c99a)
- [Deployment adapter](https://github.com/orenaksakal/railway-templates/tree/codex/unique-template-drafts/templates/round9/part-db)
- Repository services build from `orenaksakal/railway-templates`, branch `codex/unique-template-drafts`, with repository-root build context. Keep the branch available.
- Image digests and source references are tracked separately. A source revision is not asserted to match a rolling image unless the image metadata establishes it.

Upstream software retains its own license and trademarks. This community integration does not imply endorsement.
