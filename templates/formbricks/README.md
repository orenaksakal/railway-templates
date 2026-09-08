# Formbricks surveys and analytics on Railway

Deploy Formbricks **5.4.2**, Hub **0.8.7**, Cube **1.6.6**, PostgreSQL 18 with pgvector, and persistent Valkey. Only Formbricks is public. Hub, Cube, and databases communicate through the private network.

## Included

Application migrations complete before Hub migrations start. The application waits for Hub before serving requests. Cube includes the upstream tenant-scoped analytics model. Each deployment generates separate encryption, authentication, cron, Hub, Cube, and database secrets. Uploads, database contents, and Valkey data are persistent.

## First use

Open the Formbricks service domain and complete initial setup promptly. Create the first owner account and workspace, publish a survey, and submit a response. Inspect the response and analytics before embedding the survey in a real application.

Email verification and password reset are disabled initially because SMTP is not configured. To enable them, configure `MAIL_FROM`, `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASSWORD`, and the appropriate TLS settings, then set `EMAIL_VERIFICATION_DISABLED=0` and `PASSWORD_RESET_DISABLED=0`. Verify delivery before inviting users. Public HTTPS URLs are generated automatically; update `WEBAPP_URL` and `NEXTAUTH_URL` together when changing domains.

## Data and upgrades

Back up PostgreSQL and the upload volume together. Preserve all encryption/signing secrets. Pin application, Hub, and Cube versions as a compatible set. This template initializes a fresh v5 installation; it is not an automatic v4-to-v5 data migration service. Test upgrades against a restored copy before updating a customer installation.

Local file storage supports one application replica. SAML and other enterprise features require their upstream license and additional configuration; this recipe does not claim to enable them. Optional AI taxonomy/GPU services are not included.

## Acceptance before production

Verify first-owner setup, survey creation/publication, response collection, analytics, file upload/download, embed delivery, restart persistence, and restoration. `/health` only confirms the app responds; it is not a substitute for these functional checks. The private migration readiness listener on port 3001 must not receive a public domain.

Upstream: [Formbricks](https://github.com/formbricks/formbricks/tree/5.4.2), [self-hosting documentation](https://formbricks.com/docs/self-hosting/setup/docker). This community template is not an official upstream offering.
