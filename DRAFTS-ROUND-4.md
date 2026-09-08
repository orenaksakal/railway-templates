# Round 4 unpublished drafts

Prepared 2026-09-08. These are editor drafts, not release-certified deployments. No application projects, volumes or billable test deployments are created by this workflow.

All ten have concrete service configurations, pinned base images or pinned upstream source, operator inputs and release gates. Static checks do not prove runtime readiness.

| Draft | Services | Required operator inputs | Release gate |
|---|---:|---|---|
| FastGPT Core + RAG | 9 | Application onboarding only | Build and first boot; root login; model-provider configuration; document upload and retrieval; workflow execution; authenticated replica recovery; object downloads; restart and restore. Verify MongoDB 5 lifecycle/support before release. |
| Dolt SQL Server | 1 | Application onboarding only | Authenticated SQL connection; user grants; insert/commit/branch/merge; volume restart; export and restore. Verify external TLS before offering public SQL access. |
| Xberg / Kreuzberg Document API | 2 | Application onboarding only | Image startup; unauthorized rejection; representative PDF and Office extraction; Unicode output; MCP handshake if advertised; upload and timeout behavior. |
| AgentScope Service API | 3 | Application onboarding only | Clean build; authenticated API; provider setup; agent run and streaming; session persistence; workspace restart; restore Redis and files together; verify tool permissions and service resource limits. |
| Coze Studio | 11 | backend.OPENAI_EMBEDDING_API_KEY, backend.MODEL_ID_0, backend.MODEL_NAME_0, backend.MODEL_API_KEY_0 | All image builds; MySQL schema review/apply; Elasticsearch index setup; private IPv4/IPv6 connectivity; account creation; model chat; workflow run; knowledge ingestion; file signatures and downloads; NSQ delivery; volume permissions; backup and restore. Confirm legacy Bitnami images are supportable before publication. |
| BettaFish Research Reports | 3 | app.MODEL_API_KEY, app.MODEL_BASE_URL, app.MODEL_NAME, app.TAVILY_API_KEY, app.ANSPIRE_API_KEY | Image startup; PostgreSQL schema initialization; search provider call; each engine; full report generation and download; engine routing; log retention; persistence and restore. |
| OpenRAG CPU Stack | 6 | backend.OPENAI_API_KEY, backend.OPENRAG_ENCRYPTION_KEY | All image builds and permissions; OpenSearch bootstrap/JWKS; authentication; Langflow key creation and flow import; document ingestion and chat; Docling model download; encryption recovery; saved connections and flows after restart; backup and restore. |
| Marker PDF to Markdown API | 2 | Application onboarding only | CPU image build; model download; reject missing credentials and oversized requests; adversarial filenames; digital PDF conversion; temporary-file cleanup after failure; concurrent request rejection; memory/timeout measurements; model-license review. |
| Acontext Agent Context Platform | 9 | core.LLM_API_KEY, core.CLOUDFLARE_WORKER_URL | Clean image builds; DB migrations and vector extension; API auth; context/session lifecycle; worker queue processing; S3 upload and signed download; Cloudflare sandbox execution; UI login; private trace access; persistence and restore. |
| OceanBase seekdb | 1 | Application onboarding only | Container boot within resource limits; console password enforcement; private SQL connection; vector/full-text/hybrid query; volume restart; backup and restore; application-user grants. |

## Verified editor drafts

All ten configurations and listing metadata matched Railway readback with status `UNPUBLISHED`.

- [FastGPT Core + RAG](https://railway.com/workspace/templates/a396a70f-7b1b-4596-9ec5-a1f6de50098a) — 9 services
- [Dolt SQL Server](https://railway.com/workspace/templates/b7b2fed7-4f80-4e02-926d-bbcb40776791) — 1 services
- [Xberg / Kreuzberg Document API](https://railway.com/workspace/templates/3131a1e4-ce17-426a-b8d8-e129da1424bf) — 2 services
- [AgentScope Service API](https://railway.com/workspace/templates/6dad8c6f-f2c0-4fe2-af77-0ea5dc74b0d5) — 3 services
- [Coze Studio](https://railway.com/workspace/templates/76e90076-7609-46a8-a5be-04f634900476) — 11 services
- [BettaFish Research Reports](https://railway.com/workspace/templates/74f995f7-51eb-49f1-9e3b-877ba1a93d0a) — 3 services
- [OpenRAG CPU Stack](https://railway.com/workspace/templates/b0cefbac-ddc4-4d05-bc90-4c0118a76a4f) — 6 services
- [Marker PDF to Markdown API](https://railway.com/workspace/templates/bcfc6928-4727-41ae-82aa-928a32dfc867) — 2 services
- [Acontext Agent Context Platform](https://railway.com/workspace/templates/b90a159d-8fdb-4170-bcaf-c238d63be939) — 9 services
- [OceanBase seekdb](https://railway.com/workspace/templates/d3493925-4af2-4655-b8ab-584adb5dfb9f) — 1 services

Validation: 47-service static catalog checks and 10 Python tests passed, including Marker upload path isolation, failure cleanup, oversize/type rejection and concurrent-job rejection. No container builds or live application tests have run. No new projects need cleanup.
