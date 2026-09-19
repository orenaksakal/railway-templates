# Deploy and Host Grimoire Bookmark Workspace

Local-first bookmarks and search in a private persistent workspace.

**Validation scope: source review and static checks.** This template meets the selection criterion through a public marketplace gap: no matching listing was found on September 19, 2026 using `Grimoire`, `grimoire bookmarks`, `littleimp`, `little imp`, `goniszewski`. Searches are bounded; private, unindexed and differently named listings may exist. The selection does not claim any competitor is broken.

## About Hosting

| Service | Network | Persistent mount |
| --- | --- | --- |
| core | Private | /data |
| grimoire | Public HTTPS | None |

The public gateway requires username **admin** and **ACCESS_PASSWORD** from the **grimoire** service. API clients can send `X-Template-Key: <ACCESS_PASSWORD>`. Keep core and databases private. The gateway strips Basic Authorization, preserves Bearer authorization and WebSocket upgrades, and limits requests to 32 MiB. Verify native client compatibility before relying on it.

## First use

Open the workspace behind the gateway. Optional AI enrichment requires your own model credentials in the application settings. The current v1.2 rewrite is built from a checksum-verified source archive.

## Recommended acceptance checks

Save a URL, import a small bookmark file, extract readable content, search it and verify data after restart. Test semantic search separately if a provider is configured.

Test a volume-preserving redeploy as well as a restart. For stateful apps, take an application-consistent backup, including database/WAL and uploaded files, restore it into a separate disposable instance and verify account access and records. For configuration-as-code services, verify a clean rebuild from the saved source. Keep the original data until restoration passes.

## Scope and limitations

Not an upgrade path for legacy v0.5 installations. AI providers cost extra. Build dependencies and the application workflow have not been executed in Railway.

This template has source/configuration review and static checks only. No container build, Railway startup, browser/API workflow, volume recovery or cost measurement was performed. Saved editor fidelity is not deployment proof; `/healthz` proves only gateway readiness. Set operator-owned provider credentials only where needed and inspect the selected upstream license before commercial use.

## Dependencies and sources

- [Upstream project](https://github.com/goniszewski/grimoire)
- [Selected source reference](https://github.com/goniszewski/grimoire/releases/tag/v1.2.0)
- Upstream source receipt: `ca974f3561399302b56e2b2b7f52036766dc4117`.
- Images are digest-pinned in `images.round8.lock.json`. Rolling image tags are frozen at the captured digest, not asserted to match the source commit unless independently established.
- Adapters and the gateway use `orenaksakal/railway-templates`, branch `codex/unique-template-drafts`, with repository-root Docker build context. Keep the branch available.
- [Configuration reference](https://github.com/goniszewski/grimoire/blob/v1.2.0/Dockerfile)
- [Configuration reference](https://github.com/goniszewski/grimoire/blob/v1.2.0/daemon/.env.example)
- [Configuration reference](https://github.com/goniszewski/grimoire/blob/v1.2.0/docker-compose.yml)
