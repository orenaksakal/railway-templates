# Additional-template release validation

Release validation and publication were authorized on September 7, 2026. Each template is tested in its own Railway project. Test deployments incur Railway usage; no fixed monthly cost claim is made.

| Template | Current evidence | Marketplace |
| --- | --- | --- |
| DBOS | Linux build; fresh Railway deployment; generated auth key; unauthorized rejection; idempotent event/result; app/database restart; volume-preserving redeploy; pg_dump restored into separate database with completed workflow | [Published](https://railway.com/deploy/dbos-durable-webhooks) |
| SpiceDB | Linux build; fresh Railway migration; authenticated schema/relationship writes; allow/deny checks; app/database restart; volume-preserving redeploy; pg_dump restored into separate database with relationship intact | [Published](https://railway.com/deploy/spicedb-with-postgresql) |
| Immich | Fresh Railway startup after telemetry fix; private ML service healthy; admin signup/login; unauthorized rejection; photo upload, metadata and byte-identical download | Unpublished; persistence/recovery testing continues |
| Frappe CRM | MariaDB entrypoint corrected; initial application build succeeded; latest source build underway | Unpublished |
| Frappe Helpdesk | MariaDB entrypoint corrected; missing build-time socketio_port fixed; latest source build underway | Unpublished |
| Matrix | MAS and databases start; Synapse config ownership corrected; client/gateway checks continue | Unpublished |
| Novu | API, worker, WebSocket, MongoDB, Redis and private storage start; dashboard health-check port corrected | Unpublished |
| Appwrite | Dependency services start; core process/connection failures under investigation | Unpublished |
| AppFlowy | Dependency startup and pinned frontend compatibility testing underway | Unpublished |
| RAGFlow | Search/database/storage startup; large image build underway on Railway | Unpublished |

Database restore checks above use separate databases on isolated test PostgreSQL services. They are not full separate-project disaster-recovery drills. Backups are not automatically scheduled. Load testing and high availability are outside the verified scope. Test credentials, deployment receipts, and logs stay in ignored `.local/round3/`.
