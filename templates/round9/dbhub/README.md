# Deploy and Host DBHub Database MCP

Read-only database MCP tools and web UI behind an owner gateway.

## About Hosting

| Service | Access | Persistent storage |
| --- | --- | --- |
| dbhub | Public HTTPS | None |
| app | Private | None |

Railway provides the public HTTPS endpoint. Dependencies stay on private networking. Keep each volume-backed service at one replica.

## Why Deploy DBHub Database MCP on Railway

This definition includes pinned container sources, documented storage paths and generated credentials where required. It restores the missing repository adapters from the previous draft and keeps the application setup steps explicit.

## Common Use Cases

Read-only database MCP tools and web UI behind an owner gateway.

## First use

- `app.DSN`: Required connection string for your existing database. Use a database user with read-only privileges.

Supply DSN for an existing database using a database-level read-only account. Use username admin and ACCESS_PASSWORD at the gateway, or send X-Template-Key with that password. The MCP endpoint is /mcp. The adapter writes a private TOML configuration exposing execute_sql with readonly=true and search_objects; the removed READONLY environment option is not used.

Where an owner gateway is included, the username is admin. API clients can use `X-Template-Key: YOUR_ACCESS_PASSWORD`. The gateway consumes Basic Authorization, preserves Bearer authorization and WebSocket upgrades, and caps requests at 32 MiB; check compatibility with native clients. Generated credentials must remain private.

## Scope and limitations

No database is included. A read-only database account remains required even with the tool-level restriction. Native MCP clients must support the gateway header or Basic authentication. Credentials stay in runtime environment variables and a mode-0600 temporary configuration file.

Source and static configuration checks are recorded in the repository's release report. Container builds, fresh Railway startup, native-client compatibility, full application workflows, backup restoration and costs have not been verified. A proxy healthcheck is not application readiness.

## Acceptance checks

Connect a read-only test database, initialize an MCP session, list tools, query a known row, verify a write is rejected and confirm anonymous requests receive 401.

Verify first use, unauthorized rejection where applicable, and a volume-preserving redeploy. Back up every persistent volume, generated application key and consistent database export. Restore into a separate instance and verify accounts, records and uploaded bytes before using important data. Container rollback does not revert database migrations.

## Dependencies for DBHub Database MCP

### Deployment Dependencies

A Railway account with capacity for 2 services, access to the selected registries and repository source, and the inputs listed above. External provider accounts and optional integrations are operator-supplied.

### Source and maintenance

- [Upstream project](https://github.com/bytebase/dbhub)
- [Reviewed application source](https://github.com/bytebase/dbhub/tree/9b57283a1b415711f846b9247a7d273e11bfa366)
- [Deployment adapter](https://github.com/orenaksakal/railway-templates/tree/codex/unique-template-drafts/templates/round9/dbhub)
- Repository services build from `orenaksakal/railway-templates`, branch `codex/unique-template-drafts`, with repository-root build context. Keep the branch available.
- Image digests and source references are tracked separately. A source revision is not asserted to match a rolling image unless the image metadata establishes it.

Upstream software retains its own license and trademarks. This community integration does not imply endorsement.
