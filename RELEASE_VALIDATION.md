# Additional-template release validation

Release validation and publication were authorized September 7, 2026. Testing used isolated billable Railway projects. The original five listings were not changed.

| Template | Verified evidence | Marketplace |
| --- | --- | --- |
| DBOS Durable Webhooks | Fresh build/startup; auth rejection; idempotent durable workflow; restart/redeploy; separate-database restore | [Published](https://railway.com/deploy/dbos-durable-webhooks) |
| SpiceDB with PostgreSQL | Fresh migration/startup; schema and relationships; allow/deny; restart/redeploy; separate-database restore | [Published](https://railway.com/deploy/spicedb-with-postgresql) |
| Immich with Machine Learning | Signup/login; photo upload/download; thumbnail; CPU embedding and semantic search; restart/redeploy; database and media restore | [Published](https://railway.com/deploy/immich-with-machine-learning) |
| Frappe CRM | Fresh app build/site install; login; lead create/read/update; private attachment; worker; restart/redeploy; database/files restore | [Published](https://railway.com/deploy/frappe-crm) |
| Frappe Helpdesk | Fresh app build/site install; login; ticket create/read/update; private attachment; worker; restart/redeploy; database/files restore | [Published](https://railway.com/deploy/frappe-helpdesk) |
| Matrix Synapse with MAS | MAS password login; auth/admin rejection; private room/message/media; restart/redeploy; both databases and key/media files restored | [Published](https://railway.com/deploy/matrix-synapse-with-mas) |
| Novu Community Edition | Signup/login; org/environment; workflow/subscriber; rendered worker-delivered in-app notification; restart/redeploy; MongoDB namespace restore | [Published](https://railway.com/deploy/novu-community-edition) |
| Appwrite 2 Core | Signup/login; project/key; async schema; document write/read; private file roundtrip/denial; restart/redeploy; PostgreSQL and storage restore | [Published](https://railway.com/deploy/appwrite-2-core) |
| RAGFlow CPU | Signup/login; configured test embedding provider; upload/parse/semantic retrieval; restart/redeploy; MySQL/object/search-document restore | [Published](https://railway.com/deploy/ragflow-cpu) |
| AppFlowy Cloud | Clean 0.18.3 signup/login; workspace/page create/rename/read; file roundtrip; restart/redeploy; database and four-object restore | [Published](https://railway.com/deploy/appflowy-cloud) |

Read each template README for exact exclusions. These are scoped community integrations, not full upstream feature-parity or high-availability certifications. Database restore checks used separate databases/namespaces on isolated test services; file/object restores used separate directories. RAGFlow search recovery tested a document export/restore, not a complete snapshot recovery. No complete separate-project disaster-recovery drill or load test was performed. Backups are not automatically scheduled.

Appwrite excludes Functions/Sites execution; realtime event delivery and MongoDB application workloads remain unverified. Matrix encrypted two-client messaging and federation remain unverified. External email/SMS providers were not exercised. AppFlowy 0.18.3 reports a one-user/three-guest unlicensed limit. RAGFlow requires an operator-configured model provider; the temporary test embedding service is not included in the template, and generated answers were not tested.

Source fixes, image digests and listing metadata are versioned. Railway readbacks verify published status, metadata, README and service configuration, allowing only explicit null source deletions retained by Railway. Test credentials, bounded logs and deployment receipts remain in ignored `.local/round3/`.
