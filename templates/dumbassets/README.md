# Deploy and Host DumbAssets Private Inventory

Asset records, receipts and warranties with generated owner access.

**Validation scope: source review and static checks.** This template meets the selection criterion through a public marketplace gap: no matching listing was found on September 19, 2026 using `DumbAssets`, `Dumb Assets`, `DumbWare`. Searches are bounded; private, unindexed and differently named listings may exist. The selection does not claim any competitor is broken.

## About Hosting

| Service | Network | Persistent mount |
| --- | --- | --- |
| core | Private | /app/data |
| dumbassets | Public HTTPS | None |

The public gateway requires username **admin** and **ACCESS_PASSWORD** from the **dumbassets** service. API clients can send `X-Template-Key: <ACCESS_PASSWORD>`. Keep core and databases private. The gateway strips Basic Authorization, preserves Bearer authorization and WebSocket upgrades, and limits requests to 32 MiB. Verify native client compatibility before relying on it.

## Why Deploy DumbAssets Private Inventory on Railway

This template wires a protected HTTPS entry point to private application services, uses generated owner credentials, and declares the persistent mounts shown above. Repository adapters and pinned image references keep the deployment configuration reviewable. Application setup and the acceptance checks below remain operator responsibilities.

## Common Use Cases

Catalog household or workshop assets; retain purchase receipts; track warranty dates.

## First use

Unlock the gateway and enter DUMBASSETS_PIN from core. Create your inventory and optionally configure your own Apprise destination.

## Recommended acceptance checks

Add an asset, warranty date and a small receipt/photo, export records, restart and verify the record and attachment.

Test a volume-preserving redeploy as well as a restart. For stateful apps, take an application-consistent backup, including database/WAL and uploaded files, restore it into a separate disposable instance and verify account access and records. For configuration-as-code services, verify a clean rebuild from the saved source. Keep the original data until restoration passes.

## Scope and limitations

Single shared household/workshop inventory. Notifications are optional and untested. The chosen tagged release is older; review maintenance suitability.

This template has source/configuration review and static checks only. No container build, Railway startup, browser/API workflow, volume recovery or cost measurement was performed. Saved editor fidelity is not deployment proof; `/healthz` proves only gateway readiness. Set operator-owned provider credentials only where needed and inspect the selected upstream license before commercial use.

## Dependencies for DumbAssets Private Inventory

### Deployment Dependencies

A Railway account with capacity for the 2 services listed above, access to the selected image registries and GitHub source branch, and persistent volumes where shown are required. Keep volume-backed services at one replica. Provider accounts, SMTP and other optional integrations are supplied by the operator as described in First use and Scope and limitations.

### Upstream sources

- [Upstream project](https://github.com/DumbWareio/DumbAssets)
- [Selected source reference](https://github.com/DumbWareio/DumbAssets/releases/tag/v1.0.11)
- Upstream source receipt: `0868fe328fd1118a680fc3f2871f920c46f68976`.
- Images are digest-pinned in `images.round8.lock.json`. Rolling image tags are frozen at the captured digest, not asserted to match the source commit unless independently established.
- Adapters and the gateway use `orenaksakal/railway-templates`, branch `codex/unique-template-drafts`, with repository-root Docker build context. Keep the branch available.
- [Configuration reference](https://github.com/DumbWareio/DumbAssets/blob/v1.0.11/.env.example)
- [Configuration reference](https://github.com/DumbWareio/DumbAssets/blob/v1.0.11/Dockerfile)
- [Configuration reference](https://github.com/DumbWareio/DumbAssets/blob/v1.0.11/docker-compose.yml)
