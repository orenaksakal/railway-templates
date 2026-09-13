# Deploy and Host MCPJungle Enterprise Mode on Railway

MCP registry and gateway with PostgreSQL and a protected initialization.

**Unpublished draft. Image builds and Railway application workflows have not been validated.** The template defines services; saving a draft creates no running application. Deploying it later incurs Railway usage and any external provider charges.

## About Hosting MCPJungle Enterprise Mode

Three services: MCPJungle, PostgreSQL and owner gateway. Upstream enterprise mode is a server authorization mode, not a bundled commercial license. The uninitialized service is private behind the owner gate. The standard distroless image supports the included runtime; arbitrary local stdio programs and host-shell tools are not installed. Prefer remote HTTP MCP servers. Mozilla Public License 2.0 upstream terms apply. Client tooling must support the additional header.

## Setup

Open mcpjungle with username admin and mcpjungle.ACCESS_PASSWORD. Initialize once by sending POST /init with JSON {"mode":"enterprise"} and X-Template-Key set to ACCESS_PASSWORD. Save the returned admin_access_token securely; never put it in template defaults or logs. Use that token for subsequent native API authorization, retaining X-Template-Key for gateway access.

### Deployment Dependencies

| Service | Source | Persistent volume | Public HTTP port |
| --- | --- | --- | --- |
| postgres | postgres:17-alpine | /var/lib/postgresql/data | Private |
| core | ghcr.io/mcpjungle/mcpjungle:0.4.6 | None | Private |
| mcpjungle | Repository adapter: shared/round6-gateway/Dockerfile | None | 8080 |

## Operator inputs

| Variable | Requirement |
| --- | --- |
| None | Initial credentials are generated; complete application setup above. |

Generated credentials: `postgres.POSTGRES_PASSWORD`, `mcpjungle.ACCESS_PASSWORD`. Never copy another deployment's secrets. Preserve encryption/signing keys with backups.

## Why Deploy MCPJungle Enterprise Mode on Railway

The definition connects private dependencies, declares persistent volumes and exposes the listed application endpoints through Railway HTTPS. Repository adapters build from `codex/fifteen-template-drafts` with the repository root as Docker context. Configure one replica for each stateful service.

## Common Use Cases

MCP registry and gateway with PostgreSQL and a protected initialization. Use a separate test project to verify the workflow below before putting real data into the instance.

## Dependencies for MCPJungle Enterprise Mode

Reviewed upstream release: [0.4.6](https://github.com/mcpjungle/MCPJungle/tree/12648be5edc70391dc3f9c4aecfd37b83b3e30be). Image digests are recorded in `images.round6.lock.json`; source receipts are in `sources.round6.lock.json`. A matching version label does not independently prove image-to-source provenance. Base-image pins do not lock later apt/apk or language-package resolution.

## Recommended acceptance checks

Fresh database; anonymous init rejection; initialize and securely capture the admin token; confirm repeat initialization cannot seize ownership; register a remote test server; discover and invoke a tool; verify permission rejection and streaming; restart without losing registry/users; restore PostgreSQL.

## Operations and recovery

Back up every listed persistent volume and export every application database, preserving the generated encryption/signing secrets. Restore into a separate test instance and repeat the functional workflow before relying on the backup. Keep internal databases private. An owner gateway `/healthz` response proves only that gateway is alive, not that its application or dependencies are ready. After changing a public domain, update all application origin and callback settings. Review upstream migrations before upgrading; record the old source/image pins and a recoverable backup. No scheduled backup service is configured by this draft.

## Validation status

The checked-in catalog supports static pin, reference, Docker COPY-path and script-syntax validation. Container builds, native proxy behavior, fresh Railway deployment, provider integrations, persistence and restore remain release gates. See `DRAFTS-ROUND-6.md` for the batch record.
