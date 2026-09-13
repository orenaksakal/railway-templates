# Fifteen new Railway template drafts

Prepared September 13, 2026. This batch adds Plunk, Bugsink, Notifuse, Lago, DocuSeal, Frappe Learning, DB-GPT, Frappe Insights, Frappe Builder, Unla, MCPJungle, Perses, TimeTagger, Vespa and Agenta. The existing 25 published templates are unchanged.

The fifteen definitions contain 53 services with image digest pins, generated secrets, operator inputs, private dependencies and explicit persistent volumes. Every template has a marketplace overview and product-specific acceptance workflow. Sources build from `codex/fifteen-template-drafts`, using the repository root as Docker context.

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
