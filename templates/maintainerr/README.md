# Deploy and Host Maintainerr Media Rules

Media-library review rules with persistent configuration and owner access.

**Validation scope: source review and static checks.** This template meets the selection criterion through a public marketplace gap: no matching listing was found on September 19, 2026 using `Maintainerr`, `Maintainerr Plex`. Searches are bounded; private, unindexed and differently named listings may exist. The selection does not claim any competitor is broken.

## About Hosting

| Service | Network | Persistent mount |
| --- | --- | --- |
| core | Private | /opt/data |
| maintainerr | Public HTTPS | None |

The public gateway requires username **admin** and **ACCESS_PASSWORD** from the **maintainerr** service. API clients can send `X-Template-Key: <ACCESS_PASSWORD>`. Keep core and databases private. The gateway strips Basic Authorization, preserves Bearer authorization and WebSocket upgrades, and limits requests to 32 MiB. Verify native client compatibility before relying on it.

## First use

Connect your own reachable media server after opening the owner gateway. Begin with a non-destructive review/collection rule and review results before enabling any deletion action.

## Recommended acceptance checks

Connect a disposable library, evaluate a review-only rule, inspect selected items and verify rule persistence after restart. Do not use live deletion as an onboarding test.

Test a volume-preserving redeploy as well as a restart. For stateful apps, take an application-consistent backup, including database/WAL and uploaded files, restore it into a separate disposable instance and verify account access and records. For configuration-as-code services, verify a clean rebuild from the saved source. Keep the original data until restoration passes.

## Scope and limitations

No media server or library is bundled. Remote APIs must be reachable from Railway. File deletion or collection changes can affect connected services once explicitly enabled by the operator.

This template has source/configuration review and static checks only. No container build, Railway startup, browser/API workflow, volume recovery or cost measurement was performed. Saved editor fidelity is not deployment proof; `/healthz` proves only gateway readiness. Set operator-owned provider credentials only where needed and inspect the selected upstream license before commercial use.

## Dependencies and sources

- [Upstream project](https://github.com/Maintainerr/Maintainerr)
- [Selected source reference](https://github.com/Maintainerr/Maintainerr/releases/tag/v3.29.0)
- Upstream source receipt: `34776039e26113291a46fcbde9de73fb99728788`.
- Images are digest-pinned in `images.round8.lock.json`. Rolling image tags are frozen at the captured digest, not asserted to match the source commit unless independently established.
- Adapters and the gateway use `orenaksakal/railway-templates`, branch `codex/unique-template-drafts`, with repository-root Docker build context. Keep the branch available.
- [Configuration reference](https://github.com/Maintainerr/Maintainerr/blob/v3.29.0/Dockerfile)
