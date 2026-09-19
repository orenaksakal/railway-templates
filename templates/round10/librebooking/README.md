# Deploy and Host LibreBooking Resource Scheduler

Private room and equipment reservations with MariaDB and durable uploads.

## About Hosting

LibreBooking 5.3.0 manages reservations for rooms, equipment and shared resources. A private MariaDB service stores accounts and reservations; one app volume stores configuration, resource images and reservation attachments. Only the owner gateway receives a public domain.

| Service | Access | Persistent storage |
| --- | --- | --- |
| mariadb | Private | /var/lib/mysql |
| core | Private | /data |
| librebooking | Public HTTPS | None |

Railway terminates public TLS. Keep volume-backed services at one replica. Database and core application ports are private; only the generated owner gateway is public.

## Why Deploy LibreBooking Resource Scheduler on Railway

This integration supplies pinned image sources, private dependencies, persistent storage and an authenticated setup path. Public marketplace searches found no matching product listing at preparation time; the repository records the queries and exclusions.

## Common Use Cases

Reserve meeting rooms, schedule shared laboratory equipment, coordinate community facilities and manage internal resource calendars.

## First use

Set LB_ADMIN_EMAIL to your intended administrator address before deployment. Open the gateway using ACCESS_PASSWORD and username admin. Visit /install, enter the generated LB_INSTALL_PASSWORD, and use database user librebooking with LB_DATABASE_PASSWORD. Leave Create database and Create database user unchecked because MariaDB already created them. Complete schema installation, then follow the registration link and create the first account with exactly LB_ADMIN_EMAIL. After signing in, set LB_REGISTRATION_ALLOW_SELF_REGISTRATION=false and clear LB_INSTALL_PASSWORD, then redeploy. Administrators can add additional users.

The owner gateway username is `admin`; retrieve its generated `ACCESS_PASSWORD` from Railway variables. API clients can send `X-Template-Key: YOUR_ACCESS_PASSWORD`. This preserves Bearer authorization; browser HTTP Basic credentials are consumed by the gateway. Keep all generated secrets private.

After gateway authentication, successful page responses set a Secure, HttpOnly owner cookie. This lets browser apps send their native API authorization while retaining gateway access. Rotating `ACCESS_PASSWORD` invalidates existing owner cookies. API clients can continue using `X-Template-Key`.

## Scope and limitations

This is a private resource scheduler: each user needs gateway access as well as an application account. SMTP, email password resets, reservation reminders, and scheduled cleanup are disabled or not configured. The web image contains background-job tooling, but this template does not start a cron worker; do not enable scheduled email features without adding and verifying that worker. Native calendar/API clients must support the extra gateway authentication. Reservation attachments are limited by the gateway and PHP request limits. Do not enable public guest reservations or remove the gateway without a separate security review.

The gateway caps requests at 32 MiB and upstream requests at 600 seconds. Its `/healthz` only proves the proxy process is serving; it does not certify application or database readiness.

Container builds, fresh Railway startup, full application workflows, integrations, native-client compatibility, backup restoration and operating costs remain **unverified**. Source review and static checks are not a runtime certification.

## Acceptance checks

Create two users and a resource, book a time slot, verify a conflicting booking is rejected, upload an attachment, and confirm the intended second user can view only the permitted records. Restart app and database, then verify the reservation, resource image and attachment remain. Confirm registration is closed and /install is disabled after setup.

Create a consistent MariaDB dump and back up all of /data, especially /data/config, /data/images and /data/reservations. Preserve generated secrets and the administrator email. Restore database and files into a separate instance, then verify login, a reservation and an attachment. Clear or rotate the installer password again after upgrades. Container rollback does not revert database migrations.

## Dependencies for LibreBooking Resource Scheduler

### Deployment Dependencies

A Railway account with capacity for 3 services, persistent-volume support, access to the pinned container registries and this repository branch, and the inputs described above. Optional external providers and their credentials are operator-supplied.

### Source and maintenance

- [Upstream project](https://github.com/LibreBooking/app)
- [Reviewed source](https://github.com/LibreBooking/app/tree/80928da3ee8f2c8f3a1e5c3abfa19c889c183e17)
- [Deployment adapter](https://github.com/orenaksakal/railway-templates/tree/codex/unique-template-drafts/templates/round10/librebooking)
- Repository services build from `orenaksakal/railway-templates`, branch `codex/unique-template-drafts`, using repository-root context. Keep that branch available.
- Image digests and upstream source references are tracked separately. A source revision is not asserted to match an image without image provenance evidence.

Upstream software retains its own license and trademarks. This community integration does not imply endorsement.
