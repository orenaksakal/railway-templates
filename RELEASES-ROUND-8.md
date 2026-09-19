# Round 8 published templates

All twenty replacement templates were published at the owner's request on September 19, 2026. Each listing was read back as `PUBLISHED`, with its complete service configuration and every supplied metadata field, including the overview, matching the local source. Each public listing returned HTTP 200 and contained its product name. Together with the prior 40 published listings, the recorded portfolio contains 60 templates.

| Template | Services | Public listing |
| --- | ---: | --- |
| Jelu Reading Tracker | 2 | [Deploy](https://railway.com/deploy/jelu-reading-tracker) |
| Grimoire Bookmark Workspace | 2 | [Deploy](https://railway.com/deploy/grimoire-bookmark-workspace) |
| LinkAce Bookmark Archive | 2 | [Deploy](https://railway.com/deploy/linkace-bookmark-archive) |
| SolidInvoice Billing Workspace | 3 | [Deploy](https://railway.com/deploy/solidinvoice-billing-workspace) |
| Titra Project Time Tracking | 3 | [Deploy](https://railway.com/deploy/titra-project-time-tracking) |
| Fava Beancount Ledger | 2 | [Deploy](https://railway.com/deploy/fava-beancount-ledger) |
| Yaade API Workspace | 2 | [Deploy](https://railway.com/deploy/yaade-api-workspace) |
| WireMock Private API Stubs | 2 | [Deploy](https://railway.com/deploy/wiremock-private-api-stubs) |
| MockServer Private Expectations | 2 | [Deploy](https://railway.com/deploy/mockserver-private-expectations) |
| SQLPage Private App Starter | 2 | [Deploy](https://railway.com/deploy/sqlpage-private-app-starter) |
| Lingarr Subtitle Translation | 2 | [Deploy](https://railway.com/deploy/lingarr-subtitle-translation) |
| DumbPad Private Notepad | 2 | [Deploy](https://railway.com/deploy/dumbpad-private-notepad) |
| DumbAssets Private Inventory | 2 | [Deploy](https://railway.com/deploy/dumbassets-private-inventory) |
| DumbBudget Personal Finance | 2 | [Deploy](https://railway.com/deploy/dumbbudget-personal-finance) |
| DumbKan Private Kanban | 2 | [Deploy](https://railway.com/deploy/dumbkan-private-kanban) |
| DumbDrop Private File Inbox | 2 | [Deploy](https://railway.com/deploy/dumbdrop-private-file-inbox) |
| Maintainerr Media Rules | 2 | [Deploy](https://railway.com/deploy/maintainerr-media-rules) |
| OliveTin Private Action Panel | 2 | [Deploy](https://railway.com/deploy/olivetin-private-action-panel) |
| GO Feature Flag Relay | 2 | [Deploy](https://railway.com/deploy/go-feature-flag-relay) |
| Flagd OpenFeature Starter | 2 | [Deploy](https://railway.com/deploy/flagd-openfeature-starter) |

## Selection and verified scope

The 56 product/alias searches were rerun immediately before publication. All 20 still qualified through the public marketplace-gap route; the GO Feature Flag results were the previously excluded different products. See [SELECTION-ROUND-8.md](SELECTION-ROUND-8.md) and [eligibility.round8.json](eligibility.round8.json) for the bounded search evidence. No competitor is claimed broken. Superseded round-seven drafts were not published.

Static validation passes for 20 templates / 42 services, including source/image pins, generated-secret references, private dependencies, persistent mounts, Dockerfile paths, and required overview sections. The 13 existing Python tests and 6 existing Node tests pass; those are repository checks, not application acceptance tests for these products. A complete live preflight verified the batch before publication, followed by exact per-listing readback.

No container build, Railway application startup, browser/API product workflow, native-client compatibility, volume recovery or cost measurement was performed. Docker was unavailable locally. Publication created no application projects or running services. The overviews disclose this scope and provide product-specific acceptance checks. Public listing availability does not prove successful deployment.

## Source and maintenance

Adapters build from the pushed `codex/unique-template-drafts` branch of `orenaksakal/railway-templates`; keep that branch available. Release source and overviews are committed through `7b727f1`. No main-branch promotion was performed. Images remain pinned; Fava's direct package version is fixed while transitive Python dependencies resolve at build time.

Private publication, full-readback, refreshed-search and public-page receipts remain in `.local/round8/`. Recheck the published batch with:

```sh
python3 scripts/validate-round8.py
python3 scripts/publish-round8.py --verify-only
```

[DRAFTS-ROUND-8.md](DRAFTS-ROUND-8.md) preserves the preparation-stage editor links and setup boundaries. Its original unpublished status describes that historical stage; use this release record for current status. Do not rerun draft creation against these published templates.
