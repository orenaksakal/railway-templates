# Deploy and Host AFFiNE on Railway

Deploy AFFiNE **0.27.4** with PostgreSQL/pgvector and persistent Valkey. A startup adapter waits for dependencies and runs the upstream self-host initialization before starting the server.

## About Hosting AFFiNE

This three-service deployment hosts AFFiNE with PostgreSQL/pgvector and Valkey. Railway builds the application and database adapters from the included Dockerfiles, creates the private service connections, and exposes the application over HTTPS. Startup waits for dependencies and runs the upstream self-host initialization. The application volume preserves configuration, signing keys, and uploaded files; PostgreSQL and Valkey also use persistent storage. Create an administrator and workspace after deployment, then configure any email or optional provider settings in AFFiNE. Keep one application replica with the included filesystem storage and back up both the database and application volume before upgrades.

## Common Use Cases

- Maintain team documentation and a shared knowledge workspace.
- Combine written notes and visual planning on whiteboards.
- Host personal or small-team documents with control over stored files.

## Dependencies for AFFiNE Hosting

- AFFiNE 0.27.4 with its upstream self-host initialization.
- Private PostgreSQL with pgvector and persistent Valkey.
- A Railway account with capacity for three services and their volumes.
- Optional SMTP and model-provider configuration for the features you enable.

## First use

Open the AFFiNE service domain and complete the initial administrator setup. Create a workspace, a document, and a whiteboard. Configure desktop/mobile clients to use this server if applicable.

The application volume is mounted at `/root/.affine`. It contains both `config` and `storage`, preserving the generated private key and local uploads together. Only the application is public; both data services remain private. Database and cache passwords are generated independently for every deployment.

`AFFINE_SERVER_EXTERNAL_URL` is generated from the Railway domain. Update it when using a custom domain. Configure mail and any optional model providers in AFFiNE's self-host administration interface. The template starts with `AFFINE_INDEXER_ENABLED=false`, matching the selected upstream Compose baseline; do not advertise indexer or model-backed features as configured by default.

## Operations

Back up PostgreSQL and the full application volume, including the private key. Keep one application replica with filesystem storage. Test upgrades on a restored copy: startup invokes upstream schema/data migrations and image rollback alone does not undo them.

Acceptance: create a workspace, edit a document, synchronize two clients, upload/download a file, restart and redeploy without losing content or signing configuration, then restore a backup. `/info` provides version/readiness information but does not prove client synchronization.

Upstream: [AFFiNE 0.27.4](https://github.com/toeverything/AFFiNE/tree/v0.27.4), [selected self-host configuration](https://github.com/toeverything/AFFiNE/blob/v0.27.4/.docker/selfhost/compose.yml). Paid upstream features retain their normal restrictions.

## Why Deploy AFFiNE on Railway?

Railway keeps the application and its dependencies in one project, with service references, private networking, HTTPS routing, deployment logs, and persistent volumes. This template supplies the service configuration and startup adapters so you can focus on the application setup. Resource usage and volume storage are billed by Railway; third-party services are billed separately. This deployment does not configure automatic backups or high availability.

## Support and Validation

This is an independently maintained community template. Local startup checks and exact Railway template-configuration read-back have passed. Full Railway application workflows and backup/restore certification remain outstanding; test your intended workflow before relying on the deployment. See the [validation record](https://github.com/orenaksakal/railway-templates/blob/main/VALIDATION.md) for the tested scope.

For template issues, use the Railway listing’s community thread or [open a repository issue](https://github.com/orenaksakal/railway-templates/issues). Include the service name, image version, and redacted logs; never include passwords, tokens, or connection strings.
