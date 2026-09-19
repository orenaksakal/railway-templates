# Deploy and Host Plik File Sharing

Expiring file sharing with authenticated uploads and persistent metadata.

## About Hosting

| Service | Access | Persistent storage |
| --- | --- | --- |
| plik | Public HTTPS | /data |

Railway provides the public HTTPS endpoint. Dependencies stay on private networking. Keep each volume-backed service at one replica.

## Why Deploy Plik File Sharing on Railway

This definition includes pinned container sources, documented storage paths and generated credentials where required. It restores the missing repository adapters from the previous draft and keeps the application setup steps explicit.

## Common Use Cases

Expiring file sharing with authenticated uploads and persistent metadata.

## First use

No mandatory operator-supplied variables. Retrieve generated credentials from the service variables.

Log in as admin with PLIKD_DEFAULT_ADMIN_PASSWORD. Authentication is required for upload creation; downloads are available via sharing URLs according to each upload policy. The adapter stores metadata in /data/plik.db and files under /data/files.

Where an owner gateway is included, the username is admin. API clients can use `X-Template-Key: YOUR_ACCESS_PASSWORD`. The gateway consumes Basic Authorization, preserves Bearer authorization and WebSocket upgrades, and caps requests at 32 MiB; check compatibility with native clients. Generated credentials must remain private.

## Scope and limitations

Default file size is 100 MB and retention is seven days, with a thirty-day maximum. Platform request limits still apply. The generated administrator is only created when absent. This is root-gg/plik, a different product from Plikshare.

This is a prepared, unpublished draft. Source and static configuration checks are recorded in the repository's preparation report. Container builds, fresh Railway startup, native-client compatibility, full application workflows, backup restoration and costs have not been verified. A proxy healthcheck is not application readiness.

## Acceptance checks

Reject anonymous upload creation, authenticate, upload and download a test file, verify expiration settings, restart, and check stored bytes and metadata.

Verify first use, unauthorized rejection where applicable, and a volume-preserving redeploy. Back up every persistent volume, generated application key and consistent database export. Restore into a separate instance and verify accounts, records and uploaded bytes before using important data. Container rollback does not revert database migrations.

## Dependencies for Plik File Sharing

### Deployment Dependencies

A Railway account with capacity for 1 services, access to the selected registries and repository source, and the inputs listed above. External provider accounts and optional integrations are operator-supplied.

### Source and maintenance

- [Upstream project](https://github.com/root-gg/plik)
- [Reviewed application source](https://github.com/root-gg/plik/tree/ed7f43fbe1bd0a8a3d3365fd83c17c75e9ee4bcc)
- [Deployment adapter](https://github.com/orenaksakal/railway-templates/tree/codex/unique-template-drafts/templates/round9/plik)
- Repository services build from `orenaksakal/railway-templates`, branch `codex/unique-template-drafts`, with repository-root build context. Keep the branch available.
- Image digests and source references are tracked separately. A source revision is not asserted to match a rolling image unless the image metadata establishes it.

Upstream software retains its own license and trademarks. This community integration does not imply endorsement.
