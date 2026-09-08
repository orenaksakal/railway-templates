# ToolJet Community Edition on Railway

Deploy ToolJet **v3.20.223-lts** with its internal database, PostgREST **12.0.2**, and persistent Valkey. The adapter uses the external queue service instead of the upstream image's non-persistent local Redis process.

## First use

Open the ToolJet service domain and create the initial administrator account. Build and publish an internal tool, connect a data source, and create/query a table in ToolJet Database.

Encryption/signing keys, the PostgREST JWT secret, queue dashboard password, and database/cache credentials are independently generated. PostgREST and all dependencies remain private. ToolJet's database role has `CREATEDB` and `CREATEROLE` because upstream creates additional databases and per-workspace roles; it is not a superuser.

`WORKER=true` enables the upstream job worker. The Python sandbox bypass remains **disabled**: Railway does not provide the capabilities required by every upstream sandbox mode. Python workflow execution is not advertised as supported by this recipe. Validate the specific workflow features you intend to use. Paid features retain their edition restrictions.

SMTP starts disabled. Configure the upstream SMTP variables and enable delivery before relying on invitations/password resets. Update `TOOLJET_HOST` when changing the public domain.

## Data and upgrades

Back up all application databases, including `tooljet`, `tooljet_data`, and any sample database created by upstream, plus role definitions and the persistent queue if pending jobs matter. Keep encryption keys: restoring the database without them can make saved datasource credentials unusable. Startup runs upstream database setup/migrations; test upgrades against restored data first.

Acceptance: administrator setup, datasource query, internal database table creation/query, published app use, a supported background job, restart/redeploy persistence, and restore. `/api/health` confirms server reachability, not these workflows.

Upstream: [ToolJet release](https://github.com/ToolJet/ToolJet/tree/v3.20.223-lts), [deployment guide](https://docs.tooljet.com/docs/setup/docker/).
