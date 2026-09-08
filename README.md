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
node --test tests/*.test.mjs
python3 -m unittest discover -s tests -p 'test_*.py'

python3 scripts/prepare-local.py formbricks --port 18081
docker compose -f .local/formbricks/compose.json up -d --build
```

Local configuration and generated secrets stay under ignored `.local/`; do not commit or publish that directory. Only the application port is bound, on `127.0.0.1`. The local helper translates Railway service references to Docker DNS names. It does not prove Railway networking behavior.

Use separate local ports when testing more than one template. To stop a test while retaining its database and files:

```sh
docker compose -f .local/formbricks/compose.json stop
```

## Railway marketplace listings

All five listings are published with structured overviews, category, icon, and descriptions for all 184 required variables. Saved configurations and metadata match this release branch exactly. See [the validation record](VALIDATION.md) for tested scope and remaining runtime checks. Publication did not create deployments. The source-project script below is an alternative workflow and can start deployments.

- [Formbricks](https://railway.com/deploy/formbricks)
- [Firecrawl](https://railway.com/deploy/firecrawl-1)
- [AFFiNE](https://railway.com/deploy/affine-2)
- [OpenProject](https://railway.com/deploy/openproject-2)
- [ToolJet](https://railway.com/deploy/tooljet-2)

The [draft creation script](scripts/create-drafts.py) configures separate private source projects and creates unpublished templates in your chosen workspace. It creates services, connects their sources, attaches volumes, and reserves application domains. **Railway can start billable deployments during source connection and volume attachment.** It never publishes templates. Review workspace billing rules before running it. Receipt files allow a partially completed run to resume. Railway generation removes constant variable defaults and build settings; the script fails verification until the editor repair below is completed.

```sh
python3 scripts/create-drafts.py --workspace YOUR_WORKSPACE_ID --stage-only
```

The Dockerfile sources expect `orenaksakal/railway-templates`, branch `codex/railway-template-release`. A fork should change `REPO` in `scripts/catalog.py` and regenerate before creating drafts. Review the generated draft's variables and volume mounts in Railway before publishing. New credentials must be generated for every deployment, never copied from a test instance.

In each draft, open each service's **Variables → Raw Editor → JSON** and restore the exact variable defaults from its local `template.json`. Keep generated-secret expressions symbolic. **Update Variables** stages changes; return to the canvas and click **Apply** to save them. Then verify the persisted result:

```sh
python3 scripts/create-drafts.py --workspace YOUR_WORKSPACE_ID --verify-only
```

The Formbricks bootstrap also has an opt-in integration check using cached images and a temporary in-memory database:

```sh
docker build --pull=false -t railway-templates/formbricks-hub:bootstrap-test -f templates/formbricks/Hub.Dockerfile .
python3 tests/formbricks-bootstrap.py
```

Run it after preparing the local Formbricks images with `prepare-local.py` and Compose. It removes its own test containers and network and exposes no ports.

The verification checks configuration fidelity; it does not establish a successful application deployment. `--stage-only` explicitly allows incomplete generated drafts and must never be used as release evidence.

A direct template-editor Compose import is also being evaluated to avoid source-project deployments. `python3 scripts/export-compose.py` writes symbolic import files under `.local/imports/`. Their local content is checked, but Railway's import behavior has **not** been verified; do not treat those files as a proven substitute for the native catalog.

See [PUBLISHING.md](PUBLISHING.md) for the final deployment and marketplace checks.

## Updates and recovery

Image tags resolve to digests recorded in `images.lock.json` or directly in the container recipes. Update deliberately, test with a restored copy of customer data, and back up both databases and application volumes before an upgrade. An old application image may not understand a newly migrated schema; rollback requires a compatible database snapshot as well as an image.

`scripts/lock-images.py` pins currently unpinned image references. To upgrade an existing pin, change the relevant reference deliberately and review its upstream release notes. The script does not silently advance already-pinned images.

Only one replica is supported for services using local files. Do not add replicas to a volume-backed app and expect shared storage. Optional SMTP, external model APIs, custom domains, and external storage require the operator's own configuration.

## Licensing

Our deployment adapters and tooling are MIT-licensed. Upstream applications retain their own licenses and edition restrictions. Vendored Formbricks Cube configuration is covered by the license in `templates/formbricks/cube/LICENSE`; it is not relicensed under MIT. These templates do not unlock paid upstream features or imply upstream endorsement.
