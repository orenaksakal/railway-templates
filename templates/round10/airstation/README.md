# Deploy and Host Airstation Private Radio

Private radio studio and music player with durable tracks and SQLite.

## About Hosting

| Service | Access | Persistent storage |
| --- | --- | --- |
| airstation | Public HTTPS with owner authentication | None |
| app | Private Railway network | /data (SQLite metadata and original audio tracks) |

Railway terminates public TLS. Keep the application at one replica because it uses local persistent storage. Only the gateway has a public service domain.

## Why Deploy Airstation Private Radio on Railway

A small private radio station with a studio, queue, and listener player. The template puts the SQLite database and audio library under one persistent mount while keeping transcoding scratch files ephemeral.

## Common Use Cases

Run a private listening room, arrange a music queue, and share a radio player with a small group that has the owner gateway password.

## First use

Authenticate to the public URL using gateway username `admin` and `airstation.ACCESS_PASSWORD`. Open `/studio/` (including the trailing slash) and sign in using `app.AIRSTATION_SECRET_KEY`. Upload a small audio file, add it to the queue, and open `/` to use the listener player. `AIRSTATION_JWT_SIGN` signs native sessions; keep it private and stable.

The gateway accepts Basic authentication or `X-Template-Key: YOUR_ACCESS_PASSWORD` for clients that can set headers. After an authenticated page response, it sets a Secure, HttpOnly owner cookie so browser requests can also carry the application’s native authorization headers. It consumes Basic Authorization and forwards other authorization schemes. Preserve the gateway and native authentication settings; rotating `ACCESS_PASSWORD` invalidates existing owner cookies.

## Scope and limitations

This template intentionally protects both studio and listener player, so it is a private station. Audio uploads must be smaller than 32 MiB. HLS playback through the owner gateway, player reconnection, audio formats, and transcoding behavior require live acceptance checks. Transcoding uses CPU and scratch disk; generated temporary files under `/tmp/airstation` do not survive restarts. Music licenses and distribution rights are the operator’s responsibility.

The reviewed sources and template configuration have static checks. Container builds, fresh Railway startup, complete application workflows, native-client compatibility, volume recovery, and operating costs remain **unverified**. The gateway’s `/healthz` only proves the proxy process is running; it does not establish application readiness. No application deployment was created while preparing this listing.

## Acceptance checks

Reject unauthenticated requests, enter the studio with the generated native key, upload a small audio file you may use, add it to the queue, and play it from a second authenticated browser. Restart with the volume preserved and confirm tracks and metadata remain. Verify the player resumes as expected rather than assuming uninterrupted broadcast.

Before storing important data, stop writes, make a consistent backup of the whole persistent volume and generated secrets, and restore into a separate deployment. Verify records, accounts, and original file bytes. An image rollback does not reverse a database migration.

## Dependencies for Airstation Private Radio

### Deployment Dependencies

A Railway account with capacity for two services and one persistent volume, access to the selected container registry, and GitHub access to the adapter repository. No external account is required. Supply your own permitted audio. Separate studio, session-signing, and gateway keys are generated.

### Source and maintenance

- [Upstream project](https://github.com/cheatsnake/airstation)
- [Reviewed release source: 1.4.1](https://github.com/cheatsnake/airstation/tree/78c3e31e60f0f65c9f3b1c4e3cad617fb3825db1)
- [Railway deployment adapter](https://github.com/orenaksakal/railway-templates/tree/codex/unique-template-drafts/templates/round10/airstation)
- Images are locked by digest. The release source was reviewed separately; the image was not independently reproduced from source.
- Repository services build from `orenaksakal/railway-templates`, branch `codex/unique-template-drafts`, using repository-root context. Keep that branch available.

Upstream software retains its own license and trademarks. This community integration does not imply endorsement.
