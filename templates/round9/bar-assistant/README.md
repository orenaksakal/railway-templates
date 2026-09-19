# Deploy and Host Bar Assistant + Salt Rim

Cocktail recipes and home-bar inventory with Salt Rim and Meilisearch.

## About Hosting

| Service | Access | Persistent storage |
| --- | --- | --- |
| search | Private | /meili_data |
| web | Private | None |
| bar-assistant | Public HTTPS | None |
| api | Private | /var/www/cocktails/storage/bar-assistant |

Railway provides the public HTTPS endpoint. Dependencies stay on private networking. Keep each volume-backed service at one replica.

## Why Deploy Bar Assistant + Salt Rim on Railway

This definition includes pinned container sources, documented storage paths and generated credentials where required. It restores the missing repository adapters from the previous draft and keeps the application setup steps explicit.

## Common Use Cases

Cocktail recipes and home-bar inventory with Salt Rim and Meilisearch.

## First use

No mandatory operator-supplied variables. Retrieve generated credentials from the service variables.

Authenticate to the gateway as admin with ACCESS_PASSWORD. Register the first application owner in Salt Rim, then disable ALLOW_REGISTRATION before sharing access. The gateway routes /bar/ to the private API, /search/ to authenticated Meilisearch and / to Salt Rim. The generated APP_KEY is preserved on restart.

Where an owner gateway is included, the username is admin. API clients can use `X-Template-Key: YOUR_ACCESS_PASSWORD`. The gateway consumes Basic Authorization, preserves Bearer authorization and WebSocket upgrades, and caps requests at 32 MiB; check compatibility with native clients. Generated credentials must remain private.

## Scope and limitations

All routes require owner gateway access. API clients can send X-Template-Key. Meilisearch also requires its own native key; the gateway never injects the master key. The shared owner gateway is not per-user authorization. No queue worker, SMTP or external storage is configured.

Source and static configuration checks are recorded in the repository's release report. Container builds, fresh Railway startup, native-client compatibility, full application workflows, backup restoration and costs have not been verified. A proxy healthcheck is not application readiness.

## Acceptance checks

Create a bar, add an ingredient and cocktail with a photo, search for it, test access as another user, and restart to verify data, sessions and media survive.

Verify first use, unauthorized rejection where applicable, and a volume-preserving redeploy. Back up every persistent volume, generated application key and consistent database export. Restore into a separate instance and verify accounts, records and uploaded bytes before using important data. Container rollback does not revert database migrations.

## Dependencies for Bar Assistant + Salt Rim

### Deployment Dependencies

A Railway account with capacity for 4 services, access to the selected registries and repository source, and the inputs listed above. External provider accounts and optional integrations are operator-supplied.

### Source and maintenance

- [Upstream project](https://github.com/karlomikus/bar-assistant)
- [Reviewed application source](https://github.com/karlomikus/bar-assistant/tree/b97e215dee11ebffb2dc1e2bfc949876549e098b)
- [Deployment adapter](https://github.com/orenaksakal/railway-templates/tree/codex/unique-template-drafts/templates/round9/bar-assistant)
- Repository services build from `orenaksakal/railway-templates`, branch `codex/unique-template-drafts`, with repository-root build context. Keep the branch available.
- Image digests and source references are tracked separately. A source revision is not asserted to match a rolling image unless the image metadata establishes it.

Upstream software retains its own license and trademarks. This community integration does not imply endorsement.
