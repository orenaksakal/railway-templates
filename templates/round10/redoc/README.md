# Deploy and Host Redoc Private API Documentation

Readable OpenAPI documentation with a persistent, replaceable schema.

## About Hosting

Redoc renders a searchable API reference from an OpenAPI document. The private core serves on port 8080. A generated password protects the public gateway. The `/data` volume stores `openapi.json`; the starter document is copied only when that file is absent.

## Why Deploy Redoc Private API Documentation on Railway

Publish internal API documentation to an owner-protected Railway URL with a persistent specification and a pinned Redoc image. Rendering runs in the reader's browser, while the schema file is served from the same protected origin.

## Common Use Cases

- Share a private reference for an internal API.
- Document an API contract while the backend is being developed.
- Keep a browsable reference alongside a versioned OpenAPI source file.

## First use

Open the redoc service URL and authenticate with username `admin` and its `ACCESS_PASSWORD`. The included example describes `GET /hello`. Replace `/data/openapi.json` in the core service with your own valid OpenAPI JSON document using Railway SSH or a controlled deployment workflow. Write a temporary file and rename it into place to avoid partial reads, then refresh the documentation page. The service renders documentation; it does not implement the described API.

Keep the generated owner password private. The gateway supports browser Basic authentication with username `admin` and API access through `X-Template-Key`. It preserves Bearer authorization and limits request bodies to 32 MiB with a 600-second proxy read timeout.

## Storage and backups

`core:/data` contains the OpenAPI JSON document. Back up source documents and any persistent volume before upgrades. Test a restore into a separate instance before relying on the template for important work. Do not scale a volume-backed core beyond one replica.

After gateway authentication, successful page responses set a Secure, HttpOnly owner cookie. This lets browser apps send their native API authorization while retaining gateway access. Rotating `ACCESS_PASSWORD` invalidates existing owner cookies. API clients can continue using `X-Template-Key`.

## Scope and limitations

This template serves a single specification at `/openapi.json`. There is no browser upload screen or API backend. Restrict external `$ref` and logo URLs in your specification if its readers must avoid external requests. Redoc configuration is deliberately fixed in the adapter so the specification loads from the same protected origin.

Application container builds, fresh Railway startup, full browser/API workflows, restart persistence, backup restoration, capacity and costs remain unverified. Checks performed for this template cover source configuration, manifest metadata, template references, and publication inputs. The gateway `/healthz` only confirms the proxy process is available, not application readiness.

## Acceptance checks

Load the starter reference, replace the schema with a small document bearing your own title, and verify the rendered operations and search. Check `/openapi.json` rejects unauthenticated requests, then restart core and confirm your replacement is retained.

## Dependencies for Redoc Private API Documentation

### Deployment Dependencies

A Railway account with capacity for two services, access to the pinned image registry and this repository branch, and persistent volume capacity where listed. No external database or provider account is included or required for the starter workflow.

### Source and maintenance

- [Upstream project](https://github.com/Redocly/redoc)
- [Reviewed source revision](https://github.com/Redocly/redoc/tree/1b2591e87291fbf6fe1ad5dce9326a316a54609f)
- [Deployment adapter](https://github.com/orenaksakal/railway-templates/tree/codex/unique-template-drafts/templates/round10/redoc)
- Image manifest digests and reviewed source references are recorded separately in the repository. Source review is not a runtime test or a verified source-to-image build attestation.
- Repository services build from `orenaksakal/railway-templates`, branch `codex/unique-template-drafts`, with repository-root build context. Keep the branch available.

Upstream software retains its own license and trademarks. This community template does not imply upstream endorsement.
