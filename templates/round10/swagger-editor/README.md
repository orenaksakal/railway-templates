# Deploy and Host Swagger Editor Private API Designer

Design and validate OpenAPI and AsyncAPI documents in your browser.

## About Hosting

Swagger Editor is a browser editor for OpenAPI and AsyncAPI specifications. The unprivileged upstream image serves its static application on private port 8080; the public gateway requires the generated owner password. Editing happens in the browser. There is no server database or file volume.

## Why Deploy Swagger Editor Private API Designer on Railway

Keep a consistent, pinned editor version at a private HTTPS address for API contract design. This template packages Swagger Editor, which edits specifications; its scope differs from the Swagger UI viewer.

## Common Use Cases

- Draft and validate API contracts before backend implementation.
- Preview OpenAPI and AsyncAPI documentation while editing.
- Review a specification locally in your browser and export it to source control.

## First use

Open the swagger-editor service URL and authenticate with username `admin` and that service's `ACCESS_PASSWORD`. Import or paste a specification, correct validation errors, and export the result. Keep exported files in your own source control; browser storage is not a shared or backed-up workspace.

Keep the generated owner password private. The gateway supports browser Basic authentication with username `admin` and API access through `X-Template-Key`. It preserves Bearer authorization and limits request bodies to 32 MiB with a 600-second proxy read timeout.

## Storage and backups

None; save specification exports outside the browser. Back up source documents and any persistent volume before upgrades. Test a restore into a separate instance before relying on the template for important work. Do not scale a volume-backed core beyond one replica.

After gateway authentication, successful page responses set a Secure, HttpOnly owner cookie. This lets browser apps send their native API authorization while retaining gateway access. Rotating `ACCESS_PASSWORD` invalidates existing owner cookies. API clients can continue using `X-Template-Key`.

## Scope and limitations

Browser-originated URL imports and API requests depend on the target server's HTTPS and CORS policy. Optional generator or external API integrations may send specifications to other services; review their destination before using them with private contracts. Browser data does not transfer between devices, and clearing browser storage may remove unsaved work.

Application container builds, fresh Railway startup, full browser/API workflows, restart persistence, backup restoration, capacity and costs remain unverified. Checks performed for this template cover source configuration, manifest metadata, template references, and publication inputs. The gateway `/healthz` only confirms the proxy process is available, not application readiness.

## Acceptance checks

Open the editor, import a small OpenAPI document, introduce and then fix a validation error, export the document, and reopen the export. Check a private/incognito session is rejected without credentials. A service restart should reload the editor; exported files remain your durable record.

## Dependencies for Swagger Editor Private API Designer

### Deployment Dependencies

A Railway account with capacity for two services, access to the pinned image registry and this repository branch, and persistent volume capacity where listed. No external database or provider account is included or required for the starter workflow.

### Source and maintenance

- [Upstream project](https://github.com/swagger-api/swagger-editor)
- [Reviewed source revision](https://github.com/swagger-api/swagger-editor/tree/19956f731ab7986d1b8497bbbeeee280749a8255)
- [Deployment adapter](https://github.com/orenaksakal/railway-templates/tree/codex/unique-template-drafts/templates/round10/swagger-editor)
- Image manifest digests and reviewed source references are recorded separately in the repository. Source review is not a runtime test or a verified source-to-image build attestation.
- Repository services build from `orenaksakal/railway-templates`, branch `codex/unique-template-drafts`, with repository-root build context. Keep the branch available.

Upstream software retains its own license and trademarks. This community template does not imply upstream endorsement.
