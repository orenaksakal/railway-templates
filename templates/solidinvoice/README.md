# Deploy and Host SolidInvoice Billing Workspace

Quotes and invoices with private MySQL and protected installation.

**Validation scope: source review and static checks.** This template meets the selection criterion through a public marketplace gap: no matching listing was found on September 19, 2026 using `SolidInvoice`, `Solid Invoice`. Searches are bounded; private, unindexed and differently named listings may exist. The selection does not claim any competitor is broken.

## About Hosting

| Service | Network | Persistent mount |
| --- | --- | --- |
| mysql | Private | /var/lib/mysql |
| core | Private | /etc/solidinvoice |
| solidinvoice | Public HTTPS | None |

The public gateway requires username **admin** and **ACCESS_PASSWORD** from the **solidinvoice** service. API clients can send `X-Template-Key: YOUR_ACCESS_PASSWORD`. Keep core and databases private. The gateway strips Basic Authorization, preserves Bearer authorization and WebSocket upgrades, and limits requests to 32 MiB. Verify native client compatibility before relying on it.

## Why Deploy SolidInvoice Billing Workspace on Railway

This template wires a protected HTTPS entry point to private application services, uses generated owner credentials, and declares the persistent mounts shown above. Repository adapters and pinned image references keep the deployment configuration reviewable. Application setup and the acceptance checks below remain operator responsibilities.

## Common Use Cases

Prepare client quotes; issue invoices; keep billing records for a small service business.

## First use

Complete the protected installer. Copy SETUP_DATABASE_HOST, PORT, NAME, USER and PASSWORD from core into its MySQL form; these helper variables are not automatic application settings. Create your own administrator and organization.

## Recommended acceptance checks

Create a client, quote and invoice; download a PDF, restart, and verify invoice data. Configure SMTP and test delivery only with your own account.

Test a volume-preserving redeploy as well as a restart. For stateful apps, take an application-consistent backup, including database/WAL and uploaded files, restore it into a separate disposable instance and verify account access and records. For configuration-as-code services, verify a clean rebuild from the saved source. Keep the original data until restoration passes.

## Scope and limitations

Payment gateways and tax/legal suitability are operator responsibilities. Preserve /etc/solidinvoice and a consistent MySQL backup together. No financial transaction is performed during drafting.

This template has source/configuration review and static checks only. No container build, Railway startup, browser/API workflow, volume recovery or cost measurement was performed. Saved editor fidelity is not deployment proof; `/healthz` proves only gateway readiness. Set operator-owned provider credentials only where needed and inspect the selected upstream license before commercial use.

## Dependencies for SolidInvoice Billing Workspace

### Deployment Dependencies

A Railway account with capacity for the 3 services listed above, access to the selected image registries and GitHub source branch, and persistent volumes where shown are required. Keep volume-backed services at one replica. Provider accounts, SMTP and other optional integrations are supplied by the operator as described in First use and Scope and limitations.

### Upstream sources

- [Upstream project](https://github.com/SolidInvoice/SolidInvoice)
- [Selected source reference](https://github.com/SolidInvoice/SolidInvoice/releases/tag/3.0.1)
- Upstream source receipt: `43c16ecac6eca20a8f0001dfe3f1fa95732a0050`.
- Images are digest-pinned in `images.round8.lock.json`. Rolling image tags are frozen at the captured digest, not asserted to match the source commit unless independently established.
- Adapters and the gateway use `orenaksakal/railway-templates`, branch `codex/unique-template-drafts`, with repository-root Docker build context. Keep the branch available.
- [Configuration reference](https://github.com/SolidInvoice/SolidInvoice/blob/3.0.1/docker-compose.yml)
- [Configuration reference](https://github.com/SolidInvoice/SolidInvoice/blob/3.0.1/docker/package.Dockerfile)
