# Deploy and Host Raneto Private Knowledge Base

Markdown knowledge base with browser editing and persistent pages.

## About Hosting

| Service | Access | Persistent storage |
| --- | --- | --- |
| raneto | Public HTTPS with owner authentication | None |
| app | Private Railway network | /data (Markdown pages, page images, and login sessions) |

Railway terminates public TLS. Keep the application at one replica because it uses local persistent storage. Only the gateway has a public service domain.

## Why Deploy Raneto Private Knowledge Base on Railway

An editable Markdown knowledge base without a database dependency. The adapter maps pages and sessions onto one persistent Railway volume and supplies generated native login credentials.

## Common Use Cases

Maintain private runbooks, household instructions, a project handbook, and searchable reference pages.

## First use

Open the Railway public URL and enter gateway username `admin` with the generated `raneto.ACCESS_PASSWORD`. Then sign in to Raneto as `owner` with `app.RANETO_PASSWORD`. Edit the welcome page and create a category and a page. Change `app.SITE_TITLE` for your site title. Keep `SESSION_SECRET` and both passwords with your backups.

The gateway accepts Basic authentication or `X-Template-Key: YOUR_ACCESS_PASSWORD` for clients that can set headers. After an authenticated page response, it sets a Secure, HttpOnly owner cookie so browser requests can also carry the application’s native authorization headers. It consumes Basic Authorization and forwards other authorization schemes. Preserve the gateway and native authentication settings; rotating `ACCESS_PASSWORD` invalidates existing owner cookies.

## Scope and limitations

This is a private knowledge base: the owner gateway protects reading as well as editing. Sessions and pages persist under `/data`; custom theme source is part of the image. Existing pages are never replaced by the welcome-page seed. The adapter drops root privileges before starting Raneto. The 32 MiB gateway request limit also applies to any attachment workflow. SMTP and Google OAuth are not configured.

The reviewed sources and template configuration have static checks. Container builds, fresh Railway startup, complete application workflows, native-client compatibility, volume recovery, and operating costs remain **unverified**. The gateway’s `/healthz` only proves the proxy process is running; it does not establish application readiness. No application deployment was created while preparing this listing.

## Acceptance checks

Reject an unauthenticated request, sign in through both layers, create and edit a Markdown page, create a category, search for the page, and verify that its content and images survive a volume-preserving restart. Confirm native logout blocks editing even when gateway access is still cached.

Before storing important data, stop writes, make a consistent backup of the whole persistent volume and generated secrets, and restore into a separate deployment. Verify records, accounts, and original file bytes. An image rollback does not reverse a database migration.

## Dependencies for Raneto Private Knowledge Base

### Deployment Dependencies

A Railway account with capacity for two services and one persistent volume, access to the selected container registry, and GitHub access to the adapter repository. No external provider account or operator-supplied secret is required. Generated Railway credentials are available in the service variables.

### Source and maintenance

- [Upstream project](https://github.com/ryanlelek/Raneto)
- [Reviewed release source: 0.18.1](https://github.com/ryanlelek/Raneto/tree/e90e2bca5bf1ca1413d5b06fec1e7f701abfad5b)
- [Railway deployment adapter](https://github.com/orenaksakal/railway-templates/tree/codex/unique-template-drafts/templates/round10/raneto)
- Images are locked by digest. The release source was reviewed separately; the image was not independently reproduced from source.
- Repository services build from `orenaksakal/railway-templates`, branch `codex/unique-template-drafts`, using repository-root context. Keep that branch available.

Upstream software retains its own license and trademarks. This community integration does not imply endorsement.
