# Deploy and Host Movary Movie Diary

Track, rate, and review watched movies with a persistent SQLite library.

## About Hosting

| Service | Access | Persistent storage |
| --- | --- | --- |
| movary | Public HTTPS with owner authentication | None |
| app | Private Railway network | /app/storage (SQLite, cached posters, and application storage) |

Railway terminates public TLS. Keep the application at one replica because it uses local persistent storage. Only the gateway has a public service domain.

## Why Deploy Movary Movie Diary on Railway

A dedicated movie diary with watched dates, ratings, and history. SQLite and poster storage share one Railway volume. Startup runs database migrations as the upstream application user and stops on a migration error.

## Common Use Cases

Keep a personal watch diary, compare ratings over time, and build a searchable history of watched films.

## First use

Before deployment, set `app.TMDB_API_KEY` to your own key from [TMDB](https://www.themoviedb.org/settings/api). Open the public URL and authenticate using gateway username `admin` and `movary.ACCESS_PASSWORD`. Complete Movary’s first-user screen and create your administrator. Public registration remains disabled (`ENABLE_REGISTRATION=0`). Search for a movie and log your first watch. If the first-user screen is unavailable, use Railway SSH for the private `app` service and run `php /app/bin/console.php user:create your-email@example.com YOUR_PRIVATE_PASSWORD owner`; replace both placeholders and avoid retaining the password in shared terminal history. Registration can remain closed.

The gateway accepts Basic authentication or `X-Template-Key: YOUR_ACCESS_PASSWORD` for clients that can set headers. After an authenticated page response, it sets a Secure, HttpOnly owner cookie so browser requests can also carry the application’s native authorization headers. It consumes Basic Authorization and forwards other authorization schemes. Preserve the gateway and native authentication settings; rotating `ACCESS_PASSWORD` invalidates existing owner cookies.

## Scope and limitations

Movie lookup depends on your TMDB account and API availability. No SMTP is configured. Additional webhook integrations and clients must support the gateway’s `X-Template-Key` header; compatibility is unverified. Database migrations run on each start, so a rollback requires a matching database backup. Files and requests are limited to 32 MiB by the gateway.

The reviewed sources and template configuration have static checks. Container builds, fresh Railway startup, complete application workflows, native-client compatibility, volume recovery, and operating costs remain **unverified**. The gateway’s `/healthz` only proves the proxy process is running; it does not establish application readiness. No application deployment was created while preparing this listing.

## Acceptance checks

Reject unauthenticated requests, complete first-user setup, search for a film using your TMDB key, add a watched date and rating, check its poster, and confirm the record survives a volume-preserving restart. Confirm ordinary visitors cannot register another account.

Before storing important data, stop writes, make a consistent backup of the whole persistent volume and generated secrets, and restore into a separate deployment. Verify records, accounts, and original file bytes. An image rollback does not reverse a database migration.

## Dependencies for Movary Movie Diary

### Deployment Dependencies

A Railway account with capacity for two services and one persistent volume, access to the selected container registry, and GitHub access to the adapter repository. Your TMDB API key is required. No key is supplied by this template. Other movie-service integrations and SMTP are optional and operator-configured.

### Source and maintenance

- [Upstream project](https://github.com/leepeuker/movary)
- [Reviewed release source: 0.72.0](https://github.com/leepeuker/movary/tree/baf1d9923fdfae6210d844d37a315347f7b0773b)
- [Railway deployment adapter](https://github.com/orenaksakal/railway-templates/tree/codex/unique-template-drafts/templates/round10/movary)
- Images are locked by digest. The release source was reviewed separately; the image was not independently reproduced from source.
- Repository services build from `orenaksakal/railway-templates`, branch `codex/unique-template-drafts`, using repository-root context. Keep that branch available.

Upstream software retains its own license and trademarks. This community integration does not imply endorsement.
