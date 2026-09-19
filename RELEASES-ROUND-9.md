# Round 9 published templates

All eighteen recovered candidates were published at the owner's request on September 19, 2026. Each listing was read back as `PUBLISHED`, with its complete service configuration and every supplied metadata field, including the overview, matching the local release files. Each public listing returned HTTP 200 and contained its product name. This adds 18 to the prior 60 recorded listings, for 78 published templates in this repository's release records.

| Template | Services | Public listing |
| --- | ---: | --- |
| Typemill Documentation CMS | 2 | [Deploy](https://railway.com/deploy/typemill-documentation-cms) |
| Errbit | 2 | [Deploy](https://railway.com/deploy/errbit) |
| An Otter Wiki | 2 | [Deploy](https://railway.com/deploy/an-otter-wiki) |
| Maloja Listening Statistics | 1 | [Deploy](https://railway.com/deploy/maloja-listening-statistics) |
| Part-DB | 1 | [Deploy](https://railway.com/deploy/part-db) |
| Gonic Music Server | 2 | [Deploy](https://railway.com/deploy/gonic-music-server) |
| phpIPAM Address Inventory | 3 | [Deploy](https://railway.com/deploy/phpipam-address-inventory) |
| Plik File Sharing | 1 | [Deploy](https://railway.com/deploy/plik-file-sharing) |
| Wastebin | 2 | [Deploy](https://railway.com/deploy/wastebin) |
| Jellystat | 2 | [Deploy](https://railway.com/deploy/jellystat) |
| Automad CMS v2 | 2 | [Deploy](https://railway.com/deploy/automad-cms-v2) |
| CommaFeed | 3 | [Deploy](https://railway.com/deploy/commafeed) |
| Bar Assistant + Salt Rim | 4 | [Deploy](https://railway.com/deploy/bar-assistant-salt-rim) |
| bewCloud Personal Cloud | 3 | [Deploy](https://railway.com/deploy/bewcloud-personal-cloud) |
| Chibisafe | 2 | [Deploy](https://railway.com/deploy/chibisafe) |
| Gramps Web | 2 | [Deploy](https://railway.com/deploy/gramps-web) |
| DBHub Database MCP | 2 | [Deploy](https://railway.com/deploy/dbhub-database-mcp) |
| Bludit CMS | 2 | [Deploy](https://railway.com/deploy/bludit-cms) |

## Scope and verification

The batch contains 38 services. Static validation and all 17 Python tests pass. Preparation also included Caddy 2.11.4 configuration validation and Ruby syntax validation. Publication preserved the restored Dockerfile paths, pinned images, generated credential expressions, private dependencies and persistent mounts. The full-batch preflight and per-listing readbacks are retained privately in `.local/round9/`.

Container builds, fresh Railway application startup, product workflows, native-client compatibility, backup restoration and costs remain unverified. Each public overview discloses those limitations and supplies concrete acceptance checks. Publication created no application projects or running services; public listing availability is not proof of a working deployment.

The older LinkAce and DumbDrop drafts remain unpublished duplicate holds. The separate Superseded batch was excluded. Selection research and restored adapter details are recorded in [PREPARATION-ROUND-9.md](PREPARATION-ROUND-9.md).

## Source and maintenance

Repository services build from `orenaksakal/railway-templates`, branch `codex/unique-template-drafts`. Keep that branch available. Adapter preparation was pushed in `c52b862` and `fc0249a`; release overviews and the publication verifier were pushed in `974f9ce`. No main-branch promotion was performed.

Recheck published status and exact configuration/metadata with:

```sh
python3 scripts/validate-round9.py
python3 scripts/publish-round9.py --verify-only
```

The unpublished editor-update tool refuses to modify published listings. Use the publication verifier for this released batch.
