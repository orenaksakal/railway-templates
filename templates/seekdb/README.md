# OceanBase seekdb

Hybrid search database with MySQL-compatible SQL, persistent data and a password-protected web console.

**Unpublished draft — not runtime-validated or approved for release.** Saving this template does not deploy services. Deployment later incurs Railway and provider charges.

## Setup

Open the seekdb domain on the provided web console and use ROOT_PASSWORD. Services in the same project connect with DATABASE_URL on private port 2881. No SQL TCP proxy is created.

### Deployment Dependencies

| Service | Source | Persistent volume | Public HTTP |
|---|---|---|---|
| seekdb | oceanbase/seekdb:1.4.0-100000172026082615 (digest pinned) | /var/lib/oceanbase | 2886 |

## Required inputs

No external secrets are required for initial configuration. Follow the setup instructions for application-level onboarding.

Generated credentials: `seekdb.ROOT_PASSWORD`. Keep them private and preserve relevant encryption keys with backups. Every editor variable includes a description.

## Scope and limitations

Upstream minimum: one physical core and 2 GB memory. Draft settings use CPU_COUNT=2 and MEMORY_LIMIT=2G; configure a Railway memory limit above the database setting to leave process overhead. This is one node, without high availability, scheduled backups or additional SQL application users. Create a least-privilege SQL user for your application.

## Release gates

Container boot within resource limits; console password enforcement; private SQL connection; vector/full-text/hybrid query; volume restart; backup and restore; application-user grants.

## Operations

Keep database and internal service endpoints private. Railway provides HTTPS for the explicitly exposed HTTP services. Back up the listed persistent volumes and database exports, preserve encryption keys, and test a restore before relying on this instance. Review upstream migrations before upgrades. Single-volume services use one replica; no multi-region or high-availability guarantee is made. A gateway health response only proves the gateway is alive.

## Sources

- [Upstream project](https://github.com/oceanbase/seekdb)
- [Reviewed source snapshot](https://github.com/oceanbase/seekdb/tree/31a5fa633f1d34fd8892e937339e2dffb14adc69)
- Image digest pins: `images.round4.lock.json` in the template source repository. Source snapshots are research references; image digests do not prove the image was built from that same commit.
- Build and runtime verification remain pending. Base-image pins do not lock packages installed by apt/apk/pip.
