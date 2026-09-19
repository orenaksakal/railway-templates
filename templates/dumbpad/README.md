# Deploy and Host DumbPad Private Notepad

Autosaving Markdown notes with generated PIN and persistent files.

**Unpublished draft.** This candidate meets the selection criterion through a public marketplace gap: no matching listing was found on September 19, 2026 using `DumbPad`, `Dumb Pad`, `DumbWare`. Searches are bounded; private, unindexed and differently named listings may exist. The selection does not claim any competitor is broken.

## About Hosting

| Service | Network | Persistent mount |
| --- | --- | --- |
| core | Private | /app/data |
| dumbpad | Public HTTPS | None |

The public gateway requires username **admin** and **ACCESS_PASSWORD** from the **dumbpad** service. API clients can send `X-Template-Key: <ACCESS_PASSWORD>`. Keep core and databases private. The gateway strips Basic Authorization, preserves Bearer authorization and WebSocket upgrades, and limits requests to 32 MiB. Verify native client compatibility before release.

## First use

Unlock the gateway and then enter DUMBPAD_PIN from core. Use the note editor; keep both access controls enabled.

## Recommended acceptance checks

Create two notes, format Markdown, search their text, reload and restart, then confirm both files remain.

Test a volume-preserving redeploy as well as a restart. For stateful apps, take an application-consistent backup, including database/WAL and uploaded files, restore it into a separate disposable instance and verify account access and records. For configuration-as-code services, verify a clean rebuild from the saved source. Keep the original data until restoration passes.

## Scope and limitations

Single shared notebook access, not separate per-user accounts. The chosen tagged release is older; review upstream maintenance before production use.

This draft has source/configuration review and static checks only. No container build, Railway startup, browser/API workflow, volume recovery or cost measurement was performed. Saved editor fidelity is not deployment proof; `/healthz` proves only gateway readiness. The template has not been published. Set operator-owned provider credentials only where needed and inspect the selected upstream license before commercial use.

## Dependencies and sources

- [Upstream project](https://github.com/DumbWareio/DumbPad)
- [Selected source reference](https://github.com/DumbWareio/DumbPad/releases/tag/v1.0.4)
- Upstream source receipt: `8ae0c48cb12c2c222f8c22fbbf06bb674f4b181c`.
- Images are digest-pinned in `images.round8.lock.json`. Rolling image tags are frozen at the captured digest, not asserted to match the source commit unless independently established.
- Adapters and the gateway use `orenaksakal/railway-templates`, branch `codex/unique-template-drafts`, with repository-root Docker build context. Keep the branch available.
- [Configuration reference](https://github.com/DumbWareio/DumbPad/blob/v1.0.4/.env.example)
- [Configuration reference](https://github.com/DumbWareio/DumbPad/blob/v1.0.4/Dockerfile)
- [Configuration reference](https://github.com/DumbWareio/DumbPad/blob/v1.0.4/docker-compose.yml)
