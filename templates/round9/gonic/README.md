# Deploy and Host Gonic Music Server

Subsonic music and podcast server with persistent library storage.

## About Hosting

| Service | Access | Persistent storage |
| --- | --- | --- |
| app | Private | /data |
| gonic | Public HTTPS | None |

Railway provides the public HTTPS endpoint. Dependencies stay on private networking. Keep each volume-backed service at one replica.

## Why Deploy Gonic Music Server on Railway

This definition includes pinned container sources, documented storage paths and generated credentials where required. It restores the missing repository adapters from the previous draft and keeps the application setup steps explicit.

## Common Use Cases

Subsonic music and podcast server with persistent library storage.

## First use

No mandatory operator-supplied variables. Retrieve generated credentials from the service variables.

Use the outer gateway username admin and ACCESS_PASSWORD, then change the upstream admin/admin login. Copy your own music into /data/music through Railway SSH or a controlled volume import; scan it from the administration UI. There is no bundled music or browser upload tool.

Where an owner gateway is included, the username is admin. API clients can use `X-Template-Key: YOUR_ACCESS_PASSWORD`. The gateway consumes Basic Authorization, preserves Bearer authorization and WebSocket upgrades, and caps requests at 32 MiB; check compatibility with native clients. Generated credentials must remain private.

## Scope and limitations

The gateway protects initial credentials. Subsonic clients must support additional HTTP Basic authentication; client compatibility is not yet verified. No sound device or jukebox is supplied. Cache, playlists, podcasts and the database are colocated on /data.

Source and static configuration checks are recorded in the repository's release report. Container builds, fresh Railway startup, native-client compatibility, full application workflows, backup restoration and costs have not been verified. A proxy healthcheck is not application readiness.

## Acceptance checks

Import a licensed test track, scan, authenticate a Subsonic client, stream the track, create a playlist, and verify playback metadata and files after restart.

Verify first use, unauthorized rejection where applicable, and a volume-preserving redeploy. Back up every persistent volume, generated application key and consistent database export. Restore into a separate instance and verify accounts, records and uploaded bytes before using important data. Container rollback does not revert database migrations.

## Dependencies for Gonic Music Server

### Deployment Dependencies

A Railway account with capacity for 2 services, access to the selected registries and repository source, and the inputs listed above. External provider accounts and optional integrations are operator-supplied.

### Source and maintenance

- [Upstream project](https://github.com/sentriz/gonic)
- [Reviewed application source](https://github.com/sentriz/gonic/tree/5ae99e8af550e4d5cbd45a3b430419d32cb54aed)
- [Deployment adapter](https://github.com/orenaksakal/railway-templates/tree/codex/unique-template-drafts/templates/round9/gonic)
- Repository services build from `orenaksakal/railway-templates`, branch `codex/unique-template-drafts`, with repository-root build context. Keep the branch available.
- Image digests and source references are tracked separately. A source revision is not asserted to match a rolling image unless the image metadata establishes it.

Upstream software retains its own license and trademarks. This community integration does not imply endorsement.
