# Deploy and Host Mountebank Private API Mocks

Persistent service mocks with protected administration and private ports.

## About Hosting

Mountebank creates programmable test doubles called imposters. The owner gateway exposes only its administrative HTTP API and documentation on core port 2525. Mock ports created by an imposter remain private to the Railway environment. All imposter data is persisted in `/data`.

## Why Deploy Mountebank Private API Mocks on Railway

Keep reusable service mocks near your application services without exposing their administrative API publicly. The adapter gives the upstream non-root user ownership of the mounted data directory, disables filesystem logging, and leaves JavaScript injection disabled.

## Common Use Cases

- Simulate upstream HTTP services for integration tests.
- Exercise error handling with predictable mock status codes and payloads.
- Keep persistent mock scenarios accessible to services in the same Railway environment.

## First use

Open the mountebank service URL and authenticate with username `admin` and its `ACCESS_PASSWORD`. Create an HTTP imposter by sending the following JSON to `POST /imposters` on that public administration URL, with `Content-Type: application/json` and `X-Template-Key: YOUR_ACCESS_PASSWORD`:

```json
{"port":4545,"protocol":"http","stubs":[{"responses":[{"is":{"statusCode":200,"headers":{"Content-Type":"application/json"},"body":{"message":"mock ready"}}}]}]}
```

From another service in the same Railway project and environment, use `http://${{core.RAILWAY_PRIVATE_DOMAIN}}:4545` as the mock base URL in a Railway service variable. The reference is resolved by Railway; do not paste the literal expression into a browser. The gateway URL continues to address administration on 2525, not the imposter on 4545.

Keep the generated owner password private. The gateway supports browser Basic authentication with username `admin` and API access through `X-Template-Key`. It preserves Bearer authorization and limits request bodies to 32 MiB with a 600-second proxy read timeout.

## Storage and backups

`core:/data` contains Mountebank imposter state. Keep one core replica. Back up source documents and any persistent volume before upgrades. Test a restore into a separate instance before relying on the template for important work. Do not scale a volume-backed core beyond one replica.

After gateway authentication, successful page responses set a Secure, HttpOnly owner cookie. This lets browser apps send their native API authorization while retaining gateway access. Rotating `ACCESS_PASSWORD` invalidates existing owner cookies. API clients can continue using `X-Template-Key`.

## Scope and limitations

Only the administrative endpoint is publicly routed. HTTP, TCP, or other mock ports require private network access; no public TCP proxy is provisioned. Keep injection disabled. Imposter proxy targets and captured traffic may contain sensitive values; only trusted owners should configure them. Request recording can grow storage, so enable it only for bounded test sessions and clear data when no longer needed.

Application container builds, fresh Railway startup, full browser/API workflows, restart persistence, backup restoration, capacity and costs remain unverified. Checks performed for this template cover source configuration, manifest metadata, template references, and publication inputs. The gateway `/healthz` only confirms the proxy process is available, not application readiness.

## Acceptance checks

Create the example imposter through the authenticated administrative API, request it from another Railway service over the private network, and confirm the expected JSON. Restart core and verify the imposter remains available. Delete that test imposter and confirm it stays deleted after another restart.

## Dependencies for Mountebank Private API Mocks

### Deployment Dependencies

A Railway account with capacity for two services, access to the pinned image registry and this repository branch, and persistent volume capacity where listed. No external database or provider account is included or required for the starter workflow.

### Source and maintenance

- [Upstream project](https://github.com/bbyars/mountebank)
- [Reviewed source revision](https://github.com/bbyars/mountebank/tree/f1d84839d957b5788473d4a928251f6fdaf68210)
- [Deployment adapter](https://github.com/orenaksakal/railway-templates/tree/codex/unique-template-drafts/templates/round10/mountebank)
- Image manifest digests and reviewed source references are recorded separately in the repository. Source review is not a runtime test or a verified source-to-image build attestation.
- Repository services build from `orenaksakal/railway-templates`, branch `codex/unique-template-drafts`, with repository-root build context. Keep the branch available.

Upstream software retains its own license and trademarks. This community template does not imply upstream endorsement.
