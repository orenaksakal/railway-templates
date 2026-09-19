# Deploy and Host DumbKan Private Kanban

A lightweight persistent Kanban board with generated owner access.

**Validation scope: source review and static checks.** This template meets the selection criterion through a public marketplace gap: no matching listing was found on September 19, 2026 using `DumbKan`, `Dumb Kan`, `DumbWare`. Searches are bounded; private, unindexed and differently named listings may exist. The selection does not claim any competitor is broken.

## About Hosting

| Service | Network | Persistent mount |
| --- | --- | --- |
| core | Private | /app/data |
| dumbkan | Public HTTPS | None |

The public gateway requires username **admin** and **ACCESS_PASSWORD** from the **dumbkan** service. API clients can send `X-Template-Key: <ACCESS_PASSWORD>`. Keep core and databases private. The gateway strips Basic Authorization, preserves Bearer authorization and WebSocket upgrades, and limits requests to 32 MiB. Verify native client compatibility before relying on it.

## First use

Unlock the gateway and enter DUMBKAN_PIN from core. Create your first board and cards.

## Recommended acceptance checks

Create a card, move it between columns, edit its details, restart and confirm its position and contents.

Test a volume-preserving redeploy as well as a restart. For stateful apps, take an application-consistent backup, including database/WAL and uploaded files, restore it into a separate disposable instance and verify account access and records. For configuration-as-code services, verify a clean rebuild from the saved source. Keep the original data until restoration passes.

## Scope and limitations

Shared-board access with file-based storage; use one replica. Upstream uses an older Node base. Treat dependency maintenance as a release gate, not as proof of a broken Railway competitor.

This template has source/configuration review and static checks only. No container build, Railway startup, browser/API workflow, volume recovery or cost measurement was performed. Saved editor fidelity is not deployment proof; `/healthz` proves only gateway readiness. Set operator-owned provider credentials only where needed and inspect the selected upstream license before commercial use.

## Dependencies and sources

- [Upstream project](https://github.com/DumbWareio/DumbKan)
- [Selected source reference](https://github.com/DumbWareio/DumbKan/tree/a1dc943e6b259fc0cccd1456233268ca9f40122a)
- Upstream source receipt: `a1dc943e6b259fc0cccd1456233268ca9f40122a`.
- Images are digest-pinned in `images.round8.lock.json`. Rolling image tags are frozen at the captured digest, not asserted to match the source commit unless independently established.
- Adapters and the gateway use `orenaksakal/railway-templates`, branch `codex/unique-template-drafts`, with repository-root Docker build context. Keep the branch available.
- [Configuration reference](https://github.com/DumbWareio/DumbKan/blob/main/.env.example)
- [Configuration reference](https://github.com/DumbWareio/DumbKan/blob/main/Dockerfile)
- [Configuration reference](https://github.com/DumbWareio/DumbKan/blob/main/README.md)
- [Configuration reference](https://github.com/DumbWareio/DumbKan/blob/main/server.js)
