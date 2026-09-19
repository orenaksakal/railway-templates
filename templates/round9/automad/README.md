# Deploy and Host Automad CMS v2

Flat-file visual CMS with a persistent site and a protected editor setup.

## About Hosting

| Service | Access | Persistent storage |
| --- | --- | --- |
| automad | Public HTTPS | None |
| app | Private | /app |

Railway provides the public HTTPS endpoint. Dependencies stay on private networking. Keep each volume-backed service at one replica.

## Why Deploy Automad CMS v2 on Railway

This definition includes pinned container sources, documented storage paths and generated credentials where required. It restores the missing repository adapters from the previous draft and keeps the application setup steps explicit.

## Common Use Cases

Flat-file visual CMS with a persistent site and a protected editor setup.

## First use

No mandatory operator-supplied variables. Retrieve generated credentials from the service variables.

Authenticate to the gateway, then follow the Automad dashboard setup at /dashboard. Check application logs for any generated first-run credentials. The image installs its exact AUTOMAD_VERSION into /app on the first boot.

Where an owner gateway is included, the username is admin. API clients can use `X-Template-Key: YOUR_ACCESS_PASSWORD`. The gateway consumes Basic Authorization, preserves Bearer authorization and WebSocket upgrades, and caps requests at 32 MiB; check compatibility with native clients. Generated credentials must remain private.

## Scope and limitations

This uses upstream v2 beta (2.0.0-beta.58) and is explicitly a beta deployment. First boot needs outbound Composer/package access. The whole /app site is persistent; upgrading the container does not automatically replace the existing site. The gateway makes the entire site private.

This is a prepared, unpublished draft. Source and static configuration checks are recorded in the repository's preparation report. Container builds, fresh Railway startup, native-client compatibility, full application workflows, backup restoration and costs have not been verified. A proxy healthcheck is not application readiness.

## Acceptance checks

Initialize the dashboard, create a page with an image, publish it, restart, and verify content and account persistence.

Verify first use, unauthorized rejection where applicable, and a volume-preserving redeploy. Back up every persistent volume, generated application key and consistent database export. Restore into a separate instance and verify accounts, records and uploaded bytes before using important data. Container rollback does not revert database migrations.

## Dependencies for Automad CMS v2

### Deployment Dependencies

A Railway account with capacity for 2 services, access to the selected registries and repository source, and the inputs listed above. External provider accounts and optional integrations are operator-supplied.

### Source and maintenance

- [Upstream project](https://github.com/marcantondahmen/automad)
- [Reviewed application source](https://github.com/marcantondahmen/automad/tree/1272edbbc54a8b9634fe0759d2a12fdb26a825ce)
- [Deployment adapter](https://github.com/orenaksakal/railway-templates/tree/codex/unique-template-drafts/templates/round9/automad)
- Repository services build from `orenaksakal/railway-templates`, branch `codex/unique-template-drafts`, with repository-root build context. Keep the branch available.
- Image digests and source references are tracked separately. A source revision is not asserted to match a rolling image unless the image metadata establishes it.

Upstream software retains its own license and trademarks. This community integration does not imply endorsement.
