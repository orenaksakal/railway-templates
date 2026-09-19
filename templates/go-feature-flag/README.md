# Deploy and Host GO Feature Flag Relay

A private feature-flag relay with a deterministic starter flag.

**Validation scope: source review and static checks.** This template meets the selection criterion through a public marketplace gap: no matching listing was found on September 19, 2026 using `GO Feature Flag`, `gofeatureflag`, `go-feature-flag`, `thomaspoignant`. Searches are bounded; private, unindexed and differently named listings may exist. The selection does not claim any competitor is broken.

## About Hosting

| Service | Network | Persistent mount |
| --- | --- | --- |
| core | Private | None |
| go-feature-flag | Public HTTPS | None |

The public gateway requires username **admin** and **ACCESS_PASSWORD** from the **go-feature-flag** service. API clients can send `X-Template-Key: YOUR_ACCESS_PASSWORD`. Keep core and databases private. The gateway strips Basic Authorization, preserves Bearer authorization and WebSocket upgrades, and limits requests to 32 MiB. Verify native client compatibility before relying on it.

## Why Deploy GO Feature Flag Relay on Railway

This template wires a protected HTTPS entry point to private application services, uses generated owner credentials, and declares the persistent mounts shown above. Repository adapters and pinned image references keep the deployment configuration reviewable. Application setup and the acceptance checks below remain operator responsibilities.

## Common Use Cases

Evaluate application feature flags over HTTP; manage flags in source control; prototype controlled feature rollout.

## First use

Call the relay HTTP API with X-Template-Key carrying the gateway password. The welcome-banner flag defaults to true. Change the baked YAML in a fork and redeploy to manage flags as code.

## Recommended acceptance checks

Evaluate welcome-banner via /v1/feature/welcome-banner/eval for a synthetic user, confirm true, change its default in source and confirm the redeployed value.

Test a volume-preserving redeploy as well as a restart. For stateful apps, take an application-consistent backup, including database/WAL and uploaded files, restore it into a separate disposable instance and verify account access and records. For configuration-as-code services, verify a clean rebuild from the saved source. Keep the original data until restoration passes.

## Scope and limitations

No visual editor or mutable flag database is bundled. Native SDKs must support the owner header or use private networking. Exporters and third-party retrievers are not configured.

This template has source/configuration review and static checks only. No container build, Railway startup, browser/API workflow, volume recovery or cost measurement was performed. Saved editor fidelity is not deployment proof; `/healthz` proves only gateway readiness. Set operator-owned provider credentials only where needed and inspect the selected upstream license before commercial use.

## Dependencies for GO Feature Flag Relay

### Deployment Dependencies

A Railway account with capacity for the 2 services listed above, access to the selected image registries and GitHub source branch, and persistent volumes where shown are required. Keep volume-backed services at one replica. Provider accounts, SMTP and other optional integrations are supplied by the operator as described in First use and Scope and limitations.

### Upstream sources

- [Upstream project](https://github.com/thomaspoignant/go-feature-flag)
- [Selected source reference](https://github.com/thomaspoignant/go-feature-flag/releases/tag/v1.55.3)
- Upstream source receipt: `98a70eada02674760bf94526f8567755089632c4`.
- Images are digest-pinned in `images.round8.lock.json`. Rolling image tags are frozen at the captured digest, not asserted to match the source commit unless independently established.
- Adapters and the gateway use `orenaksakal/railway-templates`, branch `codex/unique-template-drafts`, with repository-root Docker build context. Keep the branch available.
- [Configuration reference](https://github.com/thomaspoignant/go-feature-flag/blob/v1.55.3/cmd/relayproxy/DockerfileGoreleaser)
- [Configuration reference](https://github.com/thomaspoignant/go-feature-flag/blob/v1.55.3/cmd/relayproxy/testdata/dockerhub-example/flags.goff.yaml)
- [Configuration reference](https://github.com/thomaspoignant/go-feature-flag/blob/v1.55.3/cmd/relayproxy/testdata/dockerhub-example/goff-proxy.yaml)
- [Configuration reference](https://github.com/thomaspoignant/go-feature-flag/blob/v1.55.3/cmd/relayproxy/testdata/goff/all_flags/valid_request_specify_flags.json)
- [Configuration reference](https://github.com/thomaspoignant/go-feature-flag/blob/v1.55.3/cmd/relayproxy/testdata/goff/all_flags/valid_response_specify_flags.json)
- [Configuration reference](https://github.com/thomaspoignant/go-feature-flag/blob/v1.55.3/cmd/relayproxy/testdata/goff/configuration/requests/filter-flags.json)
