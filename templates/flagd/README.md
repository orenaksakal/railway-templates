# Deploy and Host Flagd OpenFeature Starter

An OpenFeature-compatible evaluator with a private starter flag.

**Validation scope: source review and static checks.** This template meets the selection criterion through a public marketplace gap: no matching listing was found on September 19, 2026 using `Flagd`, `OpenFeature flagd`. Searches are bounded; private, unindexed and differently named listings may exist. The selection does not claim any competitor is broken.

## About Hosting

| Service | Network | Persistent mount |
| --- | --- | --- |
| core | Private | None |
| flagd | Public HTTPS | None |

The public gateway requires username **admin** and **ACCESS_PASSWORD** from the **flagd** service. API clients can send `X-Template-Key: <ACCESS_PASSWORD>`. Keep core and databases private. The gateway strips Basic Authorization, preserves Bearer authorization and WebSocket upgrades, and limits requests to 32 MiB. Verify native client compatibility before relying on it.

## First use

Call /flagd.evaluation.v1.Service/ResolveBoolean with JSON containing flagKey=welcome-banner and context={}, plus X-Template-Key. Flags are baked into the image from source.

## Recommended acceptance checks

Resolve the starter flag over HTTP and confirm true; verify an unknown flag produces the expected error and requests without the gateway key are rejected.

Test a volume-preserving redeploy as well as a restart. For stateful apps, take an application-consistent backup, including database/WAL and uploaded files, restore it into a separate disposable instance and verify account access and records. For configuration-as-code services, verify a clean rebuild from the saved source. Keep the original data until restoration passes.

## Scope and limitations

Public routing uses HTTP JSON. Native gRPC clients should use the private core endpoint or a separately tested gRPC gateway. No Kubernetes operator or flag-management UI is included.

This template has source/configuration review and static checks only. No container build, Railway startup, browser/API workflow, volume recovery or cost measurement was performed. Saved editor fidelity is not deployment proof; `/healthz` proves only gateway readiness. Set operator-owned provider credentials only where needed and inspect the selected upstream license before commercial use.

## Dependencies and sources

- [Upstream project](https://github.com/open-feature/flagd)
- [Selected source reference](https://github.com/open-feature/flagd/releases/tag/flagd/v0.16.3)
- Upstream source receipt: `c643e5f033f64b2e192ad871133582a62069c568`.
- Images are digest-pinned in `images.round8.lock.json`. Rolling image tags are frozen at the captured digest, not asserted to match the source commit unless independently established.
- Adapters and the gateway use `orenaksakal/railway-templates`, branch `codex/unique-template-drafts`, with repository-root Docker build context. Keep the branch available.
- [Configuration reference](https://github.com/open-feature/flagd/blob/core/v0.17.0/README.md)
- [Configuration reference](https://github.com/open-feature/flagd/blob/core/v0.17.0/config/samples/example_flags.flagd.json)
- [Configuration reference](https://github.com/open-feature/flagd/blob/core/v0.17.0/config/samples/example_flags.json)
- [Configuration reference](https://github.com/open-feature/flagd/blob/core/v0.17.0/docs/assets/cheat-sheet-flags.json)
- [Configuration reference](https://github.com/open-feature/flagd/blob/core/v0.17.0/docs/schema/v0/flags.json)
- [Configuration reference](https://github.com/open-feature/flagd/blob/core/v0.17.0/flagd/build.Dockerfile)
