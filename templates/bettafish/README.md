# BettaFish Research Reports

Multi-agent public-opinion research and report generation with PostgreSQL and persistent output files.

**Deployment template.** Deployment incurs Railway charges. Supply your own required model, search and external-service credentials; no example provider credentials are included.

## Live verification — 2026-09-08

Container build, PostgreSQL startup, public report UI and gateway authentication passed. Real model/search calls, full report generation, source-data collection and direct Streamlit routing were not tested; deployers supply their own provider credentials and data.

## Setup

Enter MODEL_API_KEY, MODEL_BASE_URL and MODEL_NAME for an OpenAI-compatible provider, plus the selected search provider credentials. The engines reference the shared model inputs. Open the bettafish gateway using ACCESS_USER and ACCESS_PASSWORD. Set up source data before expecting database-backed insight reports.

### Deployment Dependencies

| Service | Source | Persistent volume | Public HTTP |
|---|---|---|---|
| postgres | postgres:15 (digest pinned) | /var/lib/postgresql/data | Private only |
| app | repository adapter: templates/bettafish/Dockerfile | /data | Private only |
| bettafish | repository adapter: shared/round4-gateway/Dockerfile | None | 8080 |

## Required inputs

`app.MODEL_API_KEY`, `app.MODEL_BASE_URL`, `app.MODEL_NAME`, `app.TAVILY_API_KEY`, `app.ANSPIRE_API_KEY`

Generated credentials: `postgres.POSTGRES_PASSWORD`, `bettafish.ACCESS_PASSWORD`. Keep them private and preserve relevant encryption keys with backups. Every editor variable includes a description.

## Scope and limitations

The Flask orchestrator is exposed through authentication; internal engine ports remain private. Upstream frontend/engine routing must be validated in Railway, including any direct Streamlit links. Reports and logs persist under one /data volume using directory links. Social-site collection can need cookies, source-specific setup and available datasets. No assumption of automatic data availability or model/search credits.

## Recommended acceptance checks

Image startup; PostgreSQL schema initialization; search provider call; each engine; full report generation and download; engine routing; log retention; persistence and restore.

## Operations

Keep database and internal service endpoints private. Railway provides HTTPS for the explicitly exposed HTTP services. Back up the listed persistent volumes and database exports, preserve encryption keys, and test a restore before relying on this instance. Review upstream migrations before upgrades. Single-volume services use one replica; no multi-region or high-availability guarantee is made. A gateway health response only proves the gateway is alive.

## Sources

- [Upstream project](https://github.com/666ghj/BettaFish)
- [Reviewed source snapshot](https://github.com/666ghj/BettaFish/tree/c4ca6360489b53c38d3d41d213a67b50d2fcb883)
- Image digest pins: `images.round4.lock.json` in the template source repository. Source snapshots are research references; image digests do not prove the image was built from that same commit.
- Base-image pins do not lock every package installed by apt/apk/pip. See the verification scope above before relying on this deployment.
