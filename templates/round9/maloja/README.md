# Deploy and Host Maloja Listening Statistics

Personal music scrobbling and listening statistics with persistent storage.

## About Hosting

| Service | Access | Persistent storage |
| --- | --- | --- |
| maloja | Public HTTPS | /mljdata |

Railway provides the public HTTPS endpoint. Dependencies stay on private networking. Keep each volume-backed service at one replica.

## Why Deploy Maloja Listening Statistics on Railway

This definition includes pinned container sources, documented storage paths and generated credentials where required. It restores the missing repository adapters from the previous draft and keeps the application setup steps explicit.

## Common Use Cases

Personal music scrobbling and listening statistics with persistent storage.

## First use

No mandatory operator-supplied variables. Retrieve generated credentials from the service variables.

Open the public site and enter admin mode using MALOJA_FORCE_PASSWORD. Create a separate API key for each scrobbling client in the administration UI. Import an existing supported listening-history export if desired.

Where an owner gateway is included, the username is admin. API clients can use `X-Template-Key: YOUR_ACCESS_PASSWORD`. The gateway consumes Basic Authorization, preserves Bearer authorization and WebSocket upgrades, and caps requests at 32 MiB; check compatibility with native clients. Generated credentials must remain private.

## Scope and limitations

Listening statistics are public by default; administrative changes require the configured password. This is a single-owner statistics service, not a music player. Last.fm and Spotify artwork integrations require operator API credentials. The latest image is frozen by digest.

This is a prepared, unpublished draft. Source and static configuration checks are recorded in the repository's preparation report. Container builds, fresh Railway startup, native-client compatibility, full application workflows, backup restoration and costs have not been verified. A proxy healthcheck is not application readiness.

## Acceptance checks

Enter admin mode, submit a scrobble with an API key, verify charts show it, restart and verify retained history. Reject requests with an invalid key.

Verify first use, unauthorized rejection where applicable, and a volume-preserving redeploy. Back up every persistent volume, generated application key and consistent database export. Restore into a separate instance and verify accounts, records and uploaded bytes before using important data. Container rollback does not revert database migrations.

## Dependencies for Maloja Listening Statistics

### Deployment Dependencies

A Railway account with capacity for 1 services, access to the selected registries and repository source, and the inputs listed above. External provider accounts and optional integrations are operator-supplied.

### Source and maintenance

- [Upstream project](https://github.com/krateng/maloja)
- [Reviewed application source](https://github.com/krateng/maloja/tree/52aae997fb6b8ad62c65498f4e91e7d65fbe242d)
- [Deployment adapter](https://github.com/orenaksakal/railway-templates/tree/codex/unique-template-drafts/templates/round9/maloja)
- Repository services build from `orenaksakal/railway-templates`, branch `codex/unique-template-drafts`, with repository-root build context. Keep the branch available.
- Image digests and source references are tracked separately. A source revision is not asserted to match a rolling image unless the image metadata establishes it.

Upstream software retains its own license and trademarks. This community integration does not imply endorsement.
