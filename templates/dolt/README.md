# Deploy and Host Dolt SQL Server on Railway

Versioned MySQL-compatible SQL with persistent storage.

**Deployment template.** Deployment incurs Railway charges. Supply your own required model, search and external-service credentials; no example provider credentials are included.

## About Hosting Dolt SQL Server

This template provisions 1 services in one Railway project, with image digests or upstream source revisions pinned, generated internal credentials, linked environment variables and the persistent paths listed below. Public HTTP routes use Railway HTTPS. SQL and internal dependency endpoints stay private. Keep stateful services single-replica and configure your own backup policy.

## Live verification — 2026-09-08

Authenticated SQL write, Dolt add/commit, and record/history persistence across service restart passed. SQL remains private. Offsite backup, restore and public TLS were not tested.

## Setup

Connect from another service using dolt.DATABASE_URL. The app user has access to the app database. Root remains localhost-only. To connect from a laptop, deliberately configure a Railway TCP proxy and review transport security; none is created here.

## Dependencies for Dolt SQL Server Hosting

### Deployment Dependencies

| Service | Source | Persistent volume | Public HTTP |
|---|---|---|---|
| dolt | dolthub/dolt-sql-server:2.3.2 (digest pinned) | /var/lib/dolt | Private only |

## Required inputs

No external secrets are required for initial configuration. Follow the setup instructions for application-level onboarding.

Generated credentials: `dolt.DOLT_ROOT_PASSWORD`, `dolt.DOLT_PASSWORD`. Keep them private and preserve relevant encryption keys with backups. Every editor variable includes a description.

## Scope and limitations

One persistent service. This is a standalone database, with no DoltHub synchronization, remote backup or high availability configured. Versioned history is not an offsite backup.

## Recommended acceptance checks

Authenticated SQL connection; user grants; insert/commit/branch/merge; volume restart; export and restore. Verify external TLS before offering public SQL access.

## Operations

Keep database and internal service endpoints private. Railway provides HTTPS for the explicitly exposed HTTP services. Back up the listed persistent volumes and database exports, preserve encryption keys, and test a restore before relying on this instance. Review upstream migrations before upgrades. Single-volume services use one replica; no multi-region or high-availability guarantee is made. A gateway health response only proves the gateway is alive.

## Sources

- [Upstream project](https://github.com/dolthub/dolt)
- [Reviewed source snapshot](https://github.com/dolthub/dolt/tree/329729ad14a7c5239f54f1f185cd5c38ac765ce0)
- Image digest pins: `images.round4.lock.json` in the template source repository. Source snapshots are research references; image digests do not prove the image was built from that same commit.
- Base-image pins do not lock every package installed by apt/apk/pip. See the verification scope above before relying on this deployment.

## Common Use Cases

- Version application data with SQL commits and branches.
- Explore data changes through MySQL-compatible queries.

## Why Deploy Dolt SQL Server on Railway?

Railway groups service deployment, logs, private networking, generated environment references and persistent volumes in one project. This community template supplies the configuration and setup notes; Railway resource charges and external provider costs remain separate. No fixed cost or capacity guarantee is made.
