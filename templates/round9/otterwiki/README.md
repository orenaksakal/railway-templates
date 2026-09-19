# Deploy and Host An Otter Wiki

Markdown wiki with Git history, attachments, and persistent user accounts.

## About Hosting

| Service | Access | Persistent storage |
| --- | --- | --- |
| otterwiki | Public HTTPS | None |
| app | Private | /app-data |

Railway provides the public HTTPS endpoint. Dependencies stay on private networking. Keep each volume-backed service at one replica.

## Why Deploy An Otter Wiki on Railway

This definition includes pinned container sources, documented storage paths and generated credentials where required. It restores the missing repository adapters from the previous draft and keeps the application setup steps explicit.

## Common Use Cases

Markdown wiki with Git history, attachments, and persistent user accounts.

## First use

- `app.ADMIN_USER_EMAIL`: Email address to use for the first administrator signup behind the gateway.

- `app.ADMIN_USER_EMAIL`: Email address to use for the first administrator signup behind the gateway.

Set ADMIN_USER_EMAIL before deploying. Authenticate to the public gateway with username admin and ACCESS_PASSWORD, then sign up using that email. In Settings, close registration once onboarding is complete. Reads, edits and attachments require approved accounts; email verification is disabled because SMTP is not configured.

Where an owner gateway is included, the username is admin. API clients can use `X-Template-Key: YOUR_ACCESS_PASSWORD`. The gateway consumes Basic Authorization, preserves Bearer authorization and WebSocket upgrades, and caps requests at 32 MiB; check compatibility with native clients. Generated credentials must remain private.

## Scope and limitations

The first administrator signup must be tested behind the gateway. Settings saved in the UI override environment values. The gateway limits requests to 32 MiB. Git-over-HTTP clients need testing with the additional Basic authentication layer.

This is a prepared, unpublished draft. Source and static configuration checks are recorded in the repository's preparation report. Container builds, fresh Railway startup, native-client compatibility, full application workflows, backup restoration and costs have not been verified. A proxy healthcheck is not application readiness.

## Acceptance checks

Register the intended administrator, create and revise a page, upload an attachment, inspect history, approve a second user, and verify everything after restart.

Verify first use, unauthorized rejection where applicable, and a volume-preserving redeploy. Back up every persistent volume, generated application key and consistent database export. Restore into a separate instance and verify accounts, records and uploaded bytes before using important data. Container rollback does not revert database migrations.

## Dependencies for An Otter Wiki

### Deployment Dependencies

A Railway account with capacity for 2 services, access to the selected registries and repository source, and the inputs listed above. External provider accounts and optional integrations are operator-supplied.

### Source and maintenance

- [Upstream project](https://github.com/redimp/otterwiki)
- [Reviewed application source](https://github.com/redimp/otterwiki/tree/623903665d38d7f1c2ef11df007e0e7f313e4cfc)
- [Deployment adapter](https://github.com/orenaksakal/railway-templates/tree/codex/unique-template-drafts/templates/round9/otterwiki)
- Repository services build from `orenaksakal/railway-templates`, branch `codex/unique-template-drafts`, with repository-root build context. Keep the branch available.
- Image digests and source references are tracked separately. A source revision is not asserted to match a rolling image unless the image metadata establishes it.

Upstream software retains its own license and trademarks. This community integration does not imply endorsement.
