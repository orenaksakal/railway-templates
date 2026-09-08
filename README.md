# Railway self-hosting templates

Five maintained deployment definitions: **Formbricks, Firecrawl, AFFiNE, OpenProject, and ToolJet**. Each definition uses pinned images, generated per-deployment secrets, private dependencies, persistent data, and a product-specific startup adapter.

| Template | Services | Included |
| --- | --- | --- |
| [Formbricks](templates/formbricks/README.md) | 5 | Survey app, Hub, Cube analytics, PostgreSQL, Valkey |
| [Firecrawl](templates/firecrawl/README.md) | 6 | API-key gateway, API/workers, browser, PostgreSQL queue, Redis, RabbitMQ |
| [AFFiNE](templates/affine/README.md) | 3 | Workspace server, PostgreSQL, Valkey |
| [OpenProject](templates/openproject/README.md) | 2 | Supervised application/worker/collaboration stack, external PostgreSQL |
| [ToolJet](templates/tooljet/README.md) | 4 | Community Edition server/worker, PostgreSQL, PostgREST, Valkey |

## Status

These are release candidates. Local checks are documented in [VALIDATION.md](VALIDATION.md). Marketplace publication and fresh Railway deployment verification are separate steps; passing local checks does not establish Railway production readiness.

## Files and reproduction

`templates/<name>/template.json` uses Railway's serialized template configuration shape. It is a complete multi-service definition, **not** a per-service `railway.json`. `scripts/catalog.py` is its source of truth. Container recipes use the repository root as their build context.

```sh
python3 scripts/catalog.py
python3 scripts/validate.py
node --test tests/gateway.test.mjs

python3 scripts/prepare-local.py formbricks --port 18081
docker compose -f .local/formbricks/compose.json up -d --build
```

Local configuration and generated secrets stay under ignored `.local/`; do not commit or publish that directory. Only the application port is bound, on `127.0.0.1`. The local helper translates Railway service references to Docker DNS names. It does not prove Railway networking behavior.

Use separate local ports when testing more than one template. To stop a test while retaining its database and files:

```sh
docker compose -f .local/formbricks/compose.json stop
```

## Railway drafts

The [draft creation script](scripts/create-drafts.py) configures separate private source projects and creates unpublished templates in your chosen workspace. It does not invoke deployment or publication commands. It creates services, volume attachments, and generated domain reservations; review workspace billing rules before running it. Receipt files allow a partially completed run to resume.

```sh
python3 scripts/create-drafts.py --workspace YOUR_WORKSPACE_ID
```

The Dockerfile sources expect `orenaksakal/railway-templates`, branch `main`. A fork should change `REPO` in `scripts/catalog.py` and regenerate before creating drafts. Review the generated draft's variables and volume mounts in Railway before publishing. New credentials must be generated for every deployment, never copied from a test instance.

See [PUBLISHING.md](PUBLISHING.md) for the final deployment and marketplace checks.

## Updates and recovery

Image tags resolve to digests recorded in `images.lock.json` or directly in the container recipes. Update deliberately, test with a restored copy of customer data, and back up both databases and application volumes before an upgrade. An old application image may not understand a newly migrated schema; rollback requires a compatible database snapshot as well as an image.

`scripts/lock-images.py` pins currently unpinned image references. To upgrade an existing pin, change the relevant reference deliberately and review its upstream release notes. The script does not silently advance already-pinned images.

Only one replica is supported for services using local files. Do not add replicas to a volume-backed app and expect shared storage. Optional SMTP, external model APIs, custom domains, and external storage require the operator's own configuration.

## Licensing

Our deployment adapters and tooling are MIT-licensed. Upstream applications retain their own licenses and edition restrictions. Vendored Formbricks Cube configuration is covered by the license in `templates/formbricks/cube/LICENSE`; it is not relicensed under MIT. These templates do not unlock paid upstream features or imply upstream endorsement.
