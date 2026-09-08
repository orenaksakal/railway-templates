# Deploy and Host OpenProject on Railway

Deploy OpenProject **17.8.0** with a dedicated PostgreSQL 17 database. The upstream all-in-one application image supervises the web application, job worker, cache, Apache proxy, and bundled Hocuspocus collaboration process. Its internal PostgreSQL process is disabled by using the separate database URL.

## About Hosting OpenProject

This two-service deployment pairs the OpenProject all-in-one image with a dedicated PostgreSQL database. The application image supervises the web server, background worker, cache, Apache proxy, and bundled collaboration process. Its internal PostgreSQL process is disabled in favor of the private database service. Railway provides the public HTTPS endpoint, while attachments and database contents are stored on separate persistent volumes. Startup initializes and migrates the database and generates an initial administrator password through Railway variables. After deployment, sign in, change that password, and configure email delivery. Keep one application replica so the local attachment store remains consistent.

## Common Use Cases

- Plan projects with work packages, milestones, and timelines.
- Track team tasks and progress in a shared project workspace.
- Maintain project attachments and collaborative work-package content.

## Dependencies for OpenProject Hosting

- OpenProject 17.8.0 all-in-one image with its included worker and collaboration processes.
- A dedicated private PostgreSQL 17 service.
- Persistent database and application attachment volumes.
- Optional SMTP server for notifications and upstream licenses for enterprise features.

This topology keeps application processes and attachments on one service, avoiding unsupported shared volumes between Railway services.

## First use

Open the application domain. Sign in as `admin` using the generated `OPENPROJECT_SEED__ADMIN__USER__PASSWORD` from the OpenProject service variables. The seed configuration requests a password change. Configure the administrator's email and SMTP before relying on notifications.

`OPENPROJECT_HOST__NAME` follows the Railway domain; HTTPS and HSTS are enabled for the public Railway deployment. If assigning a custom domain, update the hostname as well. The database URL deliberately has no Rails-specific query parameters because the upstream startup script also passes it to `psql`.

## Data and maintenance

Attachments are stored in `/var/openproject/assets`; database data resides in the Postgres service volume. Back up both as a consistent pair. Retain `SECRET_KEY_BASE`. The application initializes/seeds the database and runs migrations at startup; test upgrades using a restored copy before release.

Use one application replica. Incoming IMAP email processing is optional and requires its own configuration. Enterprise features require an upstream license. This is not a high-availability setup.

Acceptance: sign in, create a project and work package, upload/download an attachment, verify a background notification and collaborative editing, restart/redeploy, and restore both data stores. `/health_checks/default` is the deployment probe, not a full workflow test.

Upstream: [OpenProject 17.8.0](https://github.com/opf/openproject/tree/v17.8.0), [Docker installation](https://www.openproject.org/docs/installation-and-operations/installation/docker/).

## Why Deploy OpenProject on Railway?

Railway keeps the application and its dependencies in one project, with service references, private networking, HTTPS routing, deployment logs, and persistent volumes. This template supplies the service configuration and startup adapters so you can focus on the application setup. Resource usage and volume storage are billed by Railway; third-party services are billed separately. This deployment does not configure automatic backups or high availability.

## Support and Validation

This is an independently maintained community template. Local startup checks and exact Railway template-configuration read-back have passed. Full Railway application workflows and backup/restore certification remain outstanding; test your intended workflow before relying on the deployment. See the [validation record](https://github.com/orenaksakal/railway-templates/blob/codex/railway-template-release/VALIDATION.md) for the tested scope.

For template issues, use the Railway listing’s community thread or [open a repository issue](https://github.com/orenaksakal/railway-templates/issues). Include the service name, image version, and redacted logs; never include passwords, tokens, or connection strings.
