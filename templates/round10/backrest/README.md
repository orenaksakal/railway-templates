# Deploy and Host Backrest Repository Manager

Manage restic repositories, browse snapshots and restore files privately.

## About Hosting

Backrest 1.14.1 wraps restic with a browser interface for repositories, snapshots, maintenance and restores. This deployment is useful as a private console for remote restic repositories or data explicitly staged in this service.

| Service | Access | Persistent storage |
| --- | --- | --- |
| core | Private | /data |
| backrest | Public HTTPS | None |

Railway terminates public TLS. Keep volume-backed services at one replica. Database and core application ports are private; only the generated owner gateway is public.

## Why Deploy Backrest Repository Manager on Railway

This integration supplies pinned image sources, private dependencies, persistent storage and an authenticated setup path. Public marketplace searches found no matching product listing at preparation time; the repository records the queries and exclusions.

## Common Use Cases

Browse and maintain remote restic repositories, inspect backup history, restore selected files and manage backup plans for explicitly staged service data.

## First use

Open the gateway using its generated ACCESS_PASSWORD and username admin. Complete Backrest onboarding and create a separate application account. Add an existing remote restic repository or create one with your own S3, B2, SFTP or other supported storage credentials and repository password. Use a dedicated test repository first; never initialize over an existing repository. Configure a backup plan only for paths that actually exist inside this container.

The owner gateway username is `admin`; retrieve its generated `ACCESS_PASSWORD` from Railway variables. API clients can send `X-Template-Key: YOUR_ACCESS_PASSWORD`. This preserves Bearer authorization; browser HTTP Basic credentials are consumed by the gateway. Keep all generated secrets private.

After gateway authentication, successful page responses set a Secure, HttpOnly owner cookie. This lets browser apps send their native API authorization while retaining gateway access. Rotating `ACCESS_PASSWORD` invalidates existing owner cookies. API clients can continue using `X-Template-Key`.

## Scope and limitations

The service cannot see your laptop, NAS, other Railway services or their volumes. It does not back up the Railway workspace automatically. To back up local files, explicitly copy them into a directory such as /data/inbox through an authenticated administrative connection, or use a separate source host. No Docker socket, privileged mounts, FUSE or host filesystems are provided. Repository maintenance and restore downloads require working outbound storage access. Third-party storage and transfer charges are operator-managed. /tmp/cache is ephemeral; configuration, operational state and rclone config remain under /data. Do not disable native authentication or the owner gateway.

The gateway caps requests at 32 MiB and upstream requests at 600 seconds. Its `/healthz` only proves the proxy process is serving; it does not certify application or database readiness.

Container builds, fresh Railway startup, full application workflows, integrations, native-client compatibility, backup restoration and operating costs remain **unverified**. Source review and static checks are not a runtime certification.

## Acceptance checks

Connect a disposable restic repository, list a snapshot, restore a small known file to /data/restore-check and compare its bytes. If you configure a backup plan, use a staged test file under /data/inbox and prove backup and restore. Restart the service and confirm repository configuration, accounts and operation history remain.

Back up /data/config.json, /data/state and /data/config together with repository credentials and restic encryption passwords. The remote restic repository needs its own retention and protection policy; the Railway volume is not a copy of it. Restore the console into a separate instance and verify it can decrypt and restore a known snapshot before any maintenance or prune operation. Container rollback does not revert database migrations.

## Dependencies for Backrest Repository Manager

### Deployment Dependencies

A Railway account with capacity for 2 services, persistent-volume support, access to the pinned container registries and this repository branch, and the inputs described above. Optional external providers and their credentials are operator-supplied.

### Source and maintenance

- [Upstream project](https://github.com/garethgeorge/backrest)
- [Reviewed source](https://github.com/garethgeorge/backrest/tree/875c9cb51e626a75276a64da42c6a9ec0695010a)
- [Deployment adapter](https://github.com/orenaksakal/railway-templates/tree/codex/unique-template-drafts/templates/round10/backrest)
- Repository services build from `orenaksakal/railway-templates`, branch `codex/unique-template-drafts`, using repository-root context. Keep that branch available.
- Image digests and upstream source references are tracked separately. A source revision is not asserted to match an image without image provenance evidence.

Upstream software retains its own license and trademarks. This community integration does not imply endorsement.
