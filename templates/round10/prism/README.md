# Deploy and Host Stoplight Prism OpenAPI Mock Server

Generate mock API responses from a persistent OpenAPI specification.

## About Hosting

Stoplight Prism serves mock HTTP responses defined by an OpenAPI document. The private core listens on port 4010; the owner gateway provides HTTPS. The `/data` volume holds `openapi.json`, seeded only on first startup. The template uses the published 5.15.10 image because the later source release did not have a corresponding image tag when reviewed.

## Why Deploy Stoplight Prism OpenAPI Mock Server on Railway

Run predictable contract-based API mocks beside your frontend or service tests. The template starts in static-example mode, enables request validation errors, and uses one process. Its bundled example provides `GET /hello` so the endpoint is useful immediately.

## Common Use Cases

- Develop a frontend before the real API is available.
- Check how clients handle contract validation errors.
- Share deterministic response examples with a small development team.

## First use

Read the prism service's `ACCESS_PASSWORD`. Request `/hello` on its public URL with `X-Template-Key: YOUR_ACCESS_PASSWORD`; the bundled contract returns a JSON greeting. Replace `/data/openapi.json` in core with your valid OpenAPI JSON document using Railway SSH or a controlled upload workflow, then restart core so the new contract is loaded predictably. Keep the document in source control as well as on the volume.

Keep the generated owner password private. The gateway supports browser Basic authentication with username `admin` and API access through `X-Template-Key`. It preserves Bearer authorization and limits request bodies to 32 MiB with a 600-second proxy read timeout.

## Storage and backups

`core:/data` contains the OpenAPI specification. No mocked business data is stored. Back up source documents and any persistent volume before upgrades. Test a restore into a separate instance before relying on the template for important work. Do not scale a volume-backed core beyond one replica.

After gateway authentication, successful page responses set a Secure, HttpOnly owner cookie. This lets browser apps send their native API authorization while retaining gateway access. Rotating `ACCESS_PASSWORD` invalidates existing owner cookies. API clients can continue using `X-Template-Key`.

## Scope and limitations

Prism mocks an API; it does not persist application records or implement business logic. The supplied mode uses explicit examples rather than random data generation. Gateway Basic authentication consumes the Authorization header; use `X-Template-Key` for owner access when the API contract also requires Bearer authorization. Native Basic API-auth contracts conflict with this gateway and require a different access setup. Private callers can connect directly to `http://${{core.RAILWAY_PRIVATE_DOMAIN}}:4010` within the same Railway environment.

Application container builds, fresh Railway startup, full browser/API workflows, restart persistence, backup restoration, capacity and costs remain unverified. Checks performed for this template cover source configuration, manifest metadata, template references, and publication inputs. The gateway `/healthz` only confirms the proxy process is available, not application readiness.

## Acceptance checks

Request `/hello` with the owner header and check the JSON example; omit the header and confirm access is denied. Replace the contract with an endpoint having a required parameter, verify success and validation-error responses, then restart core and confirm the replacement document remains intact.

## Dependencies for Stoplight Prism OpenAPI Mock Server

### Deployment Dependencies

A Railway account with capacity for two services, access to the pinned image registry and this repository branch, and persistent volume capacity where listed. No external database or provider account is included or required for the starter workflow.

### Source and maintenance

- [Upstream project](https://github.com/stoplightio/prism)
- [Reviewed source revision](https://github.com/stoplightio/prism/tree/cd599a52d1725f622f464e0c7325de8664e8bc88)
- [Deployment adapter](https://github.com/orenaksakal/railway-templates/tree/codex/unique-template-drafts/templates/round10/prism)
- Image manifest digests and reviewed source references are recorded separately in the repository. Source review is not a runtime test or a verified source-to-image build attestation.
- Repository services build from `orenaksakal/railway-templates`, branch `codex/unique-template-drafts`, with repository-root build context. Keep the branch available.

Upstream software retains its own license and trademarks. This community template does not imply upstream endorsement.
