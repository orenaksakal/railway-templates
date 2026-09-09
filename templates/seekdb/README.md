# Deploy and Host OceanBase seekdb on Railway

MySQL-compatible hybrid search database with a protected console.

**Deployment template.** Deployment incurs Railway charges. Supply your own required model, search and external-service credentials; no example provider credentials are included.

## About Hosting OceanBase seekdb

This template provisions 1 services in one Railway project, with image digests or upstream source revisions pinned, generated internal credentials, linked environment variables and the persistent paths listed below. Public HTTP routes use Railway HTTPS. SQL and internal dependency endpoints stay private. Keep stateful services single-replica and configure your own backup policy.

## Live verification — 2026-09-08

Fresh build and startup, public console route, authenticated SQL writes and record persistence across restart passed with 4G database memory and 2G redo allocation. Vector/full-text ranking quality, restore, high availability and public SQL TLS were not tested. SQL remains private.

## Setup

Open the seekdb domain on the provided web console and use ROOT_PASSWORD. Services in the same project connect with DATABASE_URL on private port 2881. No SQL TCP proxy is created.

## Dependencies for OceanBase seekdb Hosting

### Deployment Dependencies

| Service | Source | Persistent volume | Public HTTP |
|---|---|---|---|
| seekdb | repository adapter: templates/seekdb/Dockerfile | /var/lib/seekdb | 2886 |

## Required inputs

No external secrets are required for initial configuration. Follow the setup instructions for application-level onboarding.

Generated credentials: `seekdb.ROOT_PASSWORD`. Keep them private and preserve relevant encryption keys with backups. Every editor variable includes a description.

## Scope and limitations

Upstream minimum: one physical core and 2 GB memory. Template settings use CPU_COUNT=2 and MEMORY_LIMIT=4G; configure a Railway memory limit above the database setting to leave process overhead. This is one node, without high availability, scheduled backups or additional SQL application users. Create a least-privilege SQL user for your application.

## Recommended acceptance checks

Container boot within resource limits; console password enforcement; private SQL connection; vector/full-text/hybrid query; volume restart; backup and restore; application-user grants.

## Operations

Keep database and internal service endpoints private. Railway provides HTTPS for the explicitly exposed HTTP services. Back up the listed persistent volumes and database exports, preserve encryption keys, and test a restore before relying on this instance. Review upstream migrations before upgrades. Single-volume services use one replica; no multi-region or high-availability guarantee is made. A gateway health response only proves the gateway is alive.

## Sources

- [Upstream project](https://github.com/oceanbase/seekdb)
- [Reviewed source snapshot](https://github.com/oceanbase/seekdb/tree/31a5fa633f1d34fd8892e937339e2dffb14adc69)
- Image digest pins: `images.round4.lock.json` in the template source repository. Source snapshots are research references; image digests do not prove the image was built from that same commit.
- Base-image pins do not lock every package installed by apt/apk/pip. See the verification scope above before relying on this deployment.

## Common Use Cases

- Store application data behind a private MySQL-compatible SQL endpoint.
- Explore vector, full-text and hybrid search using your own datasets.

## Why Deploy OceanBase seekdb on Railway?

Railway groups service deployment, logs, private networking, generated environment references and persistent volumes in one project. This community template supplies the configuration and setup notes; Railway resource charges and external provider costs remain separate. No fixed cost or capacity guarantee is made.
