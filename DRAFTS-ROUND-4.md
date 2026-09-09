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
| OpenRAG CPU Stack | 6 | backend.OPENAI_API_KEY | All image builds and permissions; OpenSearch bootstrap/JWKS; authentication; Langflow key creation and flow import; document ingestion and chat; Docling model download; encryption recovery; saved connections and flows after restart; backup and restore. |
| Marker PDF to Markdown API | 2 | Application onboarding only | CPU image build; model download; reject missing credentials and oversized requests; adversarial filenames; digital PDF conversion; temporary-file cleanup after failure; concurrent request rejection; memory/timeout measurements; model-license review. |
| Acontext Agent Context Platform | 9 | core.LLM_API_KEY, core.CLOUDFLARE_WORKER_URL | Clean image builds; DB migrations and vector extension; API auth; context/session lifecycle; worker queue processing; S3 upload and signed download; Cloudflare sandbox execution; UI login; private trace access; persistence and restore. |
| OceanBase seekdb | 1 | Application onboarding only | Container boot within resource limits; console password enforcement; private SQL connection; vector/full-text/hybrid query; volume restart; backup and restore; application-user grants. |
