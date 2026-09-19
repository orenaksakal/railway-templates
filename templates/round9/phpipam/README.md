# Deploy and Host phpIPAM Address Inventory

IP address and subnet inventory with MariaDB and protected administration.

## About Hosting

| Service | Access | Persistent storage |
| --- | --- | --- |
| app | Private | /phpipam/css/images/logo |
| phpipam | Public HTTPS | None |
| mariadb | Private | /var/lib/mysql |

Railway provides the public HTTPS endpoint. Dependencies stay on private networking. Keep each volume-backed service at one replica.

## Why Deploy phpIPAM Address Inventory on Railway

This definition includes pinned container sources, documented storage paths and generated credentials where required. It restores the missing repository adapters from the previous draft and keeps the application setup steps explicit.

## Common Use Cases

IP address and subnet inventory with MariaDB and protected administration.

## First use

No mandatory operator-supplied variables. Retrieve generated credentials from the service variables.

Use gateway username admin and ACCESS_PASSWORD. In the installation wizard use the supplied database user to import the schema into the existing phpipam database. Set the admin password, then set IPAM_DISABLE_INSTALLER=1. Store sections, subnets and address assignments in the UI.

Where an owner gateway is included, the username is admin. API clients can use `X-Template-Key: YOUR_ACCESS_PASSWORD`. The gateway consumes Basic Authorization, preserves Bearer authorization and WebSocket upgrades, and caps requests at 32 MiB; check compatibility with native clients. Generated credentials must remain private.

## Scope and limitations

Scope is IP address inventory. No network-scanning cron service, host network access, NET_ADMIN or NET_RAW capabilities are supplied. Railway cannot discover your home or company LAN without connectivity you separately arrange. API clients must account for the outer Basic gateway.

This is a prepared, unpublished draft. Source and static configuration checks are recorded in the repository's preparation report. Container builds, fresh Railway startup, native-client compatibility, full application workflows, backup restoration and costs have not been verified. A proxy healthcheck is not application readiness.

## Acceptance checks

Initialize the schema, sign in, create a section/subnet/address, export the inventory, restart MariaDB and the app, and verify the records.

Verify first use, unauthorized rejection where applicable, and a volume-preserving redeploy. Back up every persistent volume, generated application key and consistent database export. Restore into a separate instance and verify accounts, records and uploaded bytes before using important data. Container rollback does not revert database migrations.

## Dependencies for phpIPAM Address Inventory

### Deployment Dependencies

A Railway account with capacity for 3 services, access to the selected registries and repository source, and the inputs listed above. External provider accounts and optional integrations are operator-supplied.

### Source and maintenance

- [Upstream project](https://github.com/phpipam/phpipam)
- [Reviewed application source](https://github.com/phpipam/phpipam/tree/e8010751d491e485acefa5787fb0e518eb948771)
- [Deployment adapter](https://github.com/orenaksakal/railway-templates/tree/codex/unique-template-drafts/templates/round9/phpipam)
- Repository services build from `orenaksakal/railway-templates`, branch `codex/unique-template-drafts`, with repository-root build context. Keep the branch available.
- Image digests and source references are tracked separately. A source revision is not asserted to match a rolling image unless the image metadata establishes it.

Upstream software retains its own license and trademarks. This community integration does not imply endorsement.
