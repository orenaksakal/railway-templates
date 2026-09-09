# Coze Studio

Agent and workflow studio with SQL, vector search and object storage.

**Deployment template.** Deployment incurs Railway charges. Supply your own required model, search and external-service credentials; no example provider credentials are included.

## Live verification — 2026-09-08

All eleven services built and started after runtime fixes. etcd committed a health probe. Elasticsearch smartcn/index initialization, Milvus recovery, backend HTTP startup, and gateway authentication passed. Model inference, workflows, OAuth, full schema parity, restore and signed-file behavior were not tested. The documented operator setup remains required.

## Setup

Enter the required model ID, display name and API key; confirm the embedding endpoint/model/dimensions. After a test deployment, review the bundled /operator/opencoze_latest_schema.hcl against MySQL and explicitly apply the required schema delta using a reviewed Atlas CLI. No startup script downloads Atlas or automatically approves schema changes. Review and run the bundled Elasticsearch setup script with --es-address http://127.0.0.1:9200 --docker-host false --index-dir /operator/es_index_schema. Only then proceed to account onboarding through the authenticated coze-studio gateway.

### Deployment Dependencies

| Service | Source | Persistent volume | Public HTTP |
|---|---|---|---|
| mysql | repository adapter: templates/coze-studio/MySQL.Dockerfile | /var/lib/mysql | Private only |
| redis | redis:7.4 (digest pinned) | /data | Private only |
| elasticsearch | repository adapter: templates/coze-studio/Elasticsearch.Dockerfile | /bitnami/elasticsearch/data | Private only |
| storage | repository adapter: templates/coze-studio/Storage.Dockerfile | /data | Private only |
| etcd | repository adapter: templates/coze-studio/Etcd.Dockerfile | /bitnami/etcd | Private only |
| milvus | milvusdb/milvus:v2.5.10 (digest pinned) | /var/lib/milvus | Private only |
| nsqlookupd | nsqio/nsq:v1.2.1 (digest pinned) | None | Private only |
| nsqd | nsqio/nsq:v1.2.1 (digest pinned) | /data | Private only |
| backend | repository adapter: templates/coze-studio/Backend.Dockerfile | None | Private only |
| web | repository adapter: templates/coze-studio/Web.Dockerfile | None | Private only |
| coze-studio | repository adapter: shared/round4-gateway/Dockerfile | None | 8080 |

## Required inputs

`backend.OPENAI_EMBEDDING_API_KEY`, `backend.MODEL_ID_0`, `backend.MODEL_NAME_0`, `backend.MODEL_API_KEY_0`

Generated credentials: `mysql.MYSQL_ROOT_PASSWORD`, `mysql.MYSQL_PASSWORD`, `redis.REDIS_PASSWORD`, `storage.MINIO_ROOT_USER`, `storage.MINIO_ROOT_PASSWORD`, `backend.PLUGIN_AES_AUTH_SECRET`, `backend.PLUGIN_AES_STATE_SECRET`, `backend.PLUGIN_AES_OAUTH_TOKEN_SECRET`, `coze-studio.ACCESS_PASSWORD`. Keep them private and preserve relevant encryption keys with backups. Every editor variable includes a description.

## Scope and limitations

Eleven services; this is a substantial paid stack once deployed. MySQL contains the upstream initial schema; the upstream HCL delta is an explicit operator prerequisite. Elasticsearch smartcn and index templates are included; index initialization is manual. Elasticsearch, etcd, Milvus and NSQ have no application authentication in this draft and must remain private in a dedicated project. Coze storage URL rewriting, OAuth, code nodes and model integrations are unverified. No email or external plugin credentials are supplied.

## Recommended acceptance checks

All image builds; MySQL schema review/apply; Elasticsearch index setup; private IPv4/IPv6 connectivity; account creation; model chat; workflow run; knowledge ingestion; file signatures and downloads; NSQ delivery; volume permissions; backup and restore. Confirm legacy Bitnami images are supportable before publication.

## Operations

Keep database and internal service endpoints private. Railway provides HTTPS for the explicitly exposed HTTP services. Back up the listed persistent volumes and database exports, preserve encryption keys, and test a restore before relying on this instance. Review upstream migrations before upgrades. Single-volume services use one replica; no multi-region or high-availability guarantee is made. A gateway health response only proves the gateway is alive.

## Sources

- [Upstream project](https://github.com/coze-dev/coze-studio)
- [Reviewed source snapshot](https://github.com/coze-dev/coze-studio/tree/fefb05ff27be1da939612fbf9faf5db62583b8ae)
- Image digest pins: `images.round4.lock.json` in the template source repository. Source snapshots are research references; image digests do not prove the image was built from that same commit.
- Base-image pins do not lock every package installed by apt/apk/pip. See the verification scope above before relying on this deployment.
