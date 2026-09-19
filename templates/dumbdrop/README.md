# Deploy and Host DumbDrop Private File Inbox

A persistent file-upload inbox protected by gateway and generated PIN.

**Validation scope: source review and static checks.** This template meets the selection criterion through a public marketplace gap: no matching listing was found on September 19, 2026 using `DumbDrop`, `Dumb Drop`, `DumbWare`. Searches are bounded; private, unindexed and differently named listings may exist. The selection does not claim any competitor is broken.

## About Hosting

| Service | Network | Persistent mount |
| --- | --- | --- |
| core | Private | /app/uploads |
| dumbdrop | Public HTTPS | None |

The public gateway requires username **admin** and **ACCESS_PASSWORD** from the **dumbdrop** service. API clients can send `X-Template-Key: YOUR_ACCESS_PASSWORD`. Keep core and databases private. The gateway strips Basic Authorization, preserves Bearer authorization and WebSocket upgrades, and limits requests to 32 MiB. Verify native client compatibility before relying on it.

## Why Deploy DumbDrop Private File Inbox on Railway

This template wires a protected HTTPS entry point to private application services, uses generated owner credentials, and declares the persistent mounts shown above. Repository adapters and pinned image references keep the deployment configuration reviewable. Application setup and the acceptance checks below remain operator responsibilities.

## Common Use Cases

Collect files from trusted uploaders; receive small project deliverables; maintain a private upload inbox.

## First use

Unlock the gateway and enter DUMBDROP_PIN from core. Files are stored in /app/uploads. The application limit is 25 MB and gateway request limit is 32 MiB.

## Recommended acceptance checks

Upload a small synthetic file, inspect and retrieve it through an authenticated operator workflow, restart and confirm the file remains. Verify oversized uploads are rejected.

Test a volume-preserving redeploy as well as a restart. For stateful apps, take an application-consistent backup, including database/WAL and uploaded files, restore it into a separate disposable instance and verify account access and records. For configuration-as-code services, verify a clean rebuild from the saved source. Keep the original data until restoration passes.

## Scope and limitations

An upload inbox, not an anonymous sharing site. No automatic retention or offsite backup is configured; set storage limits and cleanup rules before inviting uploaders.

This template has source/configuration review and static checks only. No container build, Railway startup, browser/API workflow, volume recovery or cost measurement was performed. Saved editor fidelity is not deployment proof; `/healthz` proves only gateway readiness. Set operator-owned provider credentials only where needed and inspect the selected upstream license before commercial use.

## Dependencies for DumbDrop Private File Inbox

### Deployment Dependencies

A Railway account with capacity for the 2 services listed above, access to the selected image registries and GitHub source branch, and persistent volumes where shown are required. Keep volume-backed services at one replica. Provider accounts, SMTP and other optional integrations are supplied by the operator as described in First use and Scope and limitations.

### Upstream sources

- [Upstream project](https://github.com/DumbWareio/DumbDrop)
- [Selected source reference](https://github.com/DumbWareio/DumbDrop/tree/ff8f813f493e89c7da056e7a3101ce2ef48e3960)
- Upstream source receipt: `ff8f813f493e89c7da056e7a3101ce2ef48e3960`.
- Images are digest-pinned in `images.round8.lock.json`. Rolling image tags are frozen at the captured digest, not asserted to match the source commit unless independently established.
- Adapters and the gateway use `orenaksakal/railway-templates`, branch `codex/unique-template-drafts`, with repository-root Docker build context. Keep the branch available.
- [Configuration reference](https://github.com/DumbWareio/DumbDrop/blob/main/.env.example)
- [Configuration reference](https://github.com/DumbWareio/DumbDrop/blob/main/Dockerfile)
- [Configuration reference](https://github.com/DumbWareio/DumbDrop/blob/main/docker-compose.yml)
