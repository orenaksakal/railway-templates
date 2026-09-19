# Deploy and Host Typemill Documentation CMS

Markdown documentation CMS with persistent content and settings.

## About Hosting

| Service | Access | Persistent storage |
| --- | --- | --- |
| typemill | Public HTTPS | None |
| app | Private | /data |

Railway provides the public HTTPS endpoint. Dependencies stay on private networking. Keep each volume-backed service at one replica.

## Why Deploy Typemill Documentation CMS on Railway

This definition includes pinned container sources, documented storage paths and generated credentials where required. It restores the missing repository adapters from the previous draft and keeps the application setup steps explicit.

## Common Use Cases

Markdown documentation CMS with persistent content and settings.

## First use

No mandatory operator-supplied variables. Retrieve generated credentials from the service variables.

Use gateway username admin and ACCESS_PASSWORD, then create your initial Typemill administrator in the setup UI. Configure trusted proxies in Developer settings and create your first document. All seven mutable upstream directories are stored below /data.

Where an owner gateway is included, the username is admin. API clients can use `X-Template-Key: YOUR_ACCESS_PASSWORD`. The gateway consumes Basic Authorization, preserves Bearer authorization and WebSocket upgrades, and caps requests at 32 MiB; check compatibility with native clients. Generated credentials must remain private.

## Scope and limitations

The private gateway applies to readers as well as editors. Optional paid features, plugins and ebook publishing retain their upstream license requirements. The adapter removes upstream multi-volume metadata and keeps runtime state in one volume. SMTP and AI services need separate setup.

This is a prepared, unpublished draft. Source and static configuration checks are recorded in the repository's preparation report. Container builds, fresh Railway startup, native-client compatibility, full application workflows, backup restoration and costs have not been verified. A proxy healthcheck is not application readiness.

## Acceptance checks

Create and publish a Markdown document, upload media, change a setting, restart, and verify content, media and user persistence.

Verify first use, unauthorized rejection where applicable, and a volume-preserving redeploy. Back up every persistent volume, generated application key and consistent database export. Restore into a separate instance and verify accounts, records and uploaded bytes before using important data. Container rollback does not revert database migrations.

## Dependencies for Typemill Documentation CMS

### Deployment Dependencies

A Railway account with capacity for 2 services, access to the selected registries and repository source, and the inputs listed above. External provider accounts and optional integrations are operator-supplied.

### Source and maintenance

- [Upstream project](https://github.com/typemill/typemill)
- [Reviewed application source](https://github.com/typemill/typemill/tree/52f88d278743bcb1cca64bc7a2b4ac7ce8c6a32b)
- [Deployment adapter](https://github.com/orenaksakal/railway-templates/tree/codex/unique-template-drafts/templates/round9/typemill)
- Repository services build from `orenaksakal/railway-templates`, branch `codex/unique-template-drafts`, with repository-root build context. Keep the branch available.
- Image digests and source references are tracked separately. A source revision is not asserted to match a rolling image unless the image metadata establishes it.

Upstream software retains its own license and trademarks. This community integration does not imply endorsement.
