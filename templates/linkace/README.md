# Deploy and Host LinkAce Bookmark Archive

Bookmarks with SQLite search, persistent storage and protected setup.

**Validation scope: source review and static checks.** This template meets the selection criterion through a public marketplace gap: no matching listing was found on September 19, 2026 using `LinkAce`, `Link Ace`, `Kovah`. Searches are bounded; private, unindexed and differently named listings may exist. The selection does not claim any competitor is broken.

## About Hosting

| Service | Network | Persistent mount |
| --- | --- | --- |
| core | Private | /data |
| linkace | Public HTTPS | None |

The public gateway requires username **admin** and **ACCESS_PASSWORD** from the **linkace** service. API clients can send `X-Template-Key: YOUR_ACCESS_PASSWORD`. Keep core and databases private. The gateway strips Basic Authorization, preserves Bearer authorization and WebSocket upgrades, and limits requests to 32 MiB. Verify native client compatibility before relying on it.

## Why Deploy LinkAce Bookmark Archive on Railway

This template wires a protected HTTPS entry point to private application services, uses generated owner credentials, and declares the persistent mounts shown above. Repository adapters and pinned image references keep the deployment configuration reviewable. Application setup and the acceptance checks below remain operator responsibilities.

## Common Use Cases

Organize reference links into lists; maintain a searchable archive; export a portable bookmark collection.

## First use

Complete LinkAce setup behind the gateway and create an administrator. This template selects the upstream SQLite/database-search mode, with synchronous jobs, rather than the optional Meilisearch topology.

## Recommended acceptance checks

Save links, assign tags and lists, search them, export and reimport a small set, then verify records after a restart.

Test a volume-preserving redeploy as well as a restart. For stateful apps, take an application-consistent backup, including database/WAL and uploaded files, restore it into a separate disposable instance and verify account access and records. For configuration-as-code services, verify a clean rebuild from the saved source. Keep the original data until restoration passes.

## Scope and limitations

Uses one replica and synchronous jobs. Large imports can block requests. SMTP, Internet Archive integration and scheduled maintenance need separate configuration and testing.

This template has source/configuration review and static checks only. No container build, Railway startup, browser/API workflow, volume recovery or cost measurement was performed. Saved editor fidelity is not deployment proof; `/healthz` proves only gateway readiness. Set operator-owned provider credentials only where needed and inspect the selected upstream license before commercial use.

## Dependencies for LinkAce Bookmark Archive

### Deployment Dependencies

A Railway account with capacity for the 2 services listed above, access to the selected image registries and GitHub source branch, and persistent volumes where shown are required. Keep volume-backed services at one replica. Provider accounts, SMTP and other optional integrations are supplied by the operator as described in First use and Scope and limitations.

### Upstream sources

- [Upstream project](https://github.com/Kovah/LinkAce)
- [Selected source reference](https://github.com/Kovah/LinkAce/releases/tag/v2.6.1)
- Upstream source receipt: `049702ba0aae0c57fe1f319a4567cff7115e7992`.
- Images are digest-pinned in `images.round8.lock.json`. Rolling image tags are frozen at the captured digest, not asserted to match the source commit unless independently established.
- Adapters and the gateway use `orenaksakal/railway-templates`, branch `codex/unique-template-drafts`, with repository-root Docker build context. Keep the branch available.
- [Configuration reference](https://github.com/Kovah/LinkAce/blob/v2.6.1/.env.sqlite.production)
- [Configuration reference](https://github.com/Kovah/LinkAce/blob/v2.6.1/config/app.php)
- [Configuration reference](https://github.com/Kovah/LinkAce/blob/v2.6.1/config/scout.php)
- [Configuration reference](https://github.com/Kovah/LinkAce/blob/v2.6.1/docker-compose.production.yml)
- [Configuration reference](https://github.com/Kovah/LinkAce/blob/v2.6.1/docker-compose.yml)
- [Configuration reference](https://github.com/Kovah/LinkAce/blob/v2.6.1/resources/docker/dockerfiles/release-multiplatform.Dockerfile)
