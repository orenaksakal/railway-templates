# Deploy and Host PlantUML Private Diagram Renderer

Render UML diagrams from text behind owner access and sandbox controls.

## About Hosting

PlantUML Server converts textual UML descriptions into images. The private Jetty service listens on port 8080 and the owner gateway exposes HTTPS. This stateless renderer has no persistent volume; preserve your diagram source files in your own repository.

## Why Deploy PlantUML Private Diagram Renderer on Railway

Provide a private rendering endpoint for architecture and sequence diagrams with an immutable container image. The `SANDBOX` security profile blocks diagram access to local files and remote URLs. The Java heap is bounded at 512 MiB, with additional Railway memory needed for JVM overhead and Graphviz.

## Common Use Cases

- Render sequence and class diagrams for internal documentation.
- Preview diagrams without sending their source to a public renderer.
- Use an authenticated rendering endpoint from a compatible documentation pipeline.

## First use

Open the plantuml service URL and authenticate with username `admin` and its `ACCESS_PASSWORD`. Paste a short diagram such as `@startuml
Alice -> Bob: hello
@enduml` into the editor and render it. API clients must include `X-Template-Key: YOUR_ACCESS_PASSWORD` when requesting an encoded `/svg/...` or `/png/...` URL. Integrations unable to send that header or Basic credentials need a separate compatible access design.

Keep the generated owner password private. The gateway supports browser Basic authentication with username `admin` and API access through `X-Template-Key`. It preserves Bearer authorization and limits request bodies to 32 MiB with a 600-second proxy read timeout.

## Storage and backups

None; maintain source diagrams and rendered exports separately. Back up source documents and any persistent volume before upgrades. Test a restore into a separate instance before relying on the template for important work. Do not scale a volume-backed core beyond one replica.

After gateway authentication, successful page responses set a Secure, HttpOnly owner cookie. This lets browser apps send their native API authorization while retaining gateway access. Rotating `ACCESS_PASSWORD` invalidates existing owner cookies. API clients can continue using `X-Template-Key`.

## Scope and limitations

Remote includes and local file reads are disabled by `SANDBOX`; keep this setting for the supplied topology. Large or complex diagrams can consume substantial CPU and memory even within the 4096-pixel limit. This template does not store diagram history, and it does not include a collaborative editor.

Application container builds, fresh Railway startup, full browser/API workflows, restart persistence, backup restoration, capacity and costs remain unverified. Checks performed for this template cover source configuration, manifest metadata, template references, and publication inputs. The gateway `/healthz` only confirms the proxy process is available, not application readiness.

## Acceptance checks

Render a small sequence diagram as SVG and PNG, verify unauthenticated rendering is rejected, and check that a diagram trying to include a remote URL is refused. Restart core and render the same saved source again.

## Dependencies for PlantUML Private Diagram Renderer

### Deployment Dependencies

A Railway account with capacity for two services, access to the pinned image registry and this repository branch, and persistent volume capacity where listed. No external database or provider account is included or required for the starter workflow.

### Source and maintenance

- [Upstream project](https://github.com/plantuml/plantuml-server)
- [Reviewed source revision](https://github.com/plantuml/plantuml-server/tree/5dda8847617e2a4978b61367a2570dcdec3f14f7)
- [Deployment adapter](https://github.com/orenaksakal/railway-templates/tree/codex/unique-template-drafts/templates/round10/plantuml)
- Image manifest digests and reviewed source references are recorded separately in the repository. Source review is not a runtime test or a verified source-to-image build attestation.
- Repository services build from `orenaksakal/railway-templates`, branch `codex/unique-template-drafts`, with repository-root build context. Keep the branch available.

Upstream software retains its own license and trademarks. This community template does not imply upstream endorsement.
