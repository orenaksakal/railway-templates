# Deploy and Host Pinry Visual Bookmark Boards

Private image bookmarks and visual boards with generated administrator.

## About Hosting

| Service | Access | Persistent storage |
| --- | --- | --- |
| pinry | Public HTTPS with owner authentication | None |
| app | Private Railway network | /data (SQLite, media, generated static assets, and persistent settings) |

Railway terminates public TLS. Keep the application at one replica because it uses local persistent storage. Only the gateway has a public service domain.

## Why Deploy Pinry Visual Bookmark Boards on Railway

Image-oriented bookmarking with boards and tags. This adapter creates the first administrator only on an empty user database, keeps registration closed, and avoids the upstream startup path that prints a newly generated Django secret.

## Common Use Cases

Keep visual research, collect reference images, and organize private inspiration boards with tags.

## First use

Set `app.ADMIN_EMAIL` to your administrator email before deployment. Authenticate at the public URL using gateway username `admin` and `pinry.ACCESS_PASSWORD`, then sign in to Pinry as `owner` with `app.ADMIN_PASSWORD`. The first administrator is created automatically only when there are no users. Add an image and create a board. Changing the bootstrap variables later does not reset an existing account; use the application’s account controls.

The gateway accepts Basic authentication or `X-Template-Key: YOUR_ACCESS_PASSWORD` for clients that can set headers. After an authenticated page response, it sets a Secure, HttpOnly owner cookie so browser requests can also carry the application’s native authorization headers. It consumes Basic Authorization and forwards other authorization schemes. Preserve the gateway and native authentication settings; rotating `ACCESS_PASSWORD` invalidates existing owner cookies.

## Scope and limitations

Registration is closed and pins require native login. `/data/local_settings.py` is seeded only once; existing operator settings are preserved. SMTP is not configured. The pinned upstream 2.1.13 image was published in October 2024 and contains an older Python/Django stack; dependency security and compatibility have not been audited. Browser extensions and imported remote image URLs need their own acceptance checks. Uploads must fit the gateway’s 32 MiB limit.

The reviewed sources and template configuration have static checks. Container builds, fresh Railway startup, complete application workflows, native-client compatibility, volume recovery, and operating costs remain **unverified**. The gateway’s `/healthz` only proves the proxy process is running; it does not establish application readiness. No application deployment was created while preparing this listing.

## Acceptance checks

Reject an unauthenticated request, sign in to the generated administrator, create a board, upload a small image, tag it, and verify thumbnails and originals. Confirm signup is closed, pins require login, existing users and settings survive restart, and changing bootstrap credentials does not reset the account.

Before storing important data, stop writes, make a consistent backup of the whole persistent volume and generated secrets, and restore into a separate deployment. Verify records, accounts, and original file bytes. An image rollback does not reverse a database migration.

## Dependencies for Pinry Visual Bookmark Boards

### Deployment Dependencies

A Railway account with capacity for two services and one persistent volume, access to the selected container registry, and GitHub access to the adapter repository. An administrator email is required. The template generates independent gateway, administrator, and Django secrets. Retain all of them with backups.

### Source and maintenance

- [Upstream project](https://github.com/pinry/pinry)
- [Reviewed release source: v2.1.13](https://github.com/pinry/pinry/tree/a21b1e73c2f889499286339b8cc59c411e40b9b1)
- [Railway deployment adapter](https://github.com/orenaksakal/railway-templates/tree/codex/unique-template-drafts/templates/round10/pinry)
- Images are locked by digest. The release source was reviewed separately; the image was not independently reproduced from source.
- Repository services build from `orenaksakal/railway-templates`, branch `codex/unique-template-drafts`, using repository-root context. Keep that branch available.

Upstream software retains its own license and trademarks. This community integration does not imply endorsement.
