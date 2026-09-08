# AFFiNE docs and whiteboards on Railway

Deploy AFFiNE **0.27.4** with PostgreSQL/pgvector and persistent Valkey. A startup adapter waits for dependencies and runs the upstream self-host initialization before starting the server.

## First use

Open the AFFiNE service domain and complete the initial administrator setup. Create a workspace, a document, and a whiteboard. Configure desktop/mobile clients to use this server if applicable.

The application volume is mounted at `/root/.affine`. It contains both `config` and `storage`, preserving the generated private key and local uploads together. Only the application is public; both data services remain private. Database and cache passwords are generated independently for every deployment.

`AFFINE_SERVER_EXTERNAL_URL` is generated from the Railway domain. Update it when using a custom domain. Configure mail and any optional model providers in AFFiNE's self-host administration interface. The template starts with `AFFINE_INDEXER_ENABLED=false`, matching the selected upstream Compose baseline; do not advertise indexer or model-backed features as configured by default.

## Operations

Back up PostgreSQL and the full application volume, including the private key. Keep one application replica with filesystem storage. Test upgrades on a restored copy: startup invokes upstream schema/data migrations and image rollback alone does not undo them.

Acceptance: create a workspace, edit a document, synchronize two clients, upload/download a file, restart and redeploy without losing content or signing configuration, then restore a backup. `/info` provides version/readiness information but does not prove client synchronization.

Upstream: [AFFiNE 0.27.4](https://github.com/toeverything/AFFiNE/tree/v0.27.4), [selected self-host configuration](https://github.com/toeverything/AFFiNE/blob/v0.27.4/.docker/selfhost/compose.yml). Paid upstream features retain their normal restrictions.
