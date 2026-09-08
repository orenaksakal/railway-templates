# Deploy and Host Frappe Helpdesk on Railway

Frappe Helpdesk v1.30.1 provides customer support ticket management. The template installs Helpdesk and its required pinned Telephony dependency into the framework image and runs all site-file consumers together in one application service.

Release tested on Railway. See the validation scope below for verified workflows and remaining limitations.

## About Hosting Frappe Helpdesk

The template defines 3 services with pinned container digests, generated deployment secrets, explicit service references, and persistent volumes for stateful dependencies. Repository-backed adapters build from `codex/remaining-template-drafts`. Railway terminates HTTPS for the public endpoints; databases and internal workers have no public TCP proxies. Fresh initialization was tested in an isolated Railway project. Each deployment has its own database and storage resources. Backups are not scheduled by this template, and filesystem-backed services should remain single-replica.

## Common Use Cases

- Create and assign customer support tickets.
- Manage agents, customers, and ticket attachments.
- Configure an email-driven support workflow.

## Dependencies for Frappe Helpdesk Hosting

### Deployment Dependencies

| Service | Source | Persistent path |
| --- | --- | --- |
| mariadb | `mariadb:10.11` | `/var/lib/mysql` |
| redis | `redis:7.4` | `/data` |
| frappe-helpdesk | `templates/frappe-helpdesk/Dockerfile` | `/data` |

Required input before deployment: none; generated secrets and service references supply the template defaults.

## First Use

Open the frappe-helpdesk domain after initialization. Sign in as `Administrator` using the generated `ADMIN_PASSWORD`, change it, and configure agents and email accounts. SMTP and incoming email are not supplied; use your own provider and verify delivery.



## Scope and Limitations

The required Telephony source commit is pinned. The pinned application image built and installed successfully on Railway. One application replica is supported; this is not an HA or shared-volume cluster.

## Backups and Upgrades

Back up MariaDB, the complete /data site volume, and encryption keys. Explicitly enable migrations only after a backup and a successful restored-copy upgrade test. Test restoration into an isolated project before depending on the backup. Image rollback alone does not revert database migrations.

## Validation Scope

Fresh Railway build and site installation, Administrator login, ticket creation/read/update, private attachment upload/download, online background worker, restart and volume-preserving redeploy passed. MariaDB was dumped and restored into a separate database on the test service; archived attachment files were restored into a separate directory and compared byte-for-byte. Email delivery, SLA behavior, load testing, high availability and complete separate-project disaster recovery are not verified.

## Why Deploy Frappe Helpdesk on Railway?

Railway keeps the services, networking, environment references, deployment logs, and volumes together in one project. This template supplies the tested service configuration. Railway resources and volume storage are billed separately from external email, model, and other service providers. No deployment cost or revenue estimate has been measured.

## Support and Upstream

[Upstream source and release](https://github.com/frappe/helpdesk/tree/v1.30.1). This is an independent community integration; upstream licenses, trademarks, and paid-feature restrictions remain in effect. See the [draft readiness record](https://github.com/orenaksakal/railway-templates/blob/codex/remaining-template-drafts/DRAFTS.md). Report issues with redacted logs and image versions; never share credentials.
