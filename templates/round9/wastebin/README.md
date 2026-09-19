# Deploy and Host Wastebin

Lightweight Rust pastebin with SQLite persistence and authenticated access.

## About Hosting

| Service | Access | Persistent storage |
| --- | --- | --- |
| wastebin | Public HTTPS | None |
| app | Private | /data |

Railway provides the public HTTPS endpoint. Dependencies stay on private networking. Keep each volume-backed service at one replica.

## Why Deploy Wastebin on Railway

This definition includes pinned container sources, documented storage paths and generated credentials where required. It restores the missing repository adapters from the previous draft and keeps the application setup steps explicit.

## Common Use Cases

Lightweight Rust pastebin with SQLite persistence and authenticated access.

## First use

No mandatory operator-supplied variables. Retrieve generated credentials from the service variables.

No mandatory operator-supplied variables. Generated credentials are available in service variables after deployment.

Use the public gateway credentials ACCESS_USER and ACCESS_PASSWORD. Create a paste in the UI or POST JSON to / using HTTP Basic authentication. Keep WASTEBIN_SIGNING_KEY and WASTEBIN_PASSWORD_SALT with the database backup.

Where an owner gateway is included, the username is admin. API clients can use `X-Template-Key: YOUR_ACCESS_PASSWORD`. The gateway consumes Basic Authorization, preserves Bearer authorization and WebSocket upgrades, and caps requests at 32 MiB; check compatibility with native clients. Generated credentials must remain private.

## Scope and limitations

This is a private shared-credential pastebin. Upstream has no account or administration system. The scratch image runs with RAILWAY_RUN_UID=0 to write the volume. Paste payloads are limited to 1 MiB; files are not supported.

This is a prepared, unpublished draft. Source and static configuration checks are recorded in the repository's preparation report. Container builds, fresh Railway startup, native-client compatibility, full application workflows, backup restoration and costs have not been verified. A proxy healthcheck is not application readiness.

## Acceptance checks

Create and retrieve a paste, verify syntax highlighting, delete an owned paste, test password and expiration behavior, and retrieve a surviving paste after a redeploy.

Verify first use, unauthorized rejection where applicable, and a volume-preserving redeploy. Back up every persistent volume, generated application key and consistent database export. Restore into a separate instance and verify accounts, records and uploaded bytes before using important data. Container rollback does not revert database migrations.

## Dependencies for Wastebin

### Deployment Dependencies

A Railway account with capacity for 2 services, access to the selected registries and repository source, and the inputs listed above. External provider accounts and optional integrations are operator-supplied.

### Source and maintenance

- [Upstream project](https://github.com/matze/wastebin)
- [Reviewed application source](https://github.com/matze/wastebin/tree/dfca1dc82b78394d8e2dfe209d9ef3fb539da605)
- [Deployment adapter](https://github.com/orenaksakal/railway-templates/tree/codex/unique-template-drafts/templates/round9/wastebin)
- Repository services build from `orenaksakal/railway-templates`, branch `codex/unique-template-drafts`, with repository-root build context. Keep the branch available.
- Image digests and source references are tracked separately. A source revision is not asserted to match a rolling image unless the image metadata establishes it.

Upstream software retains its own license and trademarks. This community integration does not imply endorsement.
