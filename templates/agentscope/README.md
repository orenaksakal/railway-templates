# AgentScope Service API

AgentScope API with Redis state and persistent agent workspaces.

**Deployment template.** Deployment incurs Railway charges. Supply your own required model, search and external-service credentials; no example provider credentials are included.

## Live verification — 2026-09-08

Source build, gateway authentication, agent creation and Redis-backed session creation/listing passed. Model inference was not tested. This is a trusted-owner API service, without the separate upstream UI or a multi-tenant security claim.

## Setup

Use the agentscope domain with gateway ACCESS_USER and ACCESS_PASSWORD. Open /docs and configure model credentials and agents through the upstream API. The service uses one Uvicorn worker and an in-process message bus.

### Deployment Dependencies

| Service | Source | Persistent volume | Public HTTP |
|---|---|---|---|
| redis | redis:7.4 (digest pinned) | /data | Private only |
| service | repository adapter: templates/agentscope/Dockerfile | /data | Private only |
| agentscope | repository adapter: shared/round4-gateway/Dockerfile | None | 8080 |

## Required inputs

No external secrets are required for initial configuration. Follow the setup instructions for application-level onboarding.

Generated credentials: `redis.REDIS_PASSWORD`, `agentscope.ACCESS_PASSWORD`. Keep them private and preserve relevant encryption keys with backups. Every editor variable includes a description.

## Scope and limitations

API-only draft: the separate upstream web UI is not bundled. Knowledge bases, default Playwright MCP, chat channels and external execution sandboxes are not enabled. LocalWorkspace tools can execute code inside this service; use one trusted owner, not untrusted tenants. Redis persists state and /data persists workspaces. Python transitive packages need a resolved dependency lock after the first build.

## Recommended acceptance checks

Clean build; authenticated API; provider setup; agent run and streaming; session persistence; workspace restart; restore Redis and files together; verify tool permissions and service resource limits.

## Operations

Keep database and internal service endpoints private. Railway provides HTTPS for the explicitly exposed HTTP services. Back up the listed persistent volumes and database exports, preserve encryption keys, and test a restore before relying on this instance. Review upstream migrations before upgrades. Single-volume services use one replica; no multi-region or high-availability guarantee is made. A gateway health response only proves the gateway is alive.

## Sources

- [Upstream project](https://github.com/agentscope-ai/agentscope)
- [Reviewed source snapshot](https://github.com/agentscope-ai/agentscope/tree/7e614306296233e502b9278f53649acad988aa9f)
- Image digest pins: `images.round4.lock.json` in the template source repository. Source snapshots are research references; image digests do not prove the image was built from that same commit.
- Base-image pins do not lock every package installed by apt/apk/pip. See the verification scope above before relying on this deployment.
