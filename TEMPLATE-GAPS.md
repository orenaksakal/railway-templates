# Ten potential Railway templates with no matching public listing found

Checked September 8, 2026. This replaces the previous shortlist for the user's **no existing templates** requirement. Research only: no projects, deployments, drafts or publications were created.

The exact-name searches for all ten below returned zero results. Common aliases were searched too. Broad alias searches sometimes returned unrelated products; those were inspected by name and description. This establishes **no matching public template found in the checked Railway searches**, not proof that a private, unindexed or differently described template cannot exist.

GitHub stars are accumulated attention, not search volume or growth. Google autocomplete was checked for product-specific recognition. Exact monthly search volume is unavailable. The first eight have stronger recognizable product/developer-interest signals; Acontext and seekdb are smaller bets. None has passed a Railway deployment test in this research pass.

## Shortlist

| Priority | Candidate | GitHub stars | Marketplace finding | Search positioning |
| --- | --- | ---: | --- | --- |
| 1 | [FastGPT](https://github.com/labring/FastGPT) | 29,598 | No matching public listing found | `fastgpt docker` |
| 2 | [Dolt](https://github.com/dolthub/dolt) | 24,393 | No matching public listing found | `dolt database` |
| 3 | [Xberg (formerly Kreuzberg)](https://github.com/xberg-io/xberg) | 9,275 | No matching public listing found | `xberg github` |
| 4 | [AgentScope](https://github.com/agentscope-ai/agentscope) | 31,060 | No matching public listing found | `agentscope 2.0` |
| 5 | [Coze Studio](https://github.com/coze-dev/coze-studio) | 21,560 | No matching public listing found | `coze studio` |
| 6 | [BettaFish](https://github.com/666ghj/BettaFish) | 42,171 | No matching public listing found | `bettafish ai` |
| 7 | [OpenRAG](https://github.com/langflow-ai/openrag) | 4,560 | No matching public listing found | `openrag docker` |
| 8 | [Marker PDF API](https://github.com/datalab-to/marker) | 39,586 | No matching public listing found | `marker pdf to markdown` |
| 9 | [Acontext](https://github.com/memodb-io/Acontext) | 3,687 | No matching public listing found | `acontext` |
| 10 | [seekdb](https://github.com/oceanbase/seekdb) | 2,916 | No matching public listing found | `seekdb docker` |

## Evidence and proposed scope

### 1. FastGPT

Visual AI workflows and knowledge-base Q&A. Strongest combination of recognized brand, recent release and an empty exact-name marketplace search.

**Searches checked:** `FastGPT`, `Fast GPT`, `fastgpt`, `FastGPT knowledge`. [Repeat exact-name search](https://railway.com/deploy?q=FastGPT).

**Interest:** 29,598 stars. Latest repository push observed: 2026-09-08. Recent release: [v4.16.2](https://github.com/labring/FastGPT/releases/tag/v4.16.2) (2026-09-03). Search terms: `fastgpt docker`; `fastgpt vs dify`.

**Before building:** Inspect the complete current Docker stack, model-provider setup and any sandbox requirements; healthy retrieval and workflow execution are the release gates.

[Official project and setup documentation](https://github.com/labring/FastGPT#readme).

### 2. Dolt

Git-style branching/versioning for SQL data. Good match for the existing database-template audience; a persistent authenticated SQL server is a concrete product.

**Searches checked:** `Dolt`, `Dolt SQL`, `dolthub`. [Repeat exact-name search](https://railway.com/deploy?q=Dolt).

**Interest:** 24,393 stars. Latest repository push observed: 2026-09-06. Recent release: [v2.3.2](https://github.com/dolthub/dolt/releases/tag/v2.3.2) (2026-09-02). Search terms: `dolt database`; `dolt git database`.

**Before building:** Verify SQL networking, branch/merge behavior, persistence and restore. Do not expose an unauthenticated database or claim PostgreSQL compatibility: Dolt and DoltgreSQL are different products.

[Official project and setup documentation](https://github.com/dolthub/dolt#readme).

### 3. Xberg (formerly Kreuzberg)

Document extraction REST API and MCP server. Upstream explicitly supports Docker and CPU execution; avoids a mandatory GPU dependency.

**Searches checked:** `Kreuzberg`, `Xberg`. [Repeat exact-name search](https://railway.com/deploy?q=Kreuzberg).

**Interest:** 9,275 stars. Latest repository push observed: 2026-09-08. Recent release: [v1.1.2](https://github.com/xberg-io/xberg/releases/tag/v1.1.2) (2026-09-07). Search terms: `xberg github`; `xberg vs docling`; `xberg ocr`.

**Before building:** Use the current Xberg name with Kreuzberg as an alias. Confirm optional OCR/model features, upload limits and the actual image footprint. Generic Kreuzberg searches mainly concern the Berlin district.

[Official project and setup documentation](https://github.com/xberg-io/xberg#readme).

### 4. AgentScope

An agent-service template with its prebuilt UI and persistent sessions. Current upstream documents a FastAPI serving layer and August channel/skill-hub additions.

**Searches checked:** `AgentScope`, `AgentScope Runtime`, `Agent Scope`. [Repeat exact-name search](https://railway.com/deploy?q=AgentScope).

**Interest:** 31,060 stars. Latest repository push observed: 2026-09-07. Recent release: [v2.0.7.post1](https://github.com/agentscope-ai/agentscope/releases/tag/v2.0.7.post1) (2026-08-28). Search terms: `agentscope 2.0`; `agentscope studio`; `agentscope runtime`.

**Before building:** Package a specific supported service, not just an installed Python library. Docker/local-tool execution capabilities need explicit Railway-compatible scoping.

[Official project and setup documentation](https://github.com/agentscope-ai/agentscope#readme).

### 5. Coze Studio

Visual agent/application builder with recognizable developer interest and official Docker Compose deployment.

**Searches checked:** `Coze Studio`, `Coze`, `Coze Studio self hosted`. [Repeat exact-name search](https://railway.com/deploy?q=Coze%20Studio).

**Interest:** 21,560 stars. Latest repository push observed: 2026-07-29. Recent release: [v0.5.1](https://github.com/coze-dev/coze-studio/releases/tag/v0.5.1) (2026-02-05). Search terms: `coze studio`; `coze studio github`.

**Before building:** The broad Coze search returns coze2openai and Dify, not Coze Studio. Upstream describes a 2-core/4-GB minimum and public-network/code-execution risks; model configuration is required. This is a larger integration.

[Official project and setup documentation](https://github.com/coze-dev/coze-studio#readme).

### 6. BettaFish

Multi-agent public-opinion research and report generation. Large GitHub audience and an existing Docker/PostgreSQL deployment path.

**Searches checked:** `BettaFish`, `Betta Fish`, `微舆`. [Repeat exact-name search](https://railway.com/deploy?q=BettaFish).

**Interest:** 42,171 stars. Latest repository push observed: 2026-09-04. Recent release: [v3.0.0](https://github.com/666ghj/BettaFish/releases/tag/v3.0.0) (2025-12-23). Search terms: `bettafish ai`; `bettafish ai agent`.

**Before building:** Searches must include AI to avoid aquarium traffic. Validate configured data/search providers, API access and generated report storage. Chinese-language adoption does not establish English-language Railway demand.

[Official project and setup documentation](https://github.com/666ghj/BettaFish#readme).

### 7. OpenRAG

Packaged retrieval platform built around Langflow, Docling and OpenSearch, with a built-in HTTP MCP endpoint.

**Searches checked:** `OpenRAG`, `Open RAG`. [Repeat exact-name search](https://railway.com/deploy?q=OpenRAG).

**Interest:** 4,560 stars. Latest repository push observed: 2026-09-08. Recent release: [v0.7.1](https://github.com/langflow-ai/openrag/releases/tag/v0.7.1) (2026-08-31). Search terms: `openrag docker`; `openrag github`; `openrag ibm`.

**Before building:** The broader Open RAG query returned other RAG products, not this project. Model/search memory needs and ingestion/retrieval must be measured. No assumption that empty marketplace means low support effort.

[Official project and setup documentation](https://github.com/langflow-ai/openrag#readme).

### 8. Marker PDF API

Recognizable PDF-to-Markdown/JSON engine with an official FastAPI server command.

**Searches checked:** `Marker`, `Marker PDF`, `datalab`. [Repeat exact-name search](https://railway.com/deploy?q=Marker).

**Interest:** 39,586 stars. Latest repository push observed: 2026-08-31. Recent release: [v2.0.0](https://github.com/datalab-to/marker/releases/tag/v2.0.0) (2026-07-20). Search terms: `marker pdf to markdown`; `marker pdf vs docling`.

**Before building:** Conditional candidate: current Marker uses local inference for OCR and has CPU/GPU paths. CPU performance, model downloads and distinct model-weight commercial terms need validation before a Railway release.

[Official project and setup documentation](https://github.com/datalab-to/marker#readme).

### 9. Acontext

Agent context/skill-memory backend with an official self-hosting path. A smaller emerging candidate rather than a proven high-volume search target.

**Searches checked:** `Acontext`, `Memodb`, `context data platform`. [Repeat exact-name search](https://railway.com/deploy?q=Acontext).

**Interest:** 3,687 stars. Latest repository push observed: 2026-07-14. Recent release: [ui/v0.1.14](https://github.com/memodb-io/Acontext/releases/tag/ui/v0.1.14) (2026-04-08). Search terms: `acontext`.

**Before building:** Canonical repo is memodb-io/Acontext. Last observed push July 14; autocomplete gave little product-specific expansion. Inspect API/persistence separately from optional sandbox functionality.

[Official project and setup documentation](https://github.com/memodb-io/Acontext#readme).

### 10. seekdb

OceanBase-backed AI-search database brand, combining vector/full-text/structured data in a MySQL-compatible server. Official Docker path and August release.

**Searches checked:** `seekdb`, `seek db`, `OceanBase`. [Repeat exact-name search](https://railway.com/deploy?q=seekdb).

**Interest:** 2,916 stars. Latest repository push observed: 2026-09-08. Recent release: [v1.4.0](https://github.com/oceanbase/seekdb/releases/tag/v1.4.0) (2026-08-27). Search terms: `seekdb docker`; `seekdb oceanbase`.

**Before building:** Smaller audience. Validate server memory, vector queries, authentication and volume restoration. A standalone seekdb listing should not claim to deploy the full distributed OceanBase product.

[Official project and setup documentation](https://github.com/oceanbase/seekdb#readme).

## Recommended first three

1. **FastGPT:** largest clear AI-application gap with meaningful branded Docker/search interest.
2. **Dolt:** persistent database workload and straightforward user intent; strong fit with the existing backend catalog.
3. **Xberg:** explicit REST/MCP server and CPU-first deployment, although the recent name change complicates discovery.

AgentScope is the next pick if agent tooling is the preferred theme. Coze Studio and BettaFish have larger audiences but more product-specific integration work. Keep Marker conditional until CPU economics and model licensing are understood.

## Removed rather than misrepresented as gaps

OpenClaw, Hermes, NanoClaw, PicoClaw, OpenFang, LightRAG, Graphiti, Hindsight, CoPaw, DeepTutor, SpacetimeDB and many other popular names already returned matching listings. OpenMemory returned zero for its exact string, but `mem0 openmemory` found relevant Mem0 listings, so it was not retained as a clean gap. Cherry Studio is principally a desktop application. Chonkie and FlowGram are primarily libraries/frameworks without as clear a standalone hosting product for this shortlist. Backrest and Zerobyte depend on access to the data being backed up; a Railway deployment does not automatically give access to a user's NAS or other Railway volumes. Memobase had weaker recent activity and was not selected.

Evidence: ignored `.local/research-gaps/` contains marketplace search responses, GitHub snapshots, official READMEs and autocomplete responses. Availability and counts can change; repeat the name/alias checks immediately before implementation.
