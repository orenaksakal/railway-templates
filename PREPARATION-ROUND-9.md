# Recovered draft preparation

**Published September 19, 2026.** All eighteen qualifying candidates are now published. See [RELEASES-ROUND-9.md](RELEASES-ROUND-9.md) for current status and public links. The preparation-stage record below is historical.

Scope: the 20 non-superseded drafts from the workspace list. Eighteen qualify as public marketplace gaps; two are held as duplicates of the previous publication batch. The separate 20 Superseded drafts are excluded.

All eighteen were updated in place and individually read back as `UNPUBLISHED` on September 19, 2026. Their full service configurations and every supplied metadata field, including each README, match the local files exactly. Adapter sources were pushed in commit `c52b862`.

These are **prepared, unpublished definitions, not runtime-certified releases**. No application projects, deployments, or publication calls are part of this preparation. Fresh build, Railway startup, product workflows and recovery remain release checks.

## Prepared candidates

| Template | Services | Existing Railway draft |
| --- | ---: | --- |
| Typemill Documentation CMS | 2 | [Editor](https://railway.com/workspace/templates/e3907c69-d217-4a97-9332-1eb557d119cf) |
| Errbit | 2 | [Editor](https://railway.com/workspace/templates/d64d4edc-fe68-42d6-b574-b50f573edc12) |
| An Otter Wiki | 2 | [Editor](https://railway.com/workspace/templates/e83ae1fa-60c3-4bbf-a4bb-080df6503890) |
| Maloja Listening Statistics | 1 | [Editor](https://railway.com/workspace/templates/a01820a0-beb3-4422-bde3-77cbaab85b2b) |
| Part-DB | 1 | [Editor](https://railway.com/workspace/templates/e6b19995-3016-4505-a4ac-46bf2b19719f) |
| Gonic Music Server | 2 | [Editor](https://railway.com/workspace/templates/54b26f54-bd62-4101-99e3-2bc9cd6e085f) |
| phpIPAM Address Inventory | 3 | [Editor](https://railway.com/workspace/templates/8c479a32-8770-4dff-914d-2126fba04c1b) |
| Plik File Sharing | 1 | [Editor](https://railway.com/workspace/templates/02c6863a-2945-4a52-af10-a8a543655c7c) |
| Wastebin | 2 | [Editor](https://railway.com/workspace/templates/016c717b-de3c-4eb0-90f8-abd780bee1cc) |
| Jellystat | 2 | [Editor](https://railway.com/workspace/templates/5509c9be-912c-4af2-a7c9-057acf4ae07d) |
| Automad CMS v2 | 2 | [Editor](https://railway.com/workspace/templates/6c184bac-91b5-4822-99b1-d8af23b008f2) |
| CommaFeed | 3 | [Editor](https://railway.com/workspace/templates/b3247cfa-b1eb-4534-af88-95f5ac84f52d) |
| Bar Assistant + Salt Rim | 4 | [Editor](https://railway.com/workspace/templates/e41565f6-9417-49f9-b2b8-414d35f4a295) |
| bewCloud Personal Cloud | 3 | [Editor](https://railway.com/workspace/templates/4816b3ab-08a1-44e1-941d-3b66f6225414) |
| Chibisafe | 2 | [Editor](https://railway.com/workspace/templates/1a5a0b47-4419-438d-bb49-0175d3ff9980) |
| Gramps Web | 2 | [Editor](https://railway.com/workspace/templates/7abdfcf6-99b5-40d8-8f27-3b22f8015f5a) |
| DBHub Database MCP | 2 | [Editor](https://railway.com/workspace/templates/32233aaa-8ce5-4a18-bfea-49782b19fb7c) |
| Bludit CMS | 2 | [Editor](https://railway.com/workspace/templates/19742478-beef-4a64-a625-ca91f48d2163) |

## Duplicate holds

- **LinkAce**: [existing draft](https://railway.com/workspace/templates/a245d475-f109-470a-850a-d66598e452c2) overlaps [LinkAce Bookmark Archive](https://railway.com/deploy/linkace-bookmark-archive). Its MariaDB topology differs, but that alone does not meet the requested marketplace-gap or verified-public-defect criterion. No defect in the published alternative was demonstrated.
- **DumbDrop**: [existing draft](https://railway.com/workspace/templates/3c077ab7-8985-4266-9e2b-2241e6a64ebf) overlaps [DumbDrop Private File Inbox](https://railway.com/deploy/dumbdrop-private-file-inbox). No defect in that listing was demonstrated.

Both duplicates remain unchanged and unpublished. They are not silently counted as ready.

## Repairs

- Recovered the live draft configurations and existing IDs. Their old `main` references included adapter files absent from both local and current remote main. Restored adapters under `templates/round9/` and referenced the existing `codex/unique-template-drafts` source branch. No new draft IDs are created.
- Reused the repository owner gateway for private applications; documented username, header authentication, upload cap and native-client limits. Bar Assistant now protects initial registration and all public routes with owner access while retaining native API authorization.
- DBHub uses explicit TOML read-only tool configuration instead of the removed READONLY environment option; DSN escaping and control-character rejection are tested. A database-level read-only account remains mandatory.
- Bludit, Typemill, Gonic, Part-DB and Chibisafe consolidate mutable files into one volume per application. Directory initialization preserves existing content, including operator deletions, and fails without publishing partial data.
- Restored Plik's persistent file and metadata configuration, bewCloud migrations and restricted signup configuration, Errbit's first-user-only bootstrap, and Gramps' persistent paths plus supervised task worker.
- Bar Assistant preserves APP_KEY across restarts. Part-DB receives a generated initial administrator password and migration bootstrap. Bludit image debug mode is disabled.
- Replaced stale relative release links and old generator references with current source links, required Railway overview sections, operator inputs, product acceptance workflows and explicit verification limits. Shortened eight descriptions to the 75-character marketplace limit.
- Kept immutable image references. PostgreSQL 17 and Redis 7.4 drafts were refreshed to the current tag digests after their old rolling-tag values diverged. These are draft-only configuration changes; no database was upgraded.

## Selection and evidence

42 meaningful product/alias searches cover the 20 candidates. All search pages were complete. Plikshare was excluded as a different product from Plik; Bytebase listings were excluded as different products from DBHub. The only same-product results were our existing LinkAce and DumbDrop listings. See `eligibility.round9.json`. Searches cannot rule out private, unindexed or differently named listings.

Twelve adapter image references were resolved and inspected without downloading layers. Retained references were checked against Docker Hub tag metadata; registry manifest requests later hit HTTP 429, so a complete fresh manifest walk is not claimed. Sources and image metadata are separate receipts. Bludit's selected Docker image is 3.20.0, while its saved application-documentation reference is 3.22.0. The Gramps API bootstrap was reviewed against API source separately from the frontend release and still needs an image-level compatibility check.

## Validation and remaining gates

- Static validator: 18 templates / 38 services; existing IDs; eligibility; Dockerfile/COPY paths; digest syntax; private dependencies; generated variable references; persistent mounts; required overview sections; shell, Python and Node syntax.
- All 17 Python tests pass, including four new persistence/credential configuration tests. These do not execute the 18 applications.
- Chibisafe proxy configuration passes `caddy validate` using checksum-verified official Caddy 2.11.4. Errbit bootstrap passes Ruby syntax validation. The temporary Caddy binary was removed after the check.
- Docker is unavailable on this host. Container builds, live Railway startup, registration/login, provider connectivity, volume-preserving restart, backup restoration and resource usage remain unverified. Each README provides the concrete product workflow.
- The original live snapshots and full draft readbacks remain private in `.local/round9/`. Use the verifier below for the authoritative saved editor state.

## Maintenance

Source files and overviews are maintained on `codex/unique-template-drafts`; keep the branch available. Do not use the old round-five Dockerfile paths on main. The duplicate holds and Superseded drafts are excluded from the update tool.

```sh
python3 scripts/generate-round9-docs.py
python3 scripts/validate-round9.py
python3 -m unittest discover -s tests -p 'test_*.py'
python3 scripts/update-editor-drafts-round9.py --verify-only
```

Running the editor script without `--verify-only` updates only the existing 18 unpublished drafts, preflights for unexpected concurrent changes, and reads back full configuration and metadata. It never creates projects, deployments or templates, and never publishes.
