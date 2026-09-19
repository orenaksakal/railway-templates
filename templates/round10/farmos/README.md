# Deploy and Host farmOS Farm Records

Farm planning, asset and activity records with PostgreSQL and file storage.

## About Hosting

farmOS 4.0.6 provides farm planning, asset records and activity logs on Drupal, backed by PostgreSQL. A single app volume persists the Drupal sites directory, uploaded files, settings and signing keys. Apache recognizes HTTPS forwarded by the private owner gateway, so the installer uses the public HTTPS address.

| Service | Access | Persistent storage |
| --- | --- | --- |
| postgres | Private | /var/lib/postgresql/data |
| core | Private | /data |
| farmos | Public HTTPS | None |

Railway terminates public TLS. Keep volume-backed services at one replica. Database and core application ports are private; only the generated owner gateway is public.

## Why Deploy farmOS Farm Records on Railway

This integration supplies pinned image sources, private dependencies, persistent storage and an authenticated setup path. Public marketplace searches found no matching product listing at preparation time; the repository records the queries and exclusions.

## Common Use Cases

Record agricultural assets and activities, plan field work, keep farm observations and share internal farm records with authorized collaborators.

## First use

Open the gateway using ACCESS_PASSWORD and username admin. Complete the farmOS web installer. Choose PostgreSQL and copy SETUP_DATABASE_NAME, SETUP_DATABASE_USER and SETUP_DATABASE_PASSWORD from core variables. In advanced database options, use SETUP_DATABASE_HOST and port 5432. The SETUP variables are reference values for the installer, not automatic farmOS configuration. Create your farm name and administrator account. Keep uploaded files and signing keys in their default persistent locations.

The owner gateway username is `admin`; retrieve its generated `ACCESS_PASSWORD` from Railway variables. API clients can send `X-Template-Key: YOUR_ACCESS_PASSWORD`. This preserves Bearer authorization; browser HTTP Basic credentials are consumed by the gateway. Keep all generated secrets private.

After gateway authentication, successful page responses set a Secure, HttpOnly owner cookie. This lets browser apps send their native API authorization while retaining gateway access. Rotating `ACCESS_PASSWORD` invalidates existing owner cookies. API clients can continue using `X-Template-Key`.

## Scope and limitations

SMTP, external sensors, OAuth clients and mobile synchronization are not configured. Clients integrating with farmOS must support the owner gateway: send X-Template-Key with the gateway password while retaining their Bearer authorization. Uploaded files are subject to the gateway's 32 MiB request limit and PHP limits. A database upgrade requires the upstream farmOS/Drupal update procedure; changing the image alone does not complete it. Custom modules installed outside /data are not persistent and require a maintained custom image.

The gateway caps requests at 32 MiB and upstream requests at 600 seconds. Its `/healthz` only proves the proxy process is serving; it does not certify application or database readiness.

Container builds, fresh Railway startup, full application workflows, integrations, native-client compatibility, backup restoration and operating costs remain **unverified**. Source review and static checks are not a runtime certification.

## Acceptance checks

Finish setup over HTTPS, create a farm asset and activity log, attach a small image, and verify the exported record. Restart app and database, then confirm login, asset, attachment and signing keys remain. Test any mobile or OAuth integration separately with the gateway header before relying on synchronization.

Back up a consistent PostgreSQL dump together with all of /data, including /data/sites and /data/keys, plus generated database credentials. Restore the database and files into a separate instance, run the appropriate farmOS update procedure when changing versions, and verify asset records, log relationships, attachments and authentication. Container rollback does not revert database migrations.

## Dependencies for farmOS Farm Records

### Deployment Dependencies

A Railway account with capacity for 3 services, persistent-volume support, access to the pinned container registries and this repository branch, and the inputs described above. Optional external providers and their credentials are operator-supplied.

### Source and maintenance

- [Upstream project](https://github.com/farmOS/farmOS)
- [Reviewed source](https://github.com/farmOS/farmOS/tree/d8ef2413a1730482c01425dd28cbe048c2b834a3)
- [Deployment adapter](https://github.com/orenaksakal/railway-templates/tree/codex/unique-template-drafts/templates/round10/farmos)
- Repository services build from `orenaksakal/railway-templates`, branch `codex/unique-template-drafts`, using repository-root context. Keep that branch available.
- Image digests and upstream source references are tracked separately. A source revision is not asserted to match an image without image provenance evidence.

Upstream software retains its own license and trademarks. This community integration does not imply endorsement.
