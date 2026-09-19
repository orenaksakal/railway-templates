# Deploy and Host DomainMOD Portfolio Inventory

Domain and SSL asset inventory with MariaDB and protected administration.

## About Hosting

DomainMOD tracks domain registrations, renewal dates, SSL certificates and related Internet assets. This adapter builds the pinned application source on PHP 8.2 with MariaDB, a ten-minute task scheduler and a persistent temporary/export directory. It does not use the obsolete upstream PHP 7.4 container.

| Service | Access | Persistent storage |
| --- | --- | --- |
| mariadb | Private | /var/lib/mysql |
| core | Private | /data |
| domainmod | Public HTTPS | None |

Railway terminates public TLS. Keep volume-backed services at one replica. Database and core application ports are private; only the generated owner gateway is public.

## Why Deploy DomainMOD Portfolio Inventory on Railway

This integration supplies pinned image sources, private dependencies, persistent storage and an authenticated setup path. Public marketplace searches found no matching product listing at preparation time; the repository records the queries and exclusions.

## Common Use Cases

Maintain domain portfolios, inventory SSL certificates, track registrars and renewal dates, and report on Internet assets.

## First use

Open the gateway using its generated ACCESS_PASSWORD and username admin. Complete the DomainMOD installation form and create the application administrator as prompted. Database configuration is supplied from the linked MariaDB service. Add a test registrar and domain before importing a portfolio. Configure SMTP in DomainMOD if you need renewal email; no mail provider is included.

The owner gateway username is `admin`; retrieve its generated `ACCESS_PASSWORD` from Railway variables. API clients can send `X-Template-Key: YOUR_ACCESS_PASSWORD`. This preserves Bearer authorization; browser HTTP Basic credentials are consumed by the gateway. Keep all generated secrets private.

After gateway authentication, successful page responses set a Secure, HttpOnly owner cookie. This lets browser apps send their native API authorization while retaining gateway access. Rotating `ACCESS_PASSWORD` invalidates existing owner cookies. API clients can continue using `X-Template-Key`.

## Scope and limitations

The scheduler runs every ten minutes, but renewal notifications require an operator-configured mail provider. Registrar integrations and the optional WHM/cPanel Data Warehouse require your own credentials and compatible external services; those workflows are unverified. Treat saved registrar/API credentials as sensitive, follow upstream's credential-storage guidance and restrict gateway access. The application source is pinned at a reviewed commit rather than rebuilt from a rolling branch.

The gateway caps requests at 32 MiB and upstream requests at 600 seconds. Its `/healthz` only proves the proxy process is serving; it does not certify application or database readiness.

Container builds, fresh Railway startup, full application workflows, integrations, native-client compatibility, backup restoration and operating costs remain **unverified**. Source review and static checks are not a runtime certification.

## Acceptance checks

Complete installation, create a sample registrar and domain with a renewal date, export the record and verify it can be read. Check scheduler execution, then restart the app and database and confirm the domain and account remain. Validate a test notification only after configuring your own SMTP provider.

Back up a consistent MariaDB dump, /data and the generated database credentials. DomainMOD portfolio data lives in MariaDB; /data/temp preserves generated temporary exports. Restore both into a separate instance and verify authentication, domain records, SSL records and export behavior. Protect exported portfolio files as private data. Container rollback does not revert database migrations.

## Dependencies for DomainMOD Portfolio Inventory

### Deployment Dependencies

A Railway account with capacity for 3 services, persistent-volume support, access to the pinned container registries and this repository branch, and the inputs described above. Optional external providers and their credentials are operator-supplied.

### Source and maintenance

- [Upstream project](https://github.com/domainmod/domainmod)
- [Reviewed source](https://github.com/domainmod/domainmod/tree/9ff9e01070484c0fa519d4c43bf4d9192e081c37)
- [Deployment adapter](https://github.com/orenaksakal/railway-templates/tree/codex/unique-template-drafts/templates/round10/domainmod)
- Repository services build from `orenaksakal/railway-templates`, branch `codex/unique-template-drafts`, using repository-root context. Keep that branch available.
- Image digests and upstream source references are tracked separately. A source revision is not asserted to match an image without image provenance evidence.

Upstream software retains its own license and trademarks. This community integration does not imply endorsement.
