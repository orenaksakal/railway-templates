# Validation record

Local verification on 2026-09-07 (America/Edmonton), using pinned images and generated local credentials. These checks are not Railway deployment or production-readiness certification.

| Template | Observed local result |
| --- | --- |
| Formbricks 5.4.2 | Application and Hub migrations completed; Cube started; `/health` returned HTTP 200. Fixed database startup ordering before migrations. |
| Firecrawl | Gateway health HTTP 200; missing credentials HTTP 401; authenticated example.com scrape returned markdown; asynchronous one-page crawl completed with one document. Worker logs also reported successful Playwright scraping. |
| AFFiNE 0.27.4 | Database migrations and signing-key initialization completed; `/info` returned HTTP 200 and the expected self-hosted version. |
| OpenProject 17.8.0 | Database migration and seed completed; fixed connection-string handling and Apache/Puma port collision. `/health_checks/default` returned HTTP 200 with `default: PASSED Application is running`. |
| ToolJet CE 3.20.223-lts | Application/database migrations completed; PostgREST connected; `/api/health` returned HTTP 200; initial administrator setup page rendered. |

`python3 scripts/validate.py` passed for all twenty services. It checks variable references, Dockerfile paths, exposure, persistence, and shell/JavaScript syntax. The two Node gateway tests passed, including missing/wrong credentials, secret stripping, non-API routes, encoded traversal, proxy request bodies, and health access.

Local tests use Docker on an ARM Mac. OpenProject and ToolJet use x86 emulation. Running all five stacks together exceeded the practical capacity of the 8 GiB Docker VM and caused Firecrawl's resource guard to stall workers. Completed stacks were stopped before remaining tests. This is not a measured per-template Railway capacity or price estimate.

## Railway draft verification (2026-09-07)

All five unpublished drafts were read back on 2026-09-07 and their complete `serializedConfig` objects matched the current local `template.json` files exactly, including defaults, symbolic secret generators, repository branches, Dockerfile paths, health paths/timeouts, commands, public ports, and volume mounts. Formbricks now includes the revised bootstrap configuration. The superseded incomplete Formbricks draft is retained.

| Template | Unpublished editor draft |
| --- | --- |
| Formbricks | [Open draft](https://railway.com/workspace/templates/dc692dcf-fbf1-4ceb-ad27-a97b170eaa0c) |
| Firecrawl | [Open draft](https://railway.com/workspace/templates/fc48d0dd-a191-421b-aa4f-7f3e8a6ece3f) |
| AFFiNE | [Open draft](https://railway.com/workspace/templates/80bf1834-b941-4644-a7bd-0c4f85982ad9) |
| OpenProject | [Open draft](https://railway.com/workspace/templates/21db1c72-d65a-4dc9-a918-a4f7292971db) |
| ToolJet | [Open draft](https://railway.com/workspace/templates/5a7af3b8-f4d6-4e86-996f-8fd3ce8c77c1) |

The four new drafts were created directly using the editor's template-only creation and staging/apply operations, without source projects or deployments. Configuration fidelity does not establish runtime readiness. The publication revision adds deployment-variable descriptions and marketplace overviews. Repository-backed services now use `codex/railway-template-release` so publishing the source fixes does not update the stopped source project on `main`. Runtime certification remains outstanding.

The live API rejects `DOCKERFILE` as a builder enum; catalog services now use `RAILPACK` with explicit Dockerfile paths. Railway's template generator drops build settings and constant variable defaults. `RAILWAY_DOCKERFILE_PATH` is included in each repository-backed service's defaults, which must be restored in the editor. The editor's **Update Variables** button only stages changes; the canvas **Apply** button persists them.

Source connection and volume attachment started deployments even without an explicit deploy command. The existing Formbricks source project's database, cache, Hub, and Cube were marked SUCCESS, but the web deployment FAILED: its startup log reports that Hub did not become healthy, and Hub reports that application migrations did not become ready. These service statuses do not prove working application workflows. The circular HTTP bootstrap dependency has been replaced locally with a PostgreSQL completion marker tied to the pinned application version/digest. Four startup regression tests pass, covering migration-before-marker ordering, refusal to publish readiness after migration failure, refusal to serve after marker failure, and the image/version match. Five Python tests pass for draft fidelity, credential-safe CLI errors, and Compose export preservation. The opt-in local integration test also passed all seven checks using cached images and a temporary in-memory PostgreSQL database: Hub waits without application DNS; pinned app migrations succeed; old release markers remain blocked; the exact release marker unlocks real Goose/River migrations and Hub HTTP health; marker publication is idempotent; database failures do not leak credentials; and missing-current-release waits time out. The test caught and corrected `psql` URI handling: the URI must be passed with `--dbname`, not assigned to `PGDATABASE`. All test containers and their network were removed. This patch has not been deployed to Railway. All four remaining source-project deployments were then stopped; project data volumes and drafts were preserved. The retained volumes may still incur storage charges.

Direct Compose import files remain prepared and locally checked; native editor API transfer was used instead, so Compose import behavior remains unverified. No additional billable source projects or deployments were created during draft completion. Marketplace publication has not occurred. A final live read-back confirmed all five services in the retained Formbricks source project have empty active-deployment lists.

## Outstanding release checks

- Fresh Railway deployment: image builds, generated credentials, private DNS, health checks, public HTTPS, and all service dependencies.
- Complete application workflows: Formbricks survey response and analytics; AFFiNE document sync/upload; OpenProject authenticated project/work-package creation; ToolJet persisted query/application.
- Restart and volume-preserving redeploy, then backup and restore into a separate instance for every template.
- Firecrawl restart/queue recovery and dedicated JavaScript-rendering fixture. The basic scrape/crawl does not establish anti-bot or cloud-feature parity.
- SMTP and optional integrations with the operator's own credentials.

All templates remain release candidates until those checks pass. Marketplace publication is a separate step.
