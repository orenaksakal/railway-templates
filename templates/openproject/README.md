# OpenProject project management on Railway

Deploy OpenProject **17.8.0** with a dedicated PostgreSQL 17 database. The upstream all-in-one application image supervises the web application, job worker, cache, Apache proxy, and bundled Hocuspocus collaboration process. Its internal PostgreSQL process is disabled by using the separate database URL.

This topology keeps application processes and attachments on one service, avoiding unsupported shared volumes between Railway services.

## First use

Open the application domain. Sign in as `admin` using the generated `OPENPROJECT_SEED__ADMIN__USER__PASSWORD` from the OpenProject service variables. The seed configuration requests a password change. Configure the administrator's email and SMTP before relying on notifications.

`OPENPROJECT_HOST__NAME` follows the Railway domain; HTTPS and HSTS are enabled for the public Railway deployment. If assigning a custom domain, update the hostname as well. The database URL deliberately has no Rails-specific query parameters because the upstream startup script also passes it to `psql`.

## Data and maintenance

Attachments are stored in `/var/openproject/assets`; database data resides in the Postgres service volume. Back up both as a consistent pair. Retain `SECRET_KEY_BASE`. The application initializes/seeds the database and runs migrations at startup; test upgrades using a restored copy before release.

Use one application replica. Incoming IMAP email processing is optional and requires its own configuration. Enterprise features require an upstream license. This is not a high-availability setup.

Acceptance: sign in, create a project and work package, upload/download an attachment, verify a background notification and collaborative editing, restart/redeploy, and restore both data stores. `/health_checks/default` is the deployment probe, not a full workflow test.

Upstream: [OpenProject 17.8.0](https://github.com/opf/openproject/tree/v17.8.0), [Docker installation](https://www.openproject.org/docs/installation-and-operations/installation/docker/).
