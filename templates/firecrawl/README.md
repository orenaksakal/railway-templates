# Firecrawl with an authenticated API and persistent queues

Deploy a private Firecrawl API/worker harness behind an API-key gateway, with a browser renderer, PostgreSQL-backed NuQ queue, Redis, and RabbitMQ. Images are pinned by digest; the API image identifies source commit `2343d7b7b93cf4653b80e0c2b8cb681ba2661803`.

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
