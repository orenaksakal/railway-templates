# Deploy and Host Jellystat

Jellyfin viewing statistics with PostgreSQL and persistent backup storage.

## About Hosting

| Service | Access | Persistent storage |
| --- | --- | --- |
| jellystat | Public HTTPS | /app/backend/backup-data |
| postgres | Private | /var/lib/postgresql/data |

Railway provides the public HTTPS endpoint. Dependencies stay on private networking. Keep each volume-backed service at one replica.

## Why Deploy Jellystat on Railway

This definition includes pinned container sources, documented storage paths and generated credentials where required. It restores the missing repository adapters from the previous draft and keeps the application setup steps explicit.

## Common Use Cases

Jellyfin viewing statistics with PostgreSQL and persistent backup storage.

## First use

No mandatory operator-supplied variables. Retrieve generated credentials from the service variables.

Sign in using JS_USER=admin and the generated JS_PASSWORD. Connect your existing reachable Jellyfin server and its API key in the setup UI. PostgreSQL connection details are preconfigured; backups persist under /app/backend/backup-data.

Where an owner gateway is included, the username is admin. API clients can use `X-Template-Key: YOUR_ACCESS_PASSWORD`. The gateway consumes Basic Authorization, preserves Bearer authorization and WebSocket upgrades, and caps requests at 32 MiB; check compatibility with native clients. Generated credentials must remain private.

## Scope and limitations

An external Jellyfin or Emby server is required for useful statistics and is not included. Upstream describes the current generation as under redevelopment; existing functionality should be validated against your server. API keys, media playback and server-specific integration remain operator-supplied.

This is a prepared, unpublished draft. Source and static configuration checks are recorded in the repository's preparation report. Container builds, fresh Railway startup, native-client compatibility, full application workflows, backup restoration and costs have not been verified. A proxy healthcheck is not application readiness.

## Acceptance checks

Log in, connect a test Jellyfin server, sync a library, record playback, verify history, create a backup and verify data after restart.

Verify first use, unauthorized rejection where applicable, and a volume-preserving redeploy. Back up every persistent volume, generated application key and consistent database export. Restore into a separate instance and verify accounts, records and uploaded bytes before using important data. Container rollback does not revert database migrations.

## Dependencies for Jellystat

### Deployment Dependencies

A Railway account with capacity for 2 services, access to the selected registries and repository source, and the inputs listed above. External provider accounts and optional integrations are operator-supplied.

### Source and maintenance

- [Upstream project](https://github.com/CyferShepard/Jellystat)
- [Reviewed application source](https://github.com/CyferShepard/Jellystat/tree/10678476792bc88700c574b97d09f300f47f7291)
- [Deployment adapter](https://github.com/orenaksakal/railway-templates/tree/codex/unique-template-drafts/templates/round9/jellystat)
- Repository services build from `orenaksakal/railway-templates`, branch `codex/unique-template-drafts`, with repository-root build context. Keep the branch available.
- Image digests and source references are tracked separately. A source revision is not asserted to match a rolling image unless the image metadata establishes it.

Upstream software retains its own license and trademarks. This community integration does not imply endorsement.
