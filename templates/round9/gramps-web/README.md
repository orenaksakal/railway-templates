# Deploy and Host Gramps Web

Family history with persistent trees, media and background jobs.

## About Hosting

| Service | Access | Persistent storage |
| --- | --- | --- |
| gramps-web | Public HTTPS | /data |
| redis | Private | /data |

Railway provides the public HTTPS endpoint. Dependencies stay on private networking. Keep each volume-backed service at one replica.

## Why Deploy Gramps Web on Railway

This definition includes pinned container sources, documented storage paths and generated credentials where required. It restores the missing repository adapters from the previous draft and keeps the application setup steps explicit.

## Common Use Cases

Family history with persistent trees, media and background jobs.

## First use

- `gramps-web.OWNER_EMAIL`: Email for the initial Gramps Web owner.

Set OWNER_EMAIL and retrieve OWNER_PASSWORD. Sign in as owner. The adapter creates the owner before opening HTTP, initializes user database migrations, and runs one Celery worker with two web workers. Import a Gramps XML family tree or create one in the UI.

Where an owner gateway is included, the username is admin. API clients can use `X-Template-Key: YOUR_ACCESS_PASSWORD`. The gateway consumes Basic Authorization, preserves Bearer authorization and WebSocket upgrades, and caps requests at 32 MiB; check compatibility with native clients. Generated credentials must remain private.

## Scope and limitations

Web and one Celery worker share the same /data volume. The upstream entrypoint migrates the user database before owner creation; the adapter creates an owner only when no user exists. The web/API bootstrap interface requires a deployment check on the pinned image. Redis is private and authenticated. SMTP, external providers, S3 and multi-tree administration are not configured.

This is a prepared, unpublished draft. Source and static configuration checks are recorded in the repository's preparation report. Container builds, fresh Railway startup, native-client compatibility, full application workflows, backup restoration and costs have not been verified. A proxy healthcheck is not application readiness.

## Acceptance checks

Log in as owner, create two people and a relationship, upload a photo, run an export through the worker, and verify the tree and photo survive a redeploy.

Verify first use, unauthorized rejection where applicable, and a volume-preserving redeploy. Back up every persistent volume, generated application key and consistent database export. Restore into a separate instance and verify accounts, records and uploaded bytes before using important data. Container rollback does not revert database migrations.

## Dependencies for Gramps Web

### Deployment Dependencies

A Railway account with capacity for 2 services, access to the selected registries and repository source, and the inputs listed above. External provider accounts and optional integrations are operator-supplied.

### Source and maintenance

- [Upstream project](https://github.com/gramps-project/gramps-web)
- [Reviewed application source](https://github.com/gramps-project/gramps-web/tree/4bc259a027ac4854338728cd1f7cf49c4700758a)
- [Deployment adapter](https://github.com/orenaksakal/railway-templates/tree/codex/unique-template-drafts/templates/round9/gramps-web)
- Repository services build from `orenaksakal/railway-templates`, branch `codex/unique-template-drafts`, with repository-root build context. Keep the branch available.
- Image digests and source references are tracked separately. A source revision is not asserted to match a rolling image unless the image metadata establishes it.

Upstream software retains its own license and trademarks. This community integration does not imply endorsement.
