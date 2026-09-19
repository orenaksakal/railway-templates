# Deploy and Host Fava Beancount Ledger

A private Beancount web ledger with a persistent starter journal.

**Validation scope: source review and static checks.** This template meets the selection criterion through a public marketplace gap: no matching listing was found on September 19, 2026 using `Fava`, `Fava Beancount`, `Beancount`. Searches are bounded; private, unindexed and differently named listings may exist. The selection does not claim any competitor is broken.

## About Hosting

| Service | Network | Persistent mount |
| --- | --- | --- |
| core | Private | /data |
| fava | Public HTTPS | None |

The public gateway requires username **admin** and **ACCESS_PASSWORD** from the **fava** service. API clients can send `X-Template-Key: <ACCESS_PASSWORD>`. Keep core and databases private. The gateway strips Basic Authorization, preserves Bearer authorization and WebSocket upgrades, and limits requests to 32 MiB. Verify native client compatibility before relying on it.

## Why Deploy Fava Beancount Ledger on Railway

This template wires a protected HTTPS entry point to private application services, uses generated owner credentials, and declares the persistent mounts shown above. Repository adapters and pinned image references keep the deployment configuration reviewable. Application setup and the acceptance checks below remain operator responsibilities.

## Common Use Cases

Explore a Beancount journal; review account balances; maintain a versionable personal ledger.

## First use

Open the seeded ledger behind the gateway. Replace the clearly marked example transaction with your own journal through the editor or an authenticated file-management workflow.

## Recommended acceptance checks

Edit and balance a small synthetic transaction, view account balances, download the journal and confirm changes after restart. A pre-existing main.beancount file is never overwritten by startup.

Test a volume-preserving redeploy as well as a restart. For stateful apps, take an application-consistent backup, including database/WAL and uploaded files, restore it into a separate disposable instance and verify account access and records. For configuration-as-code services, verify a clean rebuild from the saved source. Keep the original data until restoration passes.

## Scope and limitations

Fava 1.30.16 is package-pinned; transitive Python dependencies are resolved at build time. This is ledger software, not bank synchronization or accounting certification. Preserve included journal files together.

This template has source/configuration review and static checks only. No container build, Railway startup, browser/API workflow, volume recovery or cost measurement was performed. Saved editor fidelity is not deployment proof; `/healthz` proves only gateway readiness. Set operator-owned provider credentials only where needed and inspect the selected upstream license before commercial use.

## Dependencies for Fava Beancount Ledger

### Deployment Dependencies

A Railway account with capacity for the 2 services listed above, access to the selected image registries and GitHub source branch, and persistent volumes where shown are required. Keep volume-backed services at one replica. Provider accounts, SMTP and other optional integrations are supplied by the operator as described in First use and Scope and limitations.

### Upstream sources

- [Upstream project](https://github.com/beancount/fava)
- [Selected source reference](https://github.com/beancount/fava/tree/7096e25c6dcc48ab0059643b5592197492ddd0dc)
- Upstream source receipt: `7096e25c6dcc48ab0059643b5592197492ddd0dc`.
- Images are digest-pinned in `images.round8.lock.json`. Rolling image tags are frozen at the captured digest, not asserted to match the source commit unless independently established.
- Adapters and the gateway use `orenaksakal/railway-templates`, branch `codex/unique-template-drafts`, with repository-root Docker build context. Keep the branch available.
- [Configuration reference](https://github.com/beancount/fava/blob/main/contrib/docker/Dockerfile)
