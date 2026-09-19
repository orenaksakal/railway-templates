# Deploy and Host bewCloud Personal Cloud

Personal files, notes, feeds, photos, and expenses with PostgreSQL.

## About Hosting

| Service | Access | Persistent storage |
| --- | --- | --- |
| app | Private | /app/data-files |
| postgres | Private | /var/lib/postgresql/data |
| bewcloud | Public HTTPS | None |

Railway provides the public HTTPS endpoint. Dependencies stay on private networking. Keep each volume-backed service at one replica.

## Why Deploy bewCloud Personal Cloud on Railway

This definition includes pinned container sources, documented storage paths and generated credentials where required. It restores the missing repository adapters from the previous draft and keeps the application setup steps explicit.

## Common Use Cases

Personal files, notes, feeds, photos, and expenses with PostgreSQL.

## First use

No mandatory operator-supplied variables. Retrieve generated credentials from the service variables.

Open the gateway using username admin and ACCESS_PASSWORD, then create the first bewCloud administrator. Later public signup is disabled. PUBLIC_URL configures the HTTPS origin. Startup runs the upstream database migrations before the application; uploaded files live in /app/data-files and account data in PostgreSQL.

Where an owner gateway is included, the username is admin. API clients can use `X-Template-Key: YOUR_ACCESS_PASSWORD`. The gateway consumes Basic Authorization, preserves Bearer authorization and WebSocket upgrades, and caps requests at 32 MiB; check compatibility with native clients. Generated credentials must remain private.

## Scope and limitations

Contacts and calendar apps are excluded because Radicale is not bundled. Public file sharing is disabled. DAV clients must account for the extra gateway authentication; Basic Authorization is consumed by the gateway. Optional SMTP and external providers require separate setup.

This is a prepared, unpublished draft. Source and static configuration checks are recorded in the repository's preparation report. Container builds, fresh Railway startup, native-client compatibility, full application workflows, backup restoration and costs have not been verified. A proxy healthcheck is not application readiness.

## Acceptance checks

Create the administrator, upload and download a file, create a note and feed subscription, add an expense, restart, and confirm account, database records and files survive.

Verify first use, unauthorized rejection where applicable, and a volume-preserving redeploy. Back up every persistent volume, generated application key and consistent database export. Restore into a separate instance and verify accounts, records and uploaded bytes before using important data. Container rollback does not revert database migrations.

## Dependencies for bewCloud Personal Cloud

### Deployment Dependencies

A Railway account with capacity for 3 services, access to the selected registries and repository source, and the inputs listed above. External provider accounts and optional integrations are operator-supplied.

### Source and maintenance

- [Upstream project](https://github.com/bewcloud/bewcloud)
- [Reviewed application source](https://github.com/bewcloud/bewcloud/tree/bdc439123c4703ad87efcf035111a335af616b82)
- [Deployment adapter](https://github.com/orenaksakal/railway-templates/tree/codex/unique-template-drafts/templates/round9/bewcloud)
- Repository services build from `orenaksakal/railway-templates`, branch `codex/unique-template-drafts`, with repository-root build context. Keep the branch available.
- Image digests and source references are tracked separately. A source revision is not asserted to match a rolling image unless the image metadata establishes it.

Upstream software retains its own license and trademarks. This community integration does not imply endorsement.
