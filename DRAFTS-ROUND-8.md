# Twenty qualifying unpublished drafts

Saved and individually read back on September 19, 2026 in the `orenaksakal` Railway workspace. **All twenty are UNPUBLISHED.** Saved service configurations and every supplied metadata field, including each README, match the local files exactly. No application project or deployment was created.

## Selection rule

A candidate must fill a public marketplace gap, or repair a concrete, evidenced defect in existing templates. **All twenty in this replacement batch use the gap route:** no matching product listing was found across 56 product/alias checks. Private, unindexed or differently named templates may still exist. The two broad GO Feature Flag results were verified as different products, Flagr and Flipt.

See [SELECTION-ROUND-8.md](SELECTION-ROUND-8.md) and [eligibility.round8.json](eligibility.round8.json) for the queries, results, exclusions and evidence boundaries. No competitor is labeled broken without defect evidence.

The earlier round-seven selection was new only to this portfolio and did not meet this criterion. Its twenty saved drafts are labeled **Superseded** in Railway, remain unpublished, and are not counted here. They were retained rather than deleted; their local records remain available.

## Saved drafts

| Product | Services | Railway editor |
| --- | ---: | --- |
| [Jelu Reading Tracker](templates/jelu/README.md) | 2 | [Open draft](https://railway.com/workspace/templates/a2ae2233-66b0-4130-8378-d608cb94ffd6) |
| [Grimoire Bookmark Workspace](templates/grimoire/README.md) | 2 | [Open draft](https://railway.com/workspace/templates/ba3ae7f4-5f5b-4acc-a3e7-7e64dd12b686) |
| [LinkAce Bookmark Archive](templates/linkace/README.md) | 2 | [Open draft](https://railway.com/workspace/templates/940d179f-3385-4153-b737-03f048246447) |
| [SolidInvoice Billing Workspace](templates/solidinvoice/README.md) | 3 | [Open draft](https://railway.com/workspace/templates/3e665f6d-fa75-4acd-a94b-4e61f1aea4fc) |
| [Titra Project Time Tracking](templates/titra/README.md) | 3 | [Open draft](https://railway.com/workspace/templates/1264061e-35a3-49b8-92b0-4239ba151f07) |
| [Fava Beancount Ledger](templates/fava/README.md) | 2 | [Open draft](https://railway.com/workspace/templates/d15cf960-707a-4280-8563-27aafefa34af) |
| [Yaade API Workspace](templates/yaade/README.md) | 2 | [Open draft](https://railway.com/workspace/templates/3b6523f9-0ee3-4385-badf-cf49a974e6d4) |
| [WireMock Private API Stubs](templates/wiremock/README.md) | 2 | [Open draft](https://railway.com/workspace/templates/00b04510-14ef-46c4-8422-231d83f4ed49) |
| [MockServer Private Expectations](templates/mockserver/README.md) | 2 | [Open draft](https://railway.com/workspace/templates/02041b29-83f3-4b49-ad12-37e7ed9dcf06) |
| [SQLPage Private App Starter](templates/sqlpage/README.md) | 2 | [Open draft](https://railway.com/workspace/templates/080125d2-742f-4b89-a3ce-238a00b760ec) |
| [Lingarr Subtitle Translation](templates/lingarr/README.md) | 2 | [Open draft](https://railway.com/workspace/templates/7fd1d3fb-70f7-4779-ae1b-25f073e7fc8a) |
| [DumbPad Private Notepad](templates/dumbpad/README.md) | 2 | [Open draft](https://railway.com/workspace/templates/08cceda4-c3a1-4e0a-aa8b-ace9b162de37) |
| [DumbAssets Private Inventory](templates/dumbassets/README.md) | 2 | [Open draft](https://railway.com/workspace/templates/0426be75-4afc-40c7-b557-1c6667b0cf18) |
| [DumbBudget Personal Finance](templates/dumbbudget/README.md) | 2 | [Open draft](https://railway.com/workspace/templates/619638bd-130a-4c10-8e08-bd324fe440d7) |
| [DumbKan Private Kanban](templates/dumbkan/README.md) | 2 | [Open draft](https://railway.com/workspace/templates/3ba189be-fa85-44b3-9e2f-977986d3b6fa) |
| [DumbDrop Private File Inbox](templates/dumbdrop/README.md) | 2 | [Open draft](https://railway.com/workspace/templates/c8a9a90e-59fc-408b-bb10-ddb6320a843e) |
| [Maintainerr Media Rules](templates/maintainerr/README.md) | 2 | [Open draft](https://railway.com/workspace/templates/19a5b975-2b3b-499f-adb9-f2f2ccc4a39f) |
| [OliveTin Private Action Panel](templates/olivetin/README.md) | 2 | [Open draft](https://railway.com/workspace/templates/3701d282-eb7e-445b-bafe-9c169ad6aa3c) |
| [GO Feature Flag Relay](templates/go-feature-flag/README.md) | 2 | [Open draft](https://railway.com/workspace/templates/3054a136-5d67-4365-9676-067ae96164b3) |
| [Flagd OpenFeature Starter](templates/flagd/README.md) | 2 | [Open draft](https://railway.com/workspace/templates/e308bf77-ad00-4a62-871d-5c4b61c7c9b7) |

## Validation

- 20 products / 42 services pass `python3 scripts/validate-round8.py`: marketplace eligibility records, no overlap with earlier catalogs, deterministic generated configurations, digest pins, source references, private dependencies, symbolic credentials, persistent mounts, metadata and shell/Python syntax.
- All 13 existing Python tests pass. No new application-level runtime test is claimed.
- All twenty live configurations and metadata were compared to the local sources; all were saved as `UNPUBLISHED`. Private receipts and readbacks remain under `.local/round8/`.
- Adapter sources were committed and pushed to `codex/unique-template-drafts`, beginning at commit `1779d1f`. That branch includes the necessary Dockerfiles, starter configuration, docs, catalogs, source/image locks and eligibility evidence. It has not been merged to main.
- Image registry/tag metadata and upstream source files were inspected without downloading container layers. Grimoire's source archive is pinned by commit and SHA-256. Fava pins its direct package version while resolving transitive Python dependencies at build time.

No container build, Railway startup, browser/API product workflow, native-client compatibility, volume recovery, cost measurement or marketplace publication occurred. Each README names the product-specific acceptance checks still needed. A saved draft or proxy healthcheck is not a successful application deployment.

## Important setup boundaries

All application endpoints begin behind an owner gateway. Use username `admin` and the public service's generated `ACCESS_PASSWORD`, or send `X-Template-Key` for API clients. Keep core and databases private. Basic Authorization is stripped by this gateway; native clients or tests requiring that header need an adapted proxy or private access.

SolidInvoice requires its protected installation wizard using the generated database helper variables. Yaade's initial native password must be changed behind the gateway. The five DumbWare applications also have generated ten-digit native PINs. Maintainerr needs an operator-owned media server; begin with review-only rules, not deletion. Lingarr needs a translation provider and reachable subtitle source. GO Feature Flag and flagd are configuration-as-code starters, not visual flag editors. Older upstream releases and runtime dependency concerns are called out individually rather than concealed by a fresh container tag.

## Reproduce and verify

```sh
python3 scripts/generate-round8-adapters.py
python3 scripts/catalog_round8.py
python3 scripts/generate-round8-docs.py
python3 scripts/validate-round8.py
python3 scripts/create-editor-drafts-round8.py --workspace YOUR_WORKSPACE_ID --verify-only
```

Use create mode without `--verify-only` only when creating or updating these unpublished drafts. It uses the authenticated Railway CLI session, records receipts, refuses to edit published templates, and makes no project/deployment/publication calls. Preserve `.local/round8/drafts.json` so a later update resumes the same drafts; missing receipts would create duplicates.

Before release, rerun the marketplace searches, complete each functional and recovery check, and review observed resource usage. A marketplace gap is not evidence of demand or revenue.
