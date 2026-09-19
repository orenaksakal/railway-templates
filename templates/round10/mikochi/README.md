# Deploy and Host Mikochi File Browser

Private file browsing, uploads, downloads, and media streaming.

## About Hosting

| Service | Access | Persistent storage |
| --- | --- | --- |
| mikochi | Public HTTPS with owner authentication | None |
| app | Private Railway network | /data (the browsable file library) |

Railway terminates public TLS. Keep the application at one replica because it uses local persistent storage. Only the gateway has a public service domain.

## Why Deploy Mikochi File Browser on Railway

A compact file browser with uploads, downloads, and streaming links. The only browsable directory is mounted persistently, and the template enables both native credentials and an owner gateway.

## Common Use Cases

Browse a small private file library, upload documents, download folders, and play supported media from the browser or compatible clients.

## First use

Open the public URL and use gateway username `admin` with `mikochi.ACCESS_PASSWORD`. Then sign in to Mikochi as `owner` with `app.PASSWORD`. Upload a small file, create a folder, rename the file, and download it again. Native authentication remains enabled (`NO_AUTH=false`).

The gateway accepts Basic authentication or `X-Template-Key: YOUR_ACCESS_PASSWORD` for clients that can set headers. After an authenticated page response, it sets a Secure, HttpOnly owner cookie so browser requests can also carry the application’s native authorization headers. It consumes Basic Authorization and forwards other authorization schemes. Preserve the gateway and native authentication settings; rotating `ACCESS_PASSWORD` invalidates existing owner cookies.

## Scope and limitations

The gateway caps each upload at 32 MiB and uses a 600-second upstream read timeout. This is suitable for small files, not unrestricted bulk media ingestion. External players require gateway authentication in addition to any Mikochi streaming token; VLC/MPV and share-link compatibility are unverified. Mikochi generates a fresh JWT signing secret on restart, intentionally invalidating native tokens. No external filesystem or NAS is mounted.

The reviewed sources and template configuration have static checks. Container builds, fresh Railway startup, complete application workflows, native-client compatibility, volume recovery, and operating costs remain **unverified**. The gateway’s `/healthz` only proves the proxy process is running; it does not establish application readiness. No application deployment was created while preparing this listing.

## Acceptance checks

Reject an unauthenticated request, sign in through both layers, upload and rename a small file, download and compare its bytes, create a folder, and verify the library after a volume-preserving restart. Test media playback with the exact client you intend to use.

Before storing important data, stop writes, make a consistent backup of the whole persistent volume and generated secrets, and restore into a separate deployment. Verify records, accounts, and original file bytes. An image rollback does not reverse a database migration.

## Dependencies for Mikochi File Browser

### Deployment Dependencies

A Railway account with capacity for two services and one persistent volume, access to the selected container registry, and GitHub access to the adapter repository. No external provider account is required. Native and gateway passwords are generated independently.

### Source and maintenance

- [Upstream project](https://github.com/zer0tonin/Mikochi)
- [Reviewed release source: 1.11.0](https://github.com/zer0tonin/Mikochi/tree/cc67722bcce3f54b3d7b4e712b4d8f9d892a156b)
- [Railway deployment adapter](https://github.com/orenaksakal/railway-templates/tree/codex/unique-template-drafts/templates/round10/mikochi)
- Images are locked by digest. The release source was reviewed separately; the image was not independently reproduced from source.
- Repository services build from `orenaksakal/railway-templates`, branch `codex/unique-template-drafts`, using repository-root context. Keep that branch available.

Upstream software retains its own license and trademarks. This community integration does not imply endorsement.
