# Ten additional unpublished Railway drafts

These are reviewable draft configurations, not deploy-ready or production-certified releases. No paid deployments or marketplace publication are authorized for this batch. The original five marketplace listings are kept separate.

The batch contains 48 services across Appwrite 2 Core, AppFlowy Cloud, DBOS Durable Webhooks, SpiceDB with PostgreSQL, Frappe CRM, Frappe Helpdesk, Matrix Synapse with MAS, Immich with Machine Learning, Novu Community Edition, and RAGFlow CPU. Each has a structured overview, icon, category, variable descriptions, generated secrets, source pins, networking, and a persistence layout.

## Readiness and remaining gates

| Draft | Evidence completed | Remaining release gate |
| --- | --- | --- |
| DBOS | Real PostgreSQL test: authentication, idempotency, forced process termination, recovered workflow result | Railway deployment and database restore |
| SpiceDB | Pinned image, migration wrapper, private gRPC/public authenticated HTTP configuration | Build, migration, schema/relationship/permission checks, recovery |
| Frappe CRM | Cached upstream image inspected; it contains only Frappe; explicit app-install adapter added | Build CRM, initialize site, lead/deal and attachment workflow, scheduler, recovery |
| Frappe Helpdesk | Helpdesk and pinned Telephony dependency included | Build, compatibility, site creation, ticket/mail/SLA workflow, recovery |
| Immich | Matching v3.1.0 server/ML images; supported vector database and persistent media layout | Build, mobile upload, CPU ML, video processing, restart, recovery |
| Matrix | Current MAS integration and Element runtime configuration paths verified | Builds, domain ownership, account login, encrypted messaging, media, federation, recovery |
| Novu | Current 3.19.0 CE topology, exact encryption-key length, separate public endpoints | Startup, dashboard/provider setup, in-app notification, object delivery, retries, recovery |
| AppFlowy | 0.9.64 backend/worker/admin and authenticated public S3 URLs | Web/GoTrue compatibility is unverified; the matching web tag does not exist. Verify the digest-pinned upstream web image before any deployment claim |
| Appwrite | 2.0.0 core commands, shared-storage constraint, database adapters inspected | Highest-risk draft: build/startup, database compatibility, auth/CRUD/storage/realtime, background tasks. Functions/Sites executor is excluded |
| RAGFlow | CPU topology, private dependencies, mmap-independent Elasticsearch configuration | Large-image build/startup and realistic resource test; parsing, model/provider setup, retrieval/citations, recovery |

Optional Docker-socket executors, GPU services, and TURN/UDP voice infrastructure are not supplied. Each product README states its exact exclusions and operator setup. AppFlowy requires `gotrue.GOTRUE_ADMIN_EMAIL`; Matrix requires a deliberate server-name/domain choice before initializing persistent data. Draft completeness must not be confused with runtime correctness.

## Reproduction

```sh
python3 scripts/catalog_round3.py
python3 scripts/validate-round3.py
python3 scripts/validate.py
python3 -m unittest discover -s tests -p 'test_*.py'
node --test tests/*.test.mjs
```

The new catalog uses `codex/remaining-template-drafts` and `images.round3.lock.json`. It does not regenerate or update the five published templates. `marketplace.round3.json` and each product's README are the listing sources. The editor tooling only creates or updates unpublished templates, then verifies complete configuration and metadata equality; it has no deployment or publication operation.

Local Compose generation supports these drafts without launching them:

```sh
python3 scripts/prepare-local.py novu --port 18200
python3 scripts/prepare-local.py appflowy --port 18300 --input gotrue.GOTRUE_ADMIN_EMAIL=YOUR_EMAIL
```

Multiple public endpoints receive consecutive loopback ports. Required operator values fail closed when absent; no fake account email is inserted. Secrets remain under ignored `.local/`, and generated-secret lengths follow their definitions. Compose generation is not a startup test.

The opt-in DBOS test uses a cached PostgreSQL 17 test image and a temporary tmpfs database, removes its container, and does not create a persistent Docker volume:

```sh
# Prepare .local/dbos-runtime using templates/dbos/package*.json and npm ci.
python3 tests/dbos-recovery.py
```

The ten images have not all been pulled or built. In particular, RAGFlow's large image was not downloaded within the local disk budget. The new Frappe application builds are unverified. All generated Dockerfile and direct-image sources are pinned by immutable digest; these pins establish source identity, not platform compatibility.
