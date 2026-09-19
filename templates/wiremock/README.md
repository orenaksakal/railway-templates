# Deploy and Host WireMock Private API Stubs

Persistent HTTP API stubs behind generated owner access.

**Validation scope: source review and static checks.** This template meets the selection criterion through a public marketplace gap: no matching listing was found on September 19, 2026 using `WireMock`, `Wire Mock`. Searches are bounded; private, unindexed and differently named listings may exist. The selection does not claim any competitor is broken.

## About Hosting

| Service | Network | Persistent mount |
| --- | --- | --- |
| core | Private | /home/wiremock |
| wiremock | Public HTTPS | None |

The public gateway requires username **admin** and **ACCESS_PASSWORD** from the **wiremock** service. API clients can send `X-Template-Key: <ACCESS_PASSWORD>`. Keep core and databases private. The gateway strips Basic Authorization, preserves Bearer authorization and WebSocket upgrades, and limits requests to 32 MiB. Verify native client compatibility before relying on it.

## First use

Use the gateway header X-Template-Key with its generated ACCESS_PASSWORD when calling the admin API and stub endpoints. Create mappings with persistent=true, or save mappings through /__admin/mappings/save.

## Recommended acceptance checks

POST a mapping to /__admin/mappings for GET /hello returning hello, call it, save mappings, restart and verify the same response. Confirm requests without the owner credential are blocked.

Test a volume-preserving redeploy as well as a restart. For stateful apps, take an application-consistent backup, including database/WAL and uploaded files, restore it into a separate disposable instance and verify account access and records. For configuration-as-code services, verify a clean rebuild from the saved source. Keep the original data until restoration passes.

## Scope and limitations

No public open proxy or production traffic capture is configured. Request journals are bounded and not persisted. Basic Authorization is stripped by the gateway; tests that inspect that header need an adapted gateway or private access.

This template has source/configuration review and static checks only. No container build, Railway startup, browser/API workflow, volume recovery or cost measurement was performed. Saved editor fidelity is not deployment proof; `/healthz` proves only gateway readiness. Set operator-owned provider credentials only where needed and inspect the selected upstream license before commercial use.

## Dependencies and sources

- [Upstream project](https://github.com/wiremock/wiremock-docker)
- [Selected source reference](https://github.com/wiremock/wiremock-docker/releases/tag/3.13.2-3)
- Upstream source receipt: `9210e86a4db4a57474728d45a352678ea0dbfe62`.
- Images are digest-pinned in `images.round8.lock.json`. Rolling image tags are frozen at the captured digest, not asserted to match the source commit unless independently established.
- Adapters and the gateway use `orenaksakal/railway-templates`, branch `codex/unique-template-drafts`, with repository-root Docker build context. Keep the branch available.
- [Configuration reference](https://github.com/wiremock/wiremock-docker/blob/3.13.2-3/Dockerfile)
