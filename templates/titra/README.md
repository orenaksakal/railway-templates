# Deploy and Host Titra Project Time Tracking

Project time tracking with private authenticated MongoDB.

**Validation scope: source review and static checks.** This template meets the selection criterion through a public marketplace gap: no matching listing was found on September 19, 2026 using `Titra`, `Titra time`, `titraio`, `kromit`. Searches are bounded; private, unindexed and differently named listings may exist. The selection does not claim any competitor is broken.

## About Hosting

| Service | Network | Persistent mount |
| --- | --- | --- |
| mongodb | Private | /data/db |
| core | Private | None |
| titra | Public HTTPS | None |

The public gateway requires username **admin** and **ACCESS_PASSWORD** from the **titra** service. API clients can send `X-Template-Key: <ACCESS_PASSWORD>`. Keep core and databases private. The gateway strips Basic Authorization, preserves Bearer authorization and WebSocket upgrades, and limits requests to 32 MiB. Verify native client compatibility before relying on it.

## Why Deploy Titra Project Time Tracking on Railway

This template wires a protected HTTPS entry point to private application services, uses generated owner credentials, and declares the persistent mounts shown above. Repository adapters and pinned image references keep the deployment configuration reviewable. Application setup and the acceptance checks below remain operator responsibilities.

## Common Use Cases

Log project hours; review time reports; export records for client billing.

## First use

Register the owner behind the gateway and review registration permissions in Titra before inviting anyone. ROOT_URL and the private MongoDB URL are prewired.

## Recommended acceptance checks

Create a project, record two time entries, run a report and export, restart and confirm the entries remain.

Test a volume-preserving redeploy as well as a restart. For stateful apps, take an application-consistent backup, including database/WAL and uploaded files, restore it into a separate disposable instance and verify account access and records. For configuration-as-code services, verify a clean rebuild from the saved source. Keep the original data until restoration passes.

## Scope and limitations

This is a single MongoDB node, not a replica set or high-availability service. The generated MongoDB administrator is limited to this private project database service.

This template has source/configuration review and static checks only. No container build, Railway startup, browser/API workflow, volume recovery or cost measurement was performed. Saved editor fidelity is not deployment proof; `/healthz` proves only gateway readiness. Set operator-owned provider credentials only where needed and inspect the selected upstream license before commercial use.

## Dependencies for Titra Project Time Tracking

### Deployment Dependencies

A Railway account with capacity for the 3 services listed above, access to the selected image registries and GitHub source branch, and persistent volumes where shown are required. Keep volume-backed services at one replica. Provider accounts, SMTP and other optional integrations are supplied by the operator as described in First use and Scope and limitations.

### Upstream sources

- [Upstream project](https://github.com/titraio/titra)
- [Selected source reference](https://github.com/titraio/titra/releases/tag/v1.1.0)
- Upstream source receipt: `82117471c86bea0a672dd75b4fd45fcd9fa44fc6`.
- Images are digest-pinned in `images.round8.lock.json`. Rolling image tags are frozen at the captured digest, not asserted to match the source commit unless independently established.
- Adapters and the gateway use `orenaksakal/railway-templates`, branch `codex/unique-template-drafts`, with repository-root Docker build context. Keep the branch available.
- [Configuration reference](https://github.com/kromitgmbh/titra/blob/v1.1.0/Dockerfile)
- [Configuration reference](https://github.com/kromitgmbh/titra/blob/v1.1.0/docker-compose.yml)
