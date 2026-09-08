# Deploy and Host Formbricks on Railway

Deploy Formbricks **5.4.2**, Hub **0.8.7**, Cube **1.6.6**, PostgreSQL 18 with pgvector, and persistent Valkey. Only Formbricks is public. Hub, Cube, and databases communicate through the private network.

## About Hosting Formbricks

This five-service deployment combines the survey application, Hub, Cube analytics, PostgreSQL with pgvector, and Valkey. Railway builds the included startup adapters from the source repository and supplies a public HTTPS domain for Formbricks. The adapters coordinate database migrations before serving requests; other services stay on the private network. Database, uploads, and cache data use persistent volumes. Authentication and encryption secrets are generated automatically. After the first deployment, create the owner account, configure SMTP if needed, and test a survey from publication through response collection and analytics. Keep a single application replica when using the included local upload storage.

## Common Use Cases

- Collect product feedback and website survey responses.
- Run customer research and satisfaction surveys.
- Review responses and survey analytics in a self-hosted workspace.

## Dependencies for Formbricks Hosting

- Formbricks 5.4.2, Hub 0.8.7, and Cube 1.6.6.
- PostgreSQL 18 with pgvector and a persistent Valkey service.
- A Railway account with capacity for five services and their volumes.
- Optional SMTP provider for verification, password resets, and email delivery.

## Included

Application migrations complete before Hub migrations start. The application waits for Hub before serving requests. Cube includes the upstream tenant-scoped analytics model. Each deployment generates separate encryption, authentication, cron, Hub, Cube, and database secrets. Uploads, database contents, and Valkey data are persistent.

## First use

Open the Formbricks service domain and complete initial setup promptly. Create the first owner account and workspace, publish a survey, and submit a response. Inspect the response and analytics before embedding the survey in a real application.

Email verification and password reset are disabled initially because SMTP is not configured. To enable them, configure `MAIL_FROM`, `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASSWORD`, and the appropriate TLS settings, then set `EMAIL_VERIFICATION_DISABLED=0` and `PASSWORD_RESET_DISABLED=0`. Verify delivery before inviting users. Public HTTPS URLs are generated automatically; update `WEBAPP_URL` and `NEXTAUTH_URL` together when changing domains.

## Data and upgrades

Back up PostgreSQL and the upload volume together. Preserve all encryption/signing secrets. Pin application, Hub, and Cube versions as a compatible set. This template initializes a fresh v5 installation; it is not an automatic v4-to-v5 data migration service. Test upgrades against a restored copy before updating a customer installation.

Local file storage supports one application replica. SAML and other enterprise features require their upstream license and additional configuration; this recipe does not claim to enable them. Optional AI taxonomy/GPU services are not included.

## Acceptance before production

Verify first-owner setup, survey creation/publication, response collection, analytics, file upload/download, embed delivery, restart persistence, and restoration. `/health` only confirms the app responds; it is not a substitute for these functional checks. Hub waits on a versioned PostgreSQL migration marker; startup does not depend on contacting the application over private HTTP. The revised bootstrap must be verified in a fresh Railway deployment.

Upstream: [Formbricks](https://github.com/formbricks/formbricks/tree/5.4.2), [self-hosting documentation](https://formbricks.com/docs/self-hosting/setup/docker). This community template is not an official upstream offering.

## Why Deploy Formbricks on Railway?

Railway keeps the application and its dependencies in one project, with service references, private networking, HTTPS routing, deployment logs, and persistent volumes. This template supplies the service configuration and startup adapters so you can focus on the application setup. Resource usage and volume storage are billed by Railway; third-party services are billed separately. This deployment does not configure automatic backups or high availability.

## Support and Validation

This is an independently maintained community template. Local startup checks and exact Railway template-configuration read-back have passed. Full Railway application workflows and backup/restore certification remain outstanding; test your intended workflow before relying on the deployment. See the [validation record](https://github.com/orenaksakal/railway-templates/blob/codex/railway-template-release/VALIDATION.md) for the tested scope.

For template issues, use the Railway listing’s community thread or [open a repository issue](https://github.com/orenaksakal/railway-templates/issues). Include the service name, image version, and redacted logs; never include passwords, tokens, or connection strings.
