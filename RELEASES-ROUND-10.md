# Fifteen published templates — 100 total

Released September 19, 2026. The Railway workspace now has **100 published templates and zero unpublished drafts**. This batch added 15 listings; the preceding 85 workspace inventory records remain unchanged. The repository release records cover 93 of the 100 listings; seven listings predate these recorded batches.

| Template | Services | Public listing |
| --- | ---: | --- |
| [Airstation Private Radio](templates/round10/airstation/README.md) | 2 | [Deploy](https://railway.com/deploy/airstation-private-radio) |
| [Backrest Repository Manager](templates/round10/backrest/README.md) | 2 | [Deploy](https://railway.com/deploy/backrest-repository-manager) |
| [DomainMOD Portfolio Inventory](templates/round10/domainmod/README.md) | 3 | [Deploy](https://railway.com/deploy/domainmod-portfolio-inventory) |
| [farmOS Farm Records](templates/round10/farmos/README.md) | 3 | [Deploy](https://railway.com/deploy/farmos-farm-records) |
| [LibreBooking Resource Scheduler](templates/round10/librebooking/README.md) | 3 | [Deploy](https://railway.com/deploy/librebooking-resource-scheduler) |
| [Mikochi File Browser](templates/round10/mikochi/README.md) | 2 | [Deploy](https://railway.com/deploy/mikochi-file-browser) |
| [Mountebank Private API Mocks](templates/round10/mountebank/README.md) | 2 | [Deploy](https://railway.com/deploy/mountebank-private-api-mocks) |
| [Movary Movie Diary](templates/round10/movary/README.md) | 2 | [Deploy](https://railway.com/deploy/movary-movie-diary) |
| [Pinry Visual Bookmark Boards](templates/round10/pinry/README.md) | 2 | [Deploy](https://railway.com/deploy/pinry-visual-bookmark-boards) |
| [PlantUML Private Diagram Renderer](templates/round10/plantuml/README.md) | 2 | [Deploy](https://railway.com/deploy/plantuml-private-diagram-renderer) |
| [Stoplight Prism OpenAPI Mock Server](templates/round10/prism/README.md) | 2 | [Deploy](https://railway.com/deploy/stoplight-prism-openapi-mock-server) |
| [Raneto Private Knowledge Base](templates/round10/raneto/README.md) | 2 | [Deploy](https://railway.com/deploy/raneto-private-knowledge-base) |
| [Redoc Private API Documentation](templates/round10/redoc/README.md) | 2 | [Deploy](https://railway.com/deploy/redoc-private-api-documentation) |
| [Speedtest Tracker Regional Egress](templates/round10/speedtest-tracker/README.md) | 2 | [Deploy](https://railway.com/deploy/speedtest-tracker-regional-egress) |
| [Swagger Editor Private API Designer](templates/round10/swagger-editor/README.md) | 2 | [Deploy](https://railway.com/deploy/swagger-editor-private-api-designer) |

## Verification

- All 15 are `PUBLISHED`, with exact configuration and metadata readbacks matching the committed sources.
- All 15 public listing pages returned HTTP 200 and contained the expected name. All marketplace icons returned image content successfully.
- The complete workspace inventory contains exactly 100 published IDs, comprising the original 85 plus these 15, with no drafts.
- Static validation passed for 15 definitions / 33 services, image pins, private dependencies, variables, mounts, source paths and required overview sections.
- 46 product/alias marketplace checks support the selections; unrelated results are explicitly excluded. See [selection evidence](SELECTION-ROUND-10.md).
- Nine real Nginx 1.28.0 regression tests passed for gateway access: credential rejection, cookie issuance, native Bearer forwarding, forged-cookie rejection, password rotation, API keys, healthcheck isolation, upstream-auth failure and rejection of partial protection mode.
- Focused isolated bootstrap checks covered preserving Raneto pages, Pinry users/settings, Redoc/Prism specifications, and atomic initialization/restart behavior for DomainMOD, LibreBooking and farmOS.

The round-ten gateway sets a Secure, HttpOnly, host-scoped owner cookie after authenticated success. This allows browser applications to send their native authorization tokens while retaining owner access. The existing published batches keep their existing gateway. Speedtest Tracker uses the publisher's GHCR mirror after Railway rejected the LSCR address; both resolved to the same image digest.

## Scope and reproduction

Sources were pushed to `codex/unique-template-drafts` before publication. Application definitions and adapters were committed in `b7a3560`; the equivalent supported registry reference was committed in `9d00270`. Private API responses and publication receipts are retained in ignored `.local/round10/`.

```sh
python3 scripts/assemble-round10.py
python3 scripts/validate-round10.py
python3 scripts/release-round10.py --verify-only
NGINX_BIN=/absolute/path/to/nginx python3 tests/round10-gateway.test.py
```

Application image builds, fresh Railway deployments, full application workflows, restart/persistence acceptance, backup restoration and measured costs remain **unverified**. No application projects or billable deployments were created. The proxy test and static checks do not certify each application's runtime behavior. Pinry's older upstream release and each product's specific limits are disclosed in its overview.
