# Deploy and Host Speedtest Tracker Regional Egress

Track Railway-region Internet performance with persistent test history.

## About Hosting

Speedtest Tracker 1.15.0 records download/upload throughput, latency and historical trends in a persistent SQLite database. Tests originate from the Railway region where the app runs. The container scheduler is included, but automatic speed tests start disabled.

| Service | Access | Persistent storage |
| --- | --- | --- |
| core | Private | /config |
| speedtest-tracker | Public HTTPS | None |

Railway terminates public TLS. Keep volume-backed services at one replica. Database and core application ports are private; only the generated owner gateway is public.

## Why Deploy Speedtest Tracker Regional Egress on Railway

This integration supplies pinned image sources, private dependencies, persistent storage and an authenticated setup path. Public marketplace searches found no matching product listing at preparation time; the repository records the queries and exclusions.

## Common Use Cases

Compare cloud-region connectivity over time, investigate changes in outbound throughput and retain a private record of manually triggered network checks.

## First use

Open the gateway using its generated ACCESS_PASSWORD and username admin, then sign in with the upstream initial account admin@example.com and password password. Immediately change that account email and password. Run one manual test before enabling a schedule. The generated 32-character APP_KEY is already supplied and must remain unchanged when reusing the volume. To enable periodic testing after checking bandwidth use, set SPEEDTEST_SCHEDULE to a conservative cron expression such as 0 3 * * *.

The owner gateway username is `admin`; retrieve its generated `ACCESS_PASSWORD` from Railway variables. API clients can send `X-Template-Key: YOUR_ACCESS_PASSWORD`. This preserves Bearer authorization; browser HTTP Basic credentials are consumed by the gateway. Keep all generated secrets private.

After gateway authentication, successful page responses set a Secure, HttpOnly owner cookie. This lets browser apps send their native API authorization while retaining gateway access. Rotating `ACCESS_PASSWORD` invalidates existing owner cookies. API clients can continue using `X-Template-Key`.

## Scope and limitations

Results measure Railway regional Internet egress, not your home Internet connection or your browser-to-Railway speed. Tests consume transfer and may incur bandwidth charges; automatic tests are disabled initially. Ookla server reachability and speed-test behavior from a cloud network are unverified. SMTP and notification integrations are not configured. The public dashboard stays disabled. Keep the additional gateway because upstream ships initial credentials.

The gateway caps requests at 32 MiB and upstream requests at 600 seconds. Its `/healthz` only proves the proxy process is serving; it does not certify application or database readiness.

Container builds, fresh Railway startup, full application workflows, integrations, native-client compatibility, backup restoration and operating costs remain **unverified**. Source review and static checks are not a runtime certification.

## Acceptance checks

Change the default login, run one manual test, inspect throughput and latency in history, restart the core service, and confirm the account and result persist. Verify the gateway denies unauthenticated requests. If scheduling is enabled, confirm exactly the intended schedule runs and review bandwidth usage.

Back up /config with the application quiesced or use SQLite's backup facility for a consistent database snapshot. Preserve APP_KEY and native user credentials. Restore to a separate service using the same APP_KEY and verify a historical result, user login and application settings before replacing the original. Container rollback does not revert database migrations.

## Dependencies for Speedtest Tracker Regional Egress

### Deployment Dependencies

A Railway account with capacity for 2 services, persistent-volume support, access to the pinned container registries and this repository branch, and the inputs described above. Optional external providers and their credentials are operator-supplied.

### Source and maintenance

- [Upstream project](https://github.com/alexjustesen/speedtest-tracker)
- [Reviewed source](https://github.com/alexjustesen/speedtest-tracker/tree/fce6eb36181ed70b5b0763c391a50b806d7e3da7)
- [Deployment adapter](https://github.com/orenaksakal/railway-templates/tree/codex/unique-template-drafts/templates/round10/speedtest-tracker)
- Repository services build from `orenaksakal/railway-templates`, branch `codex/unique-template-drafts`, using repository-root context. Keep that branch available.
- Image digests and upstream source references are tracked separately. A source revision is not asserted to match an image without image provenance evidence.

Upstream software retains its own license and trademarks. This community integration does not imply endorsement.
