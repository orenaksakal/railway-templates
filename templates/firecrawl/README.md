# Deploy and Host Firecrawl on Railway

Deploy a private Firecrawl API/worker harness behind an API-key gateway, with a browser renderer, PostgreSQL-backed NuQ queue, Redis, and RabbitMQ. Images are pinned by digest; the API image identifies source commit `2343d7b7b93cf4653b80e0c2b8cb681ba2661803`.

## About Hosting Firecrawl

This six-service deployment puts a small API-key gateway in front of Firecrawl, its browser renderer, and the queue infrastructure. Railway exposes only the gateway over HTTPS; the API harness, PostgreSQL, Redis, RabbitMQ, and renderer communicate privately. The API and browser images are pinned by digest, while the gateway is built from the included Dockerfile. Queue data is stored on persistent volumes. A generated operator key authenticates client requests without requiring a separate authentication database. Concurrency starts conservatively at two. After deployment, retrieve the key from the gateway variables and point your SDK or HTTP client at the gateway domain.

## Common Use Cases

- Convert web pages into markdown for retrieval and AI data pipelines.
- Crawl documentation and other permitted websites asynchronously.
- Extract content from browser-rendered pages through a self-hosted API.

## Dependencies for Firecrawl Hosting

- Firecrawl API/worker harness and Playwright browser renderer.
- NuQ PostgreSQL, Redis, and RabbitMQ with persistent volumes.
- A Railway account with capacity for six services, including browser workloads.
- Optional model-provider or proxy credentials for features that require them.

## First use

Read the generated `API_KEY` from the **firecrawl** gateway service variables. Use its public HTTPS domain as your SDK's API URL. Keep the key private.

```sh
curl "$FIRECRAWL_URL/v2/scrape" \
  -H "Authorization: Bearer $FIRECRAWL_API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{"url":"https://example.com","formats":["markdown"]}'
```

Only the gateway is public. It forwards authenticated `/v1/` and `/v2/` requests and denies other application routes. The internal API intentionally has `USE_DB_AUTHENTICATION=false`; the gateway supplies access control. **Do not generate a public domain or TCP proxy for the internal API.** `/healthz` exposes only a readiness status.

## Capacity and features

Initial browser and crawl concurrency is two. Raise it only after measuring memory and queue latency. PostgreSQL, Redis, and RabbitMQ have persistent volumes. Database initialization uses the upstream NuQ image, including its extension/setup requirements. FoundationDB is not enabled.

Basic scraping requires no model-provider key. Model-backed extraction needs a separately configured supported provider. External model and proxy charges are not included in Railway usage. Self-hosting does not reproduce every Firecrawl Cloud service, proxy network, or anti-bot capability. The gateway uses one operator key, not a multi-customer billing or per-user access-control system.

## Operations and validation

Before production, test rejection of missing/wrong keys, a basic scrape, JavaScript rendering, a completed asynchronous crawl, queue processing after restart, and backup/restore. Retain database and queue snapshots and the generated credentials. Rotate the gateway key by updating `API_KEY`; existing clients must receive the new key through your own secure process.

Upstream: [Firecrawl](https://github.com/firecrawl/firecrawl), [pinned deployment configuration](https://github.com/firecrawl/firecrawl/blob/2343d7b7b93cf4653b80e0c2b8cb681ba2661803/docker-compose.yaml). This template is independently maintained.

## Why Deploy Firecrawl on Railway?

Railway keeps the application and its dependencies in one project, with service references, private networking, HTTPS routing, deployment logs, and persistent volumes. This template supplies the service configuration and startup adapters so you can focus on the application setup. Resource usage and volume storage are billed by Railway; third-party services are billed separately. This deployment does not configure automatic backups or high availability.

## Support and Validation

This is an independently maintained community template. Local startup checks and exact Railway template-configuration read-back have passed. Full Railway application workflows and backup/restore certification remain outstanding; test your intended workflow before relying on the deployment. See the [validation record](https://github.com/orenaksakal/railway-templates/blob/codex/railway-template-release/VALIDATION.md) for the tested scope.

For template issues, use the Railway listing’s community thread or [open a repository issue](https://github.com/orenaksakal/railway-templates/issues). Include the service name, image version, and redacted logs; never include passwords, tokens, or connection strings.
