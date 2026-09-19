# Deploy and Host Errbit

Airbrake-compatible error tracking with MongoDB and generated owner access.

## About Hosting

| Service | Access | Persistent storage |
| --- | --- | --- |
| mongo | Private | /data/db |
| errbit | Public HTTPS | None |

Railway provides the public HTTPS endpoint. Dependencies stay on private networking. Keep each volume-backed service at one replica.

## Why Deploy Errbit on Railway

This definition includes pinned container sources, documented storage paths and generated credentials where required. It restores the missing repository adapters from the previous draft and keeps the application setup steps explicit.

## Common Use Cases

Airbrake-compatible error tracking with MongoDB and generated owner access.

## First use

- `errbit.ERRBIT_ADMIN_EMAIL`: Required initial administrator email address.

- `errbit.ERRBIT_ADMIN_EMAIL`: Required initial administrator email address.

Set ERRBIT_ADMIN_EMAIL before deploying. The bootstrap creates one administrator only if no user exists; use ERRBIT_ADMIN_PASSWORD to sign in. Create an application and configure an Airbrake-compatible notifier with its API key and this instance URL.

Where an owner gateway is included, the username is admin. API clients can use `X-Template-Key: YOUR_ACCESS_PASSWORD`. The gateway consumes Basic Authorization, preserves Bearer authorization and WebSocket upgrades, and caps requests at 32 MiB; check compatibility with native clients. Generated credentials must remain private.

## Scope and limitations

The current official latest image is frozen by digest. The bootstrap intentionally avoids upstream db:seed, which resets and prints the admin password. Existing passwords are not reset on restart. MongoDB is private and authenticated. Email, OAuth, external issue trackers and scheduled retention cleanup require additional setup.

This is a prepared, unpublished draft. Source and static configuration checks are recorded in the repository's preparation report. Container builds, fresh Railway startup, native-client compatibility, full application workflows, backup restoration and costs have not been verified. A proxy healthcheck is not application readiness.

## Acceptance checks

Log in, create an app, submit a real Airbrake notice, verify grouping and backtrace rendering, resolve it, redeploy, and confirm user credentials and notices persist.

Verify first use, unauthorized rejection where applicable, and a volume-preserving redeploy. Back up every persistent volume, generated application key and consistent database export. Restore into a separate instance and verify accounts, records and uploaded bytes before using important data. Container rollback does not revert database migrations.

## Dependencies for Errbit

### Deployment Dependencies

A Railway account with capacity for 2 services, access to the selected registries and repository source, and the inputs listed above. External provider accounts and optional integrations are operator-supplied.

### Source and maintenance

- [Upstream project](https://github.com/errbit/errbit)
- [Reviewed application source](https://github.com/errbit/errbit/tree/fa7ae712a89b115c0229675642bbe4eb2b9cfc9b)
- [Deployment adapter](https://github.com/orenaksakal/railway-templates/tree/codex/unique-template-drafts/templates/round9/errbit)
- Repository services build from `orenaksakal/railway-templates`, branch `codex/unique-template-drafts`, with repository-root build context. Keep the branch available.
- Image digests and source references are tracked separately. A source revision is not asserted to match a rolling image unless the image metadata establishes it.

Upstream software retains its own license and trademarks. This community integration does not imply endorsement.
