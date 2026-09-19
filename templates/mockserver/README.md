# Deploy and Host MockServer Private Expectations

HTTP mock expectations with bounded logs and persistent configuration.

**Validation scope: source review and static checks.** This template meets the selection criterion through a public marketplace gap: no matching listing was found on September 19, 2026 using `MockServer`, `Mock Server`. Searches are bounded; private, unindexed and differently named listings may exist. The selection does not claim any competitor is broken.

## About Hosting

| Service | Network | Persistent mount |
| --- | --- | --- |
| core | Private | /config |
| mockserver | Public HTTPS | None |

The public gateway requires username **admin** and **ACCESS_PASSWORD** from the **mockserver** service. API clients can send `X-Template-Key: <ACCESS_PASSWORD>`. Keep core and databases private. The gateway strips Basic Authorization, preserves Bearer authorization and WebSocket upgrades, and limits requests to 32 MiB. Verify native client compatibility before relying on it.

## First use

Use X-Template-Key for the owner gateway and the standard MockServer HTTP API. A new volume receives an empty expectation array; existing expectations are preserved.

## Recommended acceptance checks

PUT an expectation to /mockserver/expectation, invoke its path, restart and verify the expectation reloads. Test unauthorized rejection separately.

Test a volume-preserving redeploy as well as a restart. For stateful apps, take an application-consistent backup, including database/WAL and uploaded files, restore it into a separate disposable instance and verify account access and records. For configuration-as-code services, verify a clean rebuild from the saved source. Keep the original data until restoration passes.

## Scope and limitations

No proxy recording or external forwarding is preconfigured. Only expectations persist, not request logs. Public access uses HTTP through the gateway; other protocol modes are outside this template.

This template has source/configuration review and static checks only. No container build, Railway startup, browser/API workflow, volume recovery or cost measurement was performed. Saved editor fidelity is not deployment proof; `/healthz` proves only gateway readiness. Set operator-owned provider credentials only where needed and inspect the selected upstream license before commercial use.

## Dependencies and sources

- [Upstream project](https://github.com/mock-server/mockserver-monorepo)
- [Selected source reference](https://github.com/mock-server/mockserver-monorepo/releases/tag/mockserver-8.0.0)
- Upstream source receipt: `a9db199328775afece93f68cf6988234a9e31b43`.
- Images are digest-pinned in `images.round8.lock.json`. Rolling image tags are frozen at the captured digest, not asserted to match the source commit unless independently established.
- Adapters and the gateway use `orenaksakal/railway-templates`, branch `codex/unique-template-drafts`, with repository-root Docker build context. Keep the branch available.
- [Configuration reference](https://github.com/mock-server/mockserver-monorepo/blob/mockserver-8.0.0/container_integration_tests/docker_compose_with_persisted_expectations/docker-compose.override.yml)
- [Configuration reference](https://github.com/mock-server/mockserver-monorepo/blob/mockserver-8.0.0/docker/Dockerfile)
- [Configuration reference](https://github.com/mock-server/mockserver-monorepo/blob/mockserver-8.0.0/docker/docker-compose/configure_by_volume_mount/initializerJson.json)
- [Configuration reference](https://github.com/mock-server/mockserver-monorepo/blob/mockserver-8.0.0/helm/mockserver-config/static/initializerJson.json)
- [Configuration reference](https://github.com/mock-server/mockserver-monorepo/blob/mockserver-8.0.0/mockserver/mockserver-core/src/test/resources/org/mockserver/server/initialize/initializerJson.json)
- [Configuration reference](https://github.com/mock-server/mockserver-monorepo/blob/mockserver-8.0.0/mockserver/mockserver-maven-plugin/src/integration-tests/mockserver-initializer-json-main-classpath/src/main/resources/org/mockserver/initializerJson.json)
