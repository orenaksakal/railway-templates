# Xberg / Kreuzberg Document API

CPU document extraction API from Xberg, formerly Kreuzberg, behind authenticated HTTPS.

**Deployment template.** Deployment incurs Railway charges. Supply your own required model, search and external-service credentials; no example provider credentials are included.

## Live verification — 2026-09-08

Public gateway rejected anonymous requests. Authenticated OpenAPI and real PDF extraction passed. MCP transport, optional formats and sustained load were not tested.

## Setup

Open the xberg service domain and authenticate with ACCESS_USER and ACCESS_PASSWORD. Send extraction requests according to the pinned upstream REST API documentation. The extractor stays private.

### Deployment Dependencies

| Service | Source | Persistent volume | Public HTTP |
|---|---|---|---|
| extractor | ghcr.io/xberg-io/xberg:1.1.2 (digest pinned) | None | Private only |
| xberg | repository adapter: shared/round4-gateway/Dockerfile | None | 8080 |

## Required inputs

No external secrets are required for initial configuration. Follow the setup instructions for application-level onboarding.

Generated credentials: `xberg.ACCESS_PASSWORD`. Keep them private and preserve relevant encryption keys with backups. Every editor variable includes a description.

## Scope and limitations

CPU core image, no GPU or optional full-image extras. Gateway limits request bodies to 32 MiB and upstream idle time to 600 seconds. No durable file archive is configured. API response schemas and MCP transport must be validated before advertising client compatibility.

## Recommended acceptance checks

Image startup; unauthorized rejection; representative PDF and Office extraction; Unicode output; MCP handshake if advertised; upload and timeout behavior.

## Operations

Keep database and internal service endpoints private. Railway provides HTTPS for the explicitly exposed HTTP services. Back up the listed persistent volumes and database exports, preserve encryption keys, and test a restore before relying on this instance. Review upstream migrations before upgrades. Single-volume services use one replica; no multi-region or high-availability guarantee is made. A gateway health response only proves the gateway is alive.

## Sources

- [Upstream project](https://github.com/xberg-io/xberg)
- [Reviewed source snapshot](https://github.com/xberg-io/xberg/tree/e19378401a562ae88e81a60454e05d4f838ac8ee)
- Image digest pins: `images.round4.lock.json` in the template source repository. Source snapshots are research references; image digests do not prove the image was built from that same commit.
- Base-image pins do not lock every package installed by apt/apk/pip. See the verification scope above before relying on this deployment.
