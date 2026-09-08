# Deploy and Host Frappe CRM on Railway

Frappe CRM v1.83.0 manages leads, deals, contacts, and sales activity. This template builds the CRM app into the inspected framework image, then keeps web, worker, scheduler, WebSocket, and Nginx processes together so they can share one persistent site volume.

Release tested on Railway. See the validation scope below for verified workflows and remaining limitations.

## About Hosting Frappe CRM

The template defines 3 services with pinned container digests, generated deployment secrets, explicit service references, and persistent volumes for stateful dependencies. Repository-backed adapters build from `codex/remaining-template-drafts`. Railway terminates HTTPS for the public endpoints; databases and internal workers have no public TCP proxies. Fresh initialization was tested in an isolated Railway project. Each deployment has its own database and storage resources. Backups are not scheduled by this template, and filesystem-backed services should remain single-replica.

## Common Use Cases

- Track sales leads and deals.
- Organize customer contacts and assignments.
- Retain sales documents and activity history.

## Dependencies for Frappe CRM Hosting

### Deployment Dependencies

| Service | Source | Persistent path |
| --- | --- | --- |
| mariadb | `mariadb:10.11` | `/var/lib/mysql` |
| redis | `redis:7.4` | `/data` |
| frappe-crm | `templates/frappe-crm/Dockerfile` | `/data` |

Required input before deployment: none; generated secrets and service references supply the template defaults.

## First Use

After all services start, open the frappe-crm domain and sign in as `Administrator` using the generated `ADMIN_PASSWORD`. Change the password promptly. Keep `FRAPPE_SITE_NAME` stable; update `PUBLIC_URL` when changing the public domain. Configure your own email accounts before relying on outbound notifications.



## Scope and Limitations

The upstream tagged image was inspected and contains only the Frappe framework; this Dockerfile explicitly installs CRM and checks its import at build time. The application image built and installed successfully on Railway. One app replica is supported. Background processes intentionally share the same volume and service.

## Backups and Upgrades

Back up MariaDB and the entire /data site volume together, including site_config.json and encryption keys. Upgrades are blocked until ALLOW_MIGRATION=true is explicitly set for a backed-up existing site. Test restoration into an isolated project before depending on the backup. Image rollback alone does not revert database migrations.

## Validation Scope

Fresh Railway build and site installation, Administrator login, lead creation/read/update, private attachment upload/download, online background worker, restart and volume-preserving redeploy passed. MariaDB was dumped and restored into a separate database on the test service; archived attachment files were restored into a separate directory and compared byte-for-byte. Email delivery, SLA behavior, load testing, high availability and complete separate-project disaster recovery are not verified.

## Why Deploy Frappe CRM on Railway?

Railway keeps the services, networking, environment references, deployment logs, and volumes together in one project. This template supplies the tested service configuration. Railway resources and volume storage are billed separately from external email, model, and other service providers. No deployment cost or revenue estimate has been measured.

## Support and Upstream

[Upstream source and release](https://github.com/frappe/crm/tree/v1.83.0). This is an independent community integration; upstream licenses, trademarks, and paid-feature restrictions remain in effect. See the [draft readiness record](https://github.com/orenaksakal/railway-templates/blob/codex/remaining-template-drafts/DRAFTS.md). Report issues with redacted logs and image versions; never share credentials.
