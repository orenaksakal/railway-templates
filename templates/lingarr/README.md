# Deploy and Host Lingarr Subtitle Translation

A private subtitle translation service with persistent SQLite settings.

**Validation scope: source review and static checks.** This template meets the selection criterion through a public marketplace gap: no matching listing was found on September 19, 2026 using `Lingarr`, `Lingarr subtitles`. Searches are bounded; private, unindexed and differently named listings may exist. The selection does not claim any competitor is broken.

## About Hosting

| Service | Network | Persistent mount |
| --- | --- | --- |
| core | Private | /app/config |
| lingarr | Public HTTPS | None |

The public gateway requires username **admin** and **ACCESS_PASSWORD** from the **lingarr** service. API clients can send `X-Template-Key: <ACCESS_PASSWORD>`. Keep core and databases private. The gateway strips Basic Authorization, preserves Bearer authorization and WebSocket upgrades, and limits requests to 32 MiB. Verify native client compatibility before relying on it.

## First use

Configure an operator-owned translation provider and a small subtitle source reachable by the container. For stored test files, use a subdirectory under /app/config and configure the application paths accordingly.

## Recommended acceptance checks

Translate a short synthetic subtitle file, verify its language and timing, restart and confirm settings and queue state. Verify the exact file-ingestion workflow before release.

Test a volume-preserving redeploy as well as a restart. For stateful apps, take an application-consistent backup, including database/WAL and uploaded files, restore it into a separate disposable instance and verify account access and records. For configuration-as-code services, verify a clean rebuild from the saved source. Keep the original data until restoration passes.

## Scope and limitations

No GPU, translation model, local NAS mount or media library is bundled. Remote Sonarr/Radarr and provider connectivity require operator setup. Provider costs and subtitle/media rights are separate.

This template has source/configuration review and static checks only. No container build, Railway startup, browser/API workflow, volume recovery or cost measurement was performed. Saved editor fidelity is not deployment proof; `/healthz` proves only gateway readiness. Set operator-owned provider credentials only where needed and inspect the selected upstream license before commercial use.

## Dependencies and sources

- [Upstream project](https://github.com/lingarr-translate/lingarr)
- [Selected source reference](https://github.com/lingarr-translate/lingarr/releases/tag/1.3.0)
- Upstream source receipt: `5eadc9335c2ecdc7583d1887d6349f382f2e9092`.
- Images are digest-pinned in `images.round8.lock.json`. Rolling image tags are frozen at the captured digest, not asserted to match the source commit unless independently established.
- Adapters and the gateway use `orenaksakal/railway-templates`, branch `codex/unique-template-drafts`, with repository-root Docker build context. Keep the branch available.
- [Configuration reference](https://github.com/lingarr-translate/lingarr/blob/1.3.0/Lingarr.Server/Dockerfile)
