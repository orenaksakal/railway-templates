# Fifteen new Railway template drafts

**Historical preparation record:** all fifteen are now published. See [RELEASES-ROUND-6.md](RELEASES-ROUND-6.md) for verified status and public links.

Prepared September 13, 2026. This batch adds Plunk, Bugsink, Notifuse, Lago, DocuSeal, Frappe Learning, DB-GPT, Frappe Insights, Frappe Builder, Unla, MCPJungle, Perses, TimeTagger, Vespa and Agenta. The existing 25 published templates are unchanged.

The fifteen definitions contain 53 services with image digest pins, generated secrets, operator inputs, private dependencies and explicit persistent volumes. Every template has a marketplace overview and product-specific acceptance workflow. Sources build from `codex/fifteen-template-drafts`, using the repository root as Docker context.

## Saved Railway drafts

All fifteen were created and individually read back as `UNPUBLISHED` on September 13, 2026, in the `orenaksakal` workspace. Each saved configuration and all supplied marketplace metadata fields match the local source exactly. No running projects or services were created.

| Draft | Services | Railway editor |
| --- | ---: | --- |
| [Plunk Email Platform](templates/plunk/README.md) | 7 | [Open draft](https://railway.com/workspace/templates/9b0fd7e6-6e29-484a-97c2-8ef070b8c6f1) |
| [Bugsink Error Tracking](templates/bugsink/README.md) | 2 | [Open draft](https://railway.com/workspace/templates/aee51fee-70da-4085-a5a1-d8f155e92811) |
| [Notifuse Email Marketing](templates/notifuse/README.md) | 3 | [Open draft](https://railway.com/workspace/templates/a0cd96b5-0e1d-4217-82a8-141b0430503c) |
| [Lago Usage Billing](templates/lago/README.md) | 5 | [Open draft](https://railway.com/workspace/templates/a2b27b0a-22cc-41a9-81d8-79388c2c925f) |
| [DocuSeal Document Signing](templates/docuseal/README.md) | 2 | [Open draft](https://railway.com/workspace/templates/b0b0a820-7ae9-42a2-b4cf-77fd5eaaacaf) |
| [Frappe Learning](templates/frappe-learning/README.md) | 3 | [Open draft](https://railway.com/workspace/templates/9735860e-f9ca-4944-aa11-fa6e1b2a2490) |
| [DB-GPT Data Assistant](templates/db-gpt/README.md) | 2 | [Open draft](https://railway.com/workspace/templates/e5939101-abff-4818-a2a9-a07e42c44ff4) |
| [Frappe Insights](templates/frappe-insights/README.md) | 3 | [Open draft](https://railway.com/workspace/templates/4d0aa1d9-4389-448a-8ed6-5191557b3001) |
| [Frappe Builder](templates/frappe-builder/README.md) | 3 | [Open draft](https://railway.com/workspace/templates/9749b3f7-ebdb-44cf-881f-7730f588f1a3) |
| [Unla MCP Gateway](templates/unla/README.md) | 2 | [Open draft](https://railway.com/workspace/templates/1dcc1da0-faa2-4d43-9360-2e7916239390) |
| [MCPJungle Enterprise Mode](templates/mcpjungle/README.md) | 3 | [Open draft](https://railway.com/workspace/templates/7d377f15-4f66-48e8-97b4-955512c2d5dd) |
| [Perses Dashboards](templates/perses/README.md) | 2 | [Open draft](https://railway.com/workspace/templates/772e1d21-1ae4-4e47-849f-b1b1d06539d2) |
| [TimeTagger](templates/timetagger/README.md) | 1 | [Open draft](https://railway.com/workspace/templates/53cf49ee-b905-4d80-b479-d83dac2c506c) |
| [Vespa Search Starter](templates/vespa/README.md) | 2 | [Open draft](https://railway.com/workspace/templates/a6698293-b96c-4d38-9b1b-b517efe2c399) |
| [Agenta LLM Engineering](templates/agenta/README.md) | 13 | [Open draft](https://railway.com/workspace/templates/1b08bc5d-e54d-4db1-984e-fc926026e083) |

## Validation

- `python3 scripts/validate-round6.py`: 15 definitions / 53 services pass generated-config equality, image pins, references, exposure, Docker COPY paths, variable descriptions and script syntax.
- Existing three catalog validators pass for all 25 published templates.
- `python3 -m unittest discover -s tests -p 'test_*.py'`: 13 tests pass, including invalid TimeTagger credentials and the Frappe existing-site migration guard.
- `node --test tests/*.test.mjs`: 6 tests pass. The local-listener test required execution outside the filesystem sandbox.
- No Docker daemon is running locally. No container image builds, nginx runtime tests or Railway application deployments have been performed for this batch.
- Provider workflows, fresh startup, persistent redeploy, database/file backup and restore remain required acceptance checks. The per-template guides identify the exact workflow.

A passing gateway healthcheck is not application readiness. Image metadata is not build proof. These drafts are not production-certified or published marketplace listings, and no revenue is assured.

## Reproduce

```sh
python3 scripts/catalog_round6.py
python3 scripts/generate-round6-docs.py
python3 scripts/validate-round6.py
python3 scripts/create-editor-drafts-round6.py --workspace YOUR_WORKSPACE_ID
python3 scripts/create-editor-drafts-round6.py --workspace YOUR_WORKSPACE_ID --verify-only
```

The editor script creates unpublished templates only, with no application projects or billable deployments. It saves private receipts under `.local/round6/drafts.json`, resumes existing drafts and compares every saved configuration and metadata field. It refuses to modify published templates. Keep the source branch available while these drafts reference it.

## Important deployment inputs

Plunk needs an operator-owned AWS SES account and configured SNS callbacks; Notifuse needs a root email and working SMTP; Lago, Bugsink and DocuSeal need administrator email addresses; DB-GPT needs a model API key; Agenta's runner needs Daytona credentials, and model use needs a model provider. Do not put template-author accounts or keys into the defaults. All other configured initial credentials are generated per deployment.

The Frappe builds still need framework/app compatibility checks. MCPJungle requires protected one-time initialization and secure storage of its returned admin token. Unla, MCPJungle, Agenta and DB-GPT clients need the owner gateway header in addition to native API authentication where applicable. Plunk's uploads bucket is intentionally public for email images. Bugsink and Notifuse have source-available license restrictions; read their individual guides before commercial use.
