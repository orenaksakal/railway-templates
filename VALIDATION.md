# Validation record

Local verification on 2026-09-07 (America/Edmonton), using pinned images and generated local credentials. These checks are not Railway deployment or production-readiness certification.

| Template | Observed local result |
| --- | --- |
| Formbricks 5.4.2 | Application and Hub migrations completed; Cube started; `/health` returned HTTP 200. Fixed database startup ordering before migrations. |
| Firecrawl | Gateway health HTTP 200; missing credentials HTTP 401; authenticated example.com scrape returned markdown; asynchronous one-page crawl completed with one document. Worker logs also reported successful Playwright scraping. |
| AFFiNE 0.27.4 | Database migrations and signing-key initialization completed; `/info` returned HTTP 200 and the expected self-hosted version. |
| OpenProject 17.8.0 | Database migration and seed completed; fixed connection-string handling and Apache/Puma port collision. Final HTTP verification pending. |
| ToolJet CE 3.20.223-lts | Application/database migrations completed; PostgREST connected; `/api/health` returned HTTP 200; initial administrator setup page rendered. |

`python3 scripts/validate.py` passed for all twenty services. It checks variable references, Dockerfile paths, exposure, persistence, and shell/JavaScript syntax. The two Node gateway tests passed, including missing/wrong credentials, secret stripping, non-API routes, encoded traversal, proxy request bodies, and health access.

Local tests use Docker on an ARM Mac. OpenProject and ToolJet use x86 emulation. Running all five stacks together exceeded the practical capacity of the 8 GiB Docker VM and caused Firecrawl's resource guard to stall workers. Completed stacks were stopped before remaining tests. This is not a measured per-template Railway capacity or price estimate.

## Outstanding release checks

- Fresh Railway deployment: image builds, generated credentials, private DNS, health checks, public HTTPS, and all service dependencies.
- Complete application workflows: Formbricks survey response and analytics; AFFiNE document sync/upload; OpenProject authenticated project/work-package creation; ToolJet persisted query/application.
- Restart and volume-preserving redeploy, then backup and restore into a separate instance for every template.
- Firecrawl restart/queue recovery and dedicated JavaScript-rendering fixture. The basic scrape/crawl does not establish anti-bot or cloud-feature parity.
- SMTP and optional integrations with the operator's own credentials.

All templates remain release candidates until those checks pass. Marketplace publication is a separate step.
