# Twenty qualifying marketplace gaps — replacement batch

Checked September 19, 2026. The selection rule is **no matching public Railway template found after product/alias searches**, or **a concrete, evidenced defect in existing templates that this draft fixes**. The original round-seven selection did not meet that rule and is superseded.

All twenty replacements qualify through the gap route. None relies on a claim that a competitor is broken. There are 56 product/alias checks; every saved search has `hasNextPage=false`. These are bounded public searches, not proof that private or unindexed templates cannot exist.

| Candidate | Name/alias checks | Selection result | Upstream source |
| --- | --- | --- | --- |
| [Jelu Reading Tracker](templates/jelu/README.md) | `Jelu`, `Jelu books`, `bayang` | No matching listing found | [v0.87.3](https://github.com/bayang/jelu/releases/tag/v0.87.3) |
| [Grimoire Bookmark Workspace](templates/grimoire/README.md) | `Grimoire`, `grimoire bookmarks`, `littleimp`, `little imp`, `goniszewski` | No matching listing found | [v1.2.0](https://github.com/goniszewski/grimoire/releases/tag/v1.2.0) |
| [LinkAce Bookmark Archive](templates/linkace/README.md) | `LinkAce`, `Link Ace`, `Kovah` | No matching listing found | [v2.6.1](https://github.com/Kovah/LinkAce/releases/tag/v2.6.1) |
| [SolidInvoice Billing Workspace](templates/solidinvoice/README.md) | `SolidInvoice`, `Solid Invoice` | No matching listing found | [3.0.1](https://github.com/SolidInvoice/SolidInvoice/releases/tag/3.0.1) |
| [Titra Project Time Tracking](templates/titra/README.md) | `Titra`, `Titra time`, `titraio`, `kromit` | No matching listing found | [v1.1.0](https://github.com/titraio/titra/releases/tag/v1.1.0) |
| [Fava Beancount Ledger](templates/fava/README.md) | `Fava`, `Fava Beancount`, `Beancount` | No matching listing found | [main](https://github.com/beancount/fava/tree/7096e25c6dcc48ab0059643b5592197492ddd0dc) |
| [Yaade API Workspace](templates/yaade/README.md) | `Yaade`, `Yaade API`, `EsperoTech` | No matching listing found | [main](https://github.com/EsperoTech/yaade/tree/0b4dea7e9b140e029e29210c7694217b464eab41) |
| [WireMock Private API Stubs](templates/wiremock/README.md) | `WireMock`, `Wire Mock` | No matching listing found | [3.13.2-3](https://github.com/wiremock/wiremock-docker/releases/tag/3.13.2-3) |
| [MockServer Private Expectations](templates/mockserver/README.md) | `MockServer`, `Mock Server` | No matching listing found | [mockserver-8.0.0](https://github.com/mock-server/mockserver-monorepo/releases/tag/mockserver-8.0.0) |
| [SQLPage Private App Starter](templates/sqlpage/README.md) | `SQLPage`, `SQL Page` | No matching listing found | [v0.46.3](https://github.com/sqlpage/SQLPage/releases/tag/v0.46.3) |
| [Lingarr Subtitle Translation](templates/lingarr/README.md) | `Lingarr`, `Lingarr subtitles` | No matching listing found | [1.3.0](https://github.com/lingarr-translate/lingarr/releases/tag/1.3.0) |
| [DumbPad Private Notepad](templates/dumbpad/README.md) | `DumbPad`, `Dumb Pad`, `DumbWare` | No matching listing found | [v1.0.4](https://github.com/DumbWareio/DumbPad/releases/tag/v1.0.4) |
| [DumbAssets Private Inventory](templates/dumbassets/README.md) | `DumbAssets`, `Dumb Assets`, `DumbWare` | No matching listing found | [v1.0.11](https://github.com/DumbWareio/DumbAssets/releases/tag/v1.0.11) |
| [DumbBudget Personal Finance](templates/dumbbudget/README.md) | `DumbBudget`, `Dumb Budget`, `DumbWare` | No matching listing found | [main](https://github.com/DumbWareio/DumbBudget/tree/b9db5cb32d14b7b78675d8be054611d4829253ef) |
| [DumbKan Private Kanban](templates/dumbkan/README.md) | `DumbKan`, `Dumb Kan`, `DumbWare` | No matching listing found | [main](https://github.com/DumbWareio/DumbKan/tree/a1dc943e6b259fc0cccd1456233268ca9f40122a) |
| [DumbDrop Private File Inbox](templates/dumbdrop/README.md) | `DumbDrop`, `Dumb Drop`, `DumbWare` | No matching listing found | [main](https://github.com/DumbWareio/DumbDrop/tree/ff8f813f493e89c7da056e7a3101ce2ef48e3960) |
| [Maintainerr Media Rules](templates/maintainerr/README.md) | `Maintainerr`, `Maintainerr Plex` | No matching listing found | [v3.29.0](https://github.com/Maintainerr/Maintainerr/releases/tag/v3.29.0) |
| [OliveTin Private Action Panel](templates/olivetin/README.md) | `OliveTin`, `Olive Tin` | No matching listing found | [3000.20.0](https://github.com/OliveTin/OliveTin/releases/tag/3000.20.0) |
| [GO Feature Flag Relay](templates/go-feature-flag/README.md) | `GO Feature Flag`, `gofeatureflag`, `go-feature-flag`, `thomaspoignant` | No matching listing found | [v1.55.3](https://github.com/thomaspoignant/go-feature-flag/releases/tag/v1.55.3) |
| [Flagd OpenFeature Starter](templates/flagd/README.md) | `Flagd`, `OpenFeature flagd` | No matching listing found | [flagd/v0.16.3](https://github.com/open-feature/flagd/releases/tag/flagd/v0.16.3) |

## False positives and exclusions

The broad GO Feature Flag search returns Flagr (`BZOvXb`) and Flipt (`flipt-v2-envoy-grpc-web`). Their retrieved definitions use `ghcr.io/openflagr/flagr` and `flipt/flipt:v2.11.0`, respectively: separate upstream products. Exact `gofeatureflag` and publisher `thomaspoignant` searches return no results. The two unrelated matches and their rationale are recorded in `eligibility.round8.json`.

Grimoire is a v1.2 rewrite; its `littleimp` compatibility name was searched as well. Titra's current `titraio` name and older `kromit` publisher were both checked. The five DumbWare candidates are separate upstream repositories and applications (notes, asset records, budgets, Kanban, file inbox), not five configurations of the same app; their shared publisher search also returned no results.

Projects requiring host discovery, Docker sockets, desktop-only deployment, privileged networking or uncertain packaging were not used to fill the count. Request Baskets was not selected because its old release and forwarding/security history deserve more review. Frappe Drive and several complex document, network-management and email stacks were investigated but not selected. Existing listings for mainstream alternatives were not assumed broken merely because they were old or unpopular.

## Implementation and evidence boundary

The selected batch contains 42 services. All application endpoints start behind generated owner access; dependencies stay private. Application images and adapter bases are digest-pinned. Configuration/source references and exact commits are recorded in `sources.round8.lock.json`. Grimoire builds from a checksum-verified source archive. Fava pins its package version, but its transitive Python dependency resolution still happens at build time.

The reusable adapters seed only missing files and leave existing journals, SQL pages and expectations intact. Startup scripts explicitly handle selected writable volumes. A source review is not runtime proof; fresh startup, permission handling, application workflows, native clients, restart/redeploy and restoration remain acceptance gates in the per-product READMEs.

No application projects or billable deployments were created, and no templates were published. Raw search/configuration receipts are preserved in ignored `.local/research-round8/`. The reviewable eligibility summaries are in `eligibility.round8.json`. See [DRAFTS-ROUND-8.md](DRAFTS-ROUND-8.md) for the saved draft index and readback status.
