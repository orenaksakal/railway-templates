# Deploy and Host Yaade API Workspace

A private collaborative API client with persistent request collections.

**Validation scope: source review and static checks.** This template meets the selection criterion through a public marketplace gap: no matching listing was found on September 19, 2026 using `Yaade`, `Yaade API`, `EsperoTech`. Searches are bounded; private, unindexed and differently named listings may exist. The selection does not claim any competitor is broken.

## About Hosting

| Service | Network | Persistent mount |
| --- | --- | --- |
| core | Private | /app/data |
| yaade | Public HTTPS | None |

The public gateway requires username **admin** and **ACCESS_PASSWORD** from the **yaade** service. API clients can send `X-Template-Key: YOUR_ACCESS_PASSWORD`. Keep core and databases private. The gateway strips Basic Authorization, preserves Bearer authorization and WebSocket upgrades, and limits requests to 32 MiB. Verify native client compatibility before relying on it.

## Why Deploy Yaade API Workspace on Railway

This template wires a protected HTTPS entry point to private application services, uses generated owner credentials, and declares the persistent mounts shown above. Repository adapters and pinned image references keep the deployment configuration reviewable. Application setup and the acceptance checks below remain operator responsibilities.

## Common Use Cases

Save reusable API requests; organize request collections; maintain environments for development APIs.

## First use

After the gateway, log in as admin with the upstream initial password password and immediately change it in Account settings. The default account is never exposed directly.

## Recommended acceptance checks

Create a collection and environment, call a harmless endpoint you control, save and export the collection, restart and verify it remains.

Test a volume-preserving redeploy as well as a restart. For stateful apps, take an application-consistent backup, including database/WAL and uploaded files, restore it into a separate disposable instance and verify account access and records. For configuration-as-code services, verify a clean rebuild from the saved source. Keep the original data until restoration passes.

## Scope and limitations

The upstream latest image is digest-pinned; its source has an older update cadence. Browser extension support, OAuth and client access must be verified independently.

This template has source/configuration review and static checks only. No container build, Railway startup, browser/API workflow, volume recovery or cost measurement was performed. Saved editor fidelity is not deployment proof; `/healthz` proves only gateway readiness. Set operator-owned provider credentials only where needed and inspect the selected upstream license before commercial use.

## Dependencies for Yaade API Workspace

### Deployment Dependencies

A Railway account with capacity for the 2 services listed above, access to the selected image registries and GitHub source branch, and persistent volumes where shown are required. Keep volume-backed services at one replica. Provider accounts, SMTP and other optional integrations are supplied by the operator as described in First use and Scope and limitations.

### Upstream sources

- [Upstream project](https://github.com/EsperoTech/yaade)
- [Selected source reference](https://github.com/EsperoTech/yaade/tree/0b4dea7e9b140e029e29210c7694217b464eab41)
- Upstream source receipt: `0b4dea7e9b140e029e29210c7694217b464eab41`.
- Images are digest-pinned in `images.round8.lock.json`. Rolling image tags are frozen at the captured digest, not asserted to match the source commit unless independently established.
- Adapters and the gateway use `orenaksakal/railway-templates`, branch `codex/unique-template-drafts`, with repository-root Docker build context. Keep the branch available.
- [Configuration reference](https://github.com/EsperoTech/yaade/blob/main/server/Dockerfile)
