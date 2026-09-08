# Deploy and Host ToolJet on Railway

Deploy ToolJet **v3.20.223-lts** with its internal database, PostgREST **12.0.2**, and persistent Valkey. The adapter uses the external queue service instead of the upstream image's non-persistent local Redis process.

## About Hosting ToolJet

This four-service deployment combines ToolJet Community Edition, PostgreSQL, PostgREST, and Valkey. Railway exposes the ToolJet web application over HTTPS while the database, data API, and queue remain private. The startup adapter runs upstream database setup and migrations and uses persistent Valkey instead of the application image’s local Redis process. Railway generates the signing, encryption, database, and PostgREST secrets. Create the initial administrator after deployment, connect a data source, and test a published internal tool. Preserve the encryption keys when backing up or restoring databases. Optional SMTP and workflow features need their own configuration and validation.

## Common Use Cases

- Build internal dashboards and administrative tools.
- Create forms and interfaces over existing business data sources.
- Build internal applications using the included ToolJet Database.

## Dependencies for ToolJet Hosting

- ToolJet Community Edition v3.20.223-lts.
- Private PostgreSQL, PostgREST 12.0.2, and persistent Valkey.
- A Railway account with capacity for four services and their persistent data.
- Optional SMTP and data-source credentials; upstream licenses for paid features.

## First use

Open the ToolJet service domain and create the initial administrator account. Build and publish an internal tool, connect a data source, and create/query a table in ToolJet Database.

Encryption/signing keys, the PostgREST JWT secret, queue dashboard password, and database/cache credentials are independently generated. PostgREST and all dependencies remain private. ToolJet's database role has `CREATEDB` and `CREATEROLE` because upstream creates additional databases and per-workspace roles; it is not a superuser.

`WORKER=true` enables the upstream job worker. The Python sandbox bypass remains **disabled**: Railway does not provide the capabilities required by every upstream sandbox mode. Python workflow execution is not advertised as supported by this recipe. Validate the specific workflow features you intend to use. Paid features retain their edition restrictions.

SMTP starts disabled. Configure the upstream SMTP variables and enable delivery before relying on invitations/password resets. Update `TOOLJET_HOST` when changing the public domain.

## Data and upgrades

Back up all application databases, including `tooljet`, `tooljet_data`, and any sample database created by upstream, plus role definitions and the persistent queue if pending jobs matter. Keep encryption keys: restoring the database without them can make saved datasource credentials unusable. Startup runs upstream database setup/migrations; test upgrades against restored data first.

Acceptance: administrator setup, datasource query, internal database table creation/query, published app use, a supported background job, restart/redeploy persistence, and restore. `/api/health` confirms server reachability, not these workflows.

Upstream: [ToolJet release](https://github.com/ToolJet/ToolJet/tree/v3.20.223-lts), [deployment guide](https://docs.tooljet.com/docs/setup/docker/).

## Why Deploy ToolJet on Railway?

Railway keeps the application and its dependencies in one project, with service references, private networking, HTTPS routing, deployment logs, and persistent volumes. This template supplies the service configuration and startup adapters so you can focus on the application setup. Resource usage and volume storage are billed by Railway; third-party services are billed separately. This deployment does not configure automatic backups or high availability.

## Support and Validation

This is an independently maintained community template. Local startup checks and exact Railway template-configuration read-back have passed. Full Railway application workflows and backup/restore certification remain outstanding; test your intended workflow before relying on the deployment. See the [validation record](https://github.com/orenaksakal/railway-templates/blob/codex/railway-template-release/VALIDATION.md) for the tested scope.

For template issues, use the Railway listing’s community thread or [open a repository issue](https://github.com/orenaksakal/railway-templates/issues). Include the service name, image version, and redacted logs; never include passwords, tokens, or connection strings.
