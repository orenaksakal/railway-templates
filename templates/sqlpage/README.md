# Deploy and Host SQLPage Private App Starter

A private SQL-driven web app with persistent pages and SQLite.

**Validation scope: source review and static checks.** This template meets the selection criterion through a public marketplace gap: no matching listing was found on September 19, 2026 using `SQLPage`, `SQL Page`. Searches are bounded; private, unindexed and differently named listings may exist. The selection does not claim any competitor is broken.

## About Hosting

| Service | Network | Persistent mount |
| --- | --- | --- |
| core | Private | /data |
| sqlpage | Public HTTPS | None |

The public gateway requires username **admin** and **ACCESS_PASSWORD** from the **sqlpage** service. API clients can send `X-Template-Key: <ACCESS_PASSWORD>`. Keep core and databases private. The gateway strips Basic Authorization, preserves Bearer authorization and WebSocket upgrades, and limits requests to 32 MiB. Verify native client compatibility before relying on it.

## Why Deploy SQLPage Private App Starter on Railway

This template wires a protected HTTPS entry point to private application services, uses generated owner credentials, and declares the persistent mounts shown above. Repository adapters and pinned image references keep the deployment configuration reviewable. Application setup and the acceptance checks below remain operator responsibilities.

## Common Use Cases

Prototype a SQL-driven internal tool; render SQLite records; build private read-only reports.

## First use

Open the starter page through the gateway. Edit /data/www/index.sql or add SQL pages through an authenticated Railway shell. The SQLite database is /data/app.db.

## Recommended acceptance checks

Load the SQLite-version page, add a small table and a read-only SQL page for it, restart and confirm both the page and rows remain.

Test a volume-preserving redeploy as well as a restart. For stateful apps, take an application-consistent backup, including database/WAL and uploaded files, restore it into a separate disposable instance and verify account access and records. For configuration-as-code services, verify a clean rebuild from the saved source. Keep the original data until restoration passes.

## Scope and limitations

The starter does not implement per-user application permissions. All gateway users share the app. Review SQL, query access and form validation before turning it into a business application.

This template has source/configuration review and static checks only. No container build, Railway startup, browser/API workflow, volume recovery or cost measurement was performed. Saved editor fidelity is not deployment proof; `/healthz` proves only gateway readiness. Set operator-owned provider credentials only where needed and inspect the selected upstream license before commercial use.

## Dependencies for SQLPage Private App Starter

### Deployment Dependencies

A Railway account with capacity for the 2 services listed above, access to the selected image registries and GitHub source branch, and persistent volumes where shown are required. Keep volume-backed services at one replica. Provider accounts, SMTP and other optional integrations are supplied by the operator as described in First use and Scope and limitations.

### Upstream sources

- [Upstream project](https://github.com/sqlpage/SQLPage)
- [Selected source reference](https://github.com/sqlpage/SQLPage/releases/tag/v0.46.3)
- Upstream source receipt: `d30487b019bbd9a3bb971abd46a9616891b63d27`.
- Images are digest-pinned in `images.round8.lock.json`. Rolling image tags are frozen at the captured digest, not asserted to match the source commit unless independently established.
- Adapters and the gateway use `orenaksakal/railway-templates`, branch `codex/unique-template-drafts`, with repository-root Docker build context. Keep the branch available.
- [Configuration reference](https://github.com/sqlpage/SQLPage/blob/v0.46.3/Dockerfile)
- [Configuration reference](https://github.com/sqlpage/SQLPage/blob/v0.46.3/docker-compose.yml)
