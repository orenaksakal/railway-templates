# Deploy and Host DumbBudget Personal Finance

Manual budgets and transactions with persistent owner-protected data.

**Validation scope: source review and static checks.** This template meets the selection criterion through a public marketplace gap: no matching listing was found on September 19, 2026 using `DumbBudget`, `Dumb Budget`, `DumbWare`. Searches are bounded; private, unindexed and differently named listings may exist. The selection does not claim any competitor is broken.

## About Hosting

| Service | Network | Persistent mount |
| --- | --- | --- |
| core | Private | /app/data |
| dumbbudget | Public HTTPS | None |

The public gateway requires username **admin** and **ACCESS_PASSWORD** from the **dumbbudget** service. API clients can send `X-Template-Key: <ACCESS_PASSWORD>`. Keep core and databases private. The gateway strips Basic Authorization, preserves Bearer authorization and WebSocket upgrades, and limits requests to 32 MiB. Verify native client compatibility before relying on it.

## Why Deploy DumbBudget Personal Finance on Railway

This template wires a protected HTTPS entry point to private application services, uses generated owner credentials, and declares the persistent mounts shown above. Repository adapters and pinned image references keep the deployment configuration reviewable. Application setup and the acceptance checks below remain operator responsibilities.

## Common Use Cases

Record manual income and expenses; monitor personal budgets; export transaction history.

## First use

Unlock the gateway and enter DUMBBUDGET_PIN from core. Set your currency and create an initial budget.

## Recommended acceptance checks

Add an income and expense, check totals, export records, restart and verify the balances remain.

Test a volume-preserving redeploy as well as a restart. For stateful apps, take an application-consistent backup, including database/WAL and uploaded files, restore it into a separate disposable instance and verify account access and records. For configuration-as-code services, verify a clean rebuild from the saved source. Keep the original data until restoration passes.

## Scope and limitations

Manual personal finance tracking. No bank synchronization, regulated accounting or multi-user isolation is included. The rolling image is captured by digest.

This template has source/configuration review and static checks only. No container build, Railway startup, browser/API workflow, volume recovery or cost measurement was performed. Saved editor fidelity is not deployment proof; `/healthz` proves only gateway readiness. Set operator-owned provider credentials only where needed and inspect the selected upstream license before commercial use.

## Dependencies for DumbBudget Personal Finance

### Deployment Dependencies

A Railway account with capacity for the 2 services listed above, access to the selected image registries and GitHub source branch, and persistent volumes where shown are required. Keep volume-backed services at one replica. Provider accounts, SMTP and other optional integrations are supplied by the operator as described in First use and Scope and limitations.

### Upstream sources

- [Upstream project](https://github.com/DumbWareio/DumbBudget)
- [Selected source reference](https://github.com/DumbWareio/DumbBudget/tree/b9db5cb32d14b7b78675d8be054611d4829253ef)
- Upstream source receipt: `b9db5cb32d14b7b78675d8be054611d4829253ef`.
- Images are digest-pinned in `images.round8.lock.json`. Rolling image tags are frozen at the captured digest, not asserted to match the source commit unless independently established.
- Adapters and the gateway use `orenaksakal/railway-templates`, branch `codex/unique-template-drafts`, with repository-root Docker build context. Keep the branch available.
- [Configuration reference](https://github.com/DumbWareio/DumbBudget/blob/main/Dockerfile)
- [Configuration reference](https://github.com/DumbWareio/DumbBudget/blob/main/docker-compose.yml)
