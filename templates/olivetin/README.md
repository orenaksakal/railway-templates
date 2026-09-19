# Deploy and Host OliveTin Private Action Panel

A protected command panel with two harmless starter actions.

**Unpublished draft.** This candidate meets the selection criterion through a public marketplace gap: no matching listing was found on September 19, 2026 using `OliveTin`, `Olive Tin`. Searches are bounded; private, unindexed and differently named listings may exist. The selection does not claim any competitor is broken.

## About Hosting

| Service | Network | Persistent mount |
| --- | --- | --- |
| core | Private | /config |
| olivetin | Public HTTPS | None |

The public gateway requires username **admin** and **ACCESS_PASSWORD** from the **olivetin** service. API clients can send `X-Template-Key: <ACCESS_PASSWORD>`. Keep core and databases private. The gateway strips Basic Authorization, preserves Bearer authorization and WebSocket upgrades, and limits requests to 32 MiB. Verify native client compatibility before release.

## First use

Open the gateway and try Show UTC time and Show configuration volume usage. Edit /config/config.yaml through an authenticated operator shell to add reviewed actions.

## Recommended acceptance checks

Run both starter actions, verify their output, add a harmless fixed command, restart and confirm the configuration persists.

Test a volume-preserving redeploy as well as a restart. For stateful apps, take an application-consistent backup, including database/WAL and uploaded files, restore it into a separate disposable instance and verify account access and records. For configuration-as-code services, verify a clean rebuild from the saved source. Keep the original data until restoration passes.

## Scope and limitations

Actions run inside this container only. No Docker socket, host filesystem, SSH key or remote infrastructure permission is provided. Treat changes to executable commands as privileged configuration.

This draft has source/configuration review and static checks only. No container build, Railway startup, browser/API workflow, volume recovery or cost measurement was performed. Saved editor fidelity is not deployment proof; `/healthz` proves only gateway readiness. The template has not been published. Set operator-owned provider credentials only where needed and inspect the selected upstream license before commercial use.

## Dependencies and sources

- [Upstream project](https://github.com/OliveTin/OliveTin)
- [Selected source reference](https://github.com/OliveTin/OliveTin/releases/tag/3000.20.0)
- Upstream source receipt: `ed570ff888e2a4021d41cab1b18b44d353086c2c`.
- Images are digest-pinned in `images.round8.lock.json`. Rolling image tags are frozen at the captured digest, not asserted to match the source commit unless independently established.
- Adapters and the gateway use `orenaksakal/railway-templates`, branch `codex/unique-template-drafts`, with repository-root Docker build context. Keep the branch available.
- [Configuration reference](https://github.com/OliveTin/OliveTin/blob/3000.20.0/Dockerfile.singlearch)
- [Configuration reference](https://github.com/OliveTin/OliveTin/blob/3000.20.0/config.yaml)
