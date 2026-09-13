# Round 6 published templates

All fifteen templates were published at the owner's request on September 13, 2026. Each listing was read back as `PUBLISHED`, with its complete service configuration and supplied marketplace metadata matching the local source. The existing 25 listings were not changed; the portfolio now contains 40 published templates.

| Template | Services | Public listing |
| --- | ---: | --- |
| Plunk Email Platform | 7 | [Deploy](https://railway.com/deploy/plunk-email-platform) |
| Bugsink Error Tracking | 2 | [Deploy](https://railway.com/deploy/bugsink-error-trac-1) |
| Notifuse Email Marketing | 3 | [Deploy](https://railway.com/deploy/notifuse-email-marketing) |
| Lago Usage Billing | 5 | [Deploy](https://railway.com/deploy/lago-usage-billing) |
| DocuSeal Document Signing | 2 | [Deploy](https://railway.com/deploy/docuseal-document--1) |
| Frappe Learning | 3 | [Deploy](https://railway.com/deploy/frappe-learning) |
| DB-GPT Data Assistant | 2 | [Deploy](https://railway.com/deploy/db-gpt-data-assistant) |
| Frappe Insights | 3 | [Deploy](https://railway.com/deploy/frappe-insights) |
| Frappe Builder | 3 | [Deploy](https://railway.com/deploy/frappe-builder) |
| Unla MCP Gateway | 2 | [Deploy](https://railway.com/deploy/unla-mcp-gateway) |
| MCPJungle Enterprise Mode | 3 | [Deploy](https://railway.com/deploy/mcpjungle-enterprise-mode) |
| Perses Dashboards | 2 | [Deploy](https://railway.com/deploy/perses-dashboards) |
| TimeTagger | 1 | [Deploy](https://railway.com/deploy/timetagger) |
| Vespa Search Starter | 2 | [Deploy](https://railway.com/deploy/vespa-search-starter) |
| Agenta LLM Engineering | 13 | [Deploy](https://railway.com/deploy/agenta-llm-engineering) |

## Verified scope

The 53-service batch passes static catalog validation. Publication preserved image pins, generated-secret expressions, private dependencies, volumes and source branch references. Each public overview explicitly states that container builds and Railway application workflows have not been validated. Publication created no application projects or running services.

Container builds, proxy runtime behavior, fresh deployment, external provider integrations, persistence, backup and restoration remain unverified. These listings are not a production-readiness certification or a revenue guarantee. See each product README for its acceptance workflow.

## Source and maintenance

Repository adapters continue to build from `codex/fifteen-template-drafts`; keep that remote branch available. The prior main-branch listings are unchanged. Source files and generated marketplace overviews are maintained in this branch.

Private per-template publication and exact-readback receipts are retained under `.local/round6/`. Recheck published status and full configuration/metadata using:

```sh
python3 scripts/publish-round6.py --verify-only
```

The original preparation record remains in [DRAFTS-ROUND-6.md](DRAFTS-ROUND-6.md). Its draft status and editor-only commands describe the pre-publication stage.
