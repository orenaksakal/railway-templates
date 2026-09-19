# Deploy and Host Bludit CMS

Flat-file website CMS with persistent content, themes and plugins.

## About Hosting

| Service | Access | Persistent storage |
| --- | --- | --- |
| app | Private | /data |
| bludit | Public HTTPS | None |

Railway provides the public HTTPS endpoint. Dependencies stay on private networking. Keep each volume-backed service at one replica.

## Why Deploy Bludit CMS on Railway

This definition includes pinned container sources, documented storage paths and generated credentials where required. It restores the missing repository adapters from the previous draft and keeps the application setup steps explicit.

## Common Use Cases

Flat-file website CMS with persistent content, themes and plugins.

## First use

No mandatory operator-supplied variables. Retrieve generated credentials from the service variables.

Authenticate to the private gateway with username admin and ACCESS_PASSWORD, then complete the Bludit installer and choose your administrator credentials. Publish a page from /admin. This template is a private CMS by default because the gateway protects the entire site.

Where an owner gateway is included, the username is admin. API clients can use `X-Template-Key: YOUR_ACCESS_PASSWORD`. The gateway consumes Basic Authorization, preserves Bearer authorization and WebSocket upgrades, and caps requests at 32 MiB; check compatibility with native clients. Generated credentials must remain private.

## Scope and limitations

The official digest-pinned Docker image currently contains Bludit 3.20.0, although the repository has a newer 3.22.0 release. No claim of deploying the latest source release is made. Data, themes and plugins share /data. Public-site access requires an intentional gateway policy change after setup. The official Docker image selected here is 3.20.0, while the saved application documentation reference is 3.22.0; no version equivalence is claimed. Debug mode is disabled by the adapter.

This is a prepared, unpublished draft. Source and static configuration checks are recorded in the repository's preparation report. Container builds, fresh Railway startup, native-client compatibility, full application workflows, backup restoration and costs have not been verified. A proxy healthcheck is not application readiness.

## Acceptance checks

Complete installation, publish and edit a page, upload an image, restart, and verify both published content and administrator login.

Verify first use, unauthorized rejection where applicable, and a volume-preserving redeploy. Back up every persistent volume, generated application key and consistent database export. Restore into a separate instance and verify accounts, records and uploaded bytes before using important data. Container rollback does not revert database migrations.

## Dependencies for Bludit CMS

### Deployment Dependencies

A Railway account with capacity for 2 services, access to the selected registries and repository source, and the inputs listed above. External provider accounts and optional integrations are operator-supplied.

### Source and maintenance

- [Upstream project](https://github.com/bludit/bludit)
- [Reviewed application source](https://github.com/bludit/bludit/tree/c573a995a97dc80bf4eadd454f466d7a6ad2bba0)
- [Deployment adapter](https://github.com/orenaksakal/railway-templates/tree/codex/unique-template-drafts/templates/round9/bludit)
- Repository services build from `orenaksakal/railway-templates`, branch `codex/unique-template-drafts`, with repository-root build context. Keep the branch available.
- Image digests and source references are tracked separately. A source revision is not asserted to match a rolling image unless the image metadata establishes it.

Upstream software retains its own license and trademarks. This community integration does not imply endorsement.
