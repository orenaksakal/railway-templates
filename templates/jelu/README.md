# Deploy and Host Jelu Reading Tracker

Reading lists, book metadata and reviews with persistent SQLite.

**Unpublished draft.** This candidate meets the selection criterion through a public marketplace gap: no matching listing was found on September 19, 2026 using `Jelu`, `Jelu books`, `bayang`. Searches are bounded; private, unindexed and differently named listings may exist. The selection does not claim any competitor is broken.

## About Hosting

| Service | Network | Persistent mount |
| --- | --- | --- |
| core | Private | /data |
| jelu | Public HTTPS | None |

The public gateway requires username **admin** and **ACCESS_PASSWORD** from the **jelu** service. API clients can send `X-Template-Key: <ACCESS_PASSWORD>`. Keep core and databases private. The gateway strips Basic Authorization, preserves Bearer authorization and WebSocket upgrades, and limits requests to 32 MiB. Verify native client compatibility before release.

## First use

Create the initial owner account behind the gateway. Database, covers and imports are redirected into the single /data volume.

## Recommended acceptance checks

Add a book by ISBN and one manually; record a reading event and review, attach a cover, restart and confirm the history and image remain.

Test a volume-preserving redeploy as well as a restart. For stateful apps, take an application-consistent backup, including database/WAL and uploaded files, restore it into a separate disposable instance and verify account access and records. For configuration-as-code services, verify a clean rebuild from the saved source. Keep the original data until restoration passes.

## Scope and limitations

Metadata lookup depends on upstream book providers. This is a reading tracker, not ebook distribution or library DRM.

This draft has source/configuration review and static checks only. No container build, Railway startup, browser/API workflow, volume recovery or cost measurement was performed. Saved editor fidelity is not deployment proof; `/healthz` proves only gateway readiness. The template has not been published. Set operator-owned provider credentials only where needed and inspect the selected upstream license before commercial use.

## Dependencies and sources

- [Upstream project](https://github.com/bayang/jelu)
- [Selected source reference](https://github.com/bayang/jelu/releases/tag/v0.87.3)
- Upstream source receipt: `1e570bf65512cde2595bd145ccd54e934e181207`.
- Images are digest-pinned in `images.round8.lock.json`. Rolling image tags are frozen at the captured digest, not asserted to match the source commit unless independently established.
- Adapters and the gateway use `orenaksakal/railway-templates`, branch `codex/unique-template-drafts`, with repository-root Docker build context. Keep the branch available.
- [Configuration reference](https://github.com/bayang/jelu/blob/v0.87.3/Dockerfile)
- [Configuration reference](https://github.com/bayang/jelu/blob/v0.87.3/src/main/resources/application.yml)
