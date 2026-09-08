# Deploy and Host DBOS Durable Webhooks on Railway

A working Node.js service built with DBOS SDK 4.27.6 accepts authenticated JSON events, schedules durable processing, and stores the workflow result in PostgreSQL. This is an application template, not a standalone DBOS orchestration server.

> Verified in an isolated Railway deployment. See the validation scope below for the checks performed and operational limits.

## About Hosting DBOS Durable Webhooks

The template defines 2 services with pinned container digests, generated deployment secrets, explicit service references, and persistent volumes for stateful dependencies. Repository-backed adapters build from `codex/remaining-template-drafts`. Railway terminates HTTPS for the public endpoints; databases and internal workers have no public TCP proxies. Cold-start initialization was verified in a fresh Railway project. Each deployment has its own database and storage resources. Backups are not scheduled by this template, and filesystem-backed services should remain single-replica.

## Common Use Cases

- Receive authenticated events with idempotent submission.
- Demonstrate durable delays and recovery after process termination.
- Extend the registered workflow with your own application steps.

## Dependencies for DBOS Durable Webhooks Hosting

| Service | Source | Persistent path |
| --- | --- | --- |
| postgres | `postgres:17` | `/var/lib/postgresql/data` |
| dbos | `templates/dbos/Dockerfile` | `None` |

Required input before deployment: none; generated secrets and service references supply the template defaults.

## First Use

Read `API_KEY` from the dbos service after deployment. Submit an event with a stable `Idempotency-Key`, then poll the returned status URL. A repeated key with identical event content and delay returns the same workflow ID. Different content gets a different workflow ID. Keep one replica because this example uses a fixed executor identity. The endpoint accepts at most 64 KiB and a delay from 0 to 3600 seconds.

```sh
curl "$DBOS_URL/events" -H "Authorization: Bearer $API_KEY" \
  -H 'Idempotency-Key: first-event' -H 'Content-Type: application/json' \
  -d '{"event":{"message":"hello"},"delaySeconds":5}'
# GET the returned statusUrl with the same Authorization header.
```

## Scope and Limitations

The workflow currently computes and persists a SHA-256 digest and the input event. It does not send outbound webhooks or provide a billing system. Extend it with DBOS steps for external side effects. This example uses one shared operator key, not per-user authorization.

## Backups and Upgrades

Back up the PostgreSQL database, API key, and source revision together. Running work and results live in the DBOS system schema. Test restoration into an isolated project before depending on the backup. Image rollback alone does not revert database migrations.

## Validation Scope

The pinned Linux container built locally and on Railway. Fresh Railway deployment passed HTTPS health, generated-key authentication, unauthorized-request rejection, idempotent event submission, and durable result retrieval. Application/database restart and volume-preserving redeploy were tested. A PostgreSQL dump restored into a separate database with the completed workflow intact. Local forced-process-termination recovery also passed. Backups are not scheduled automatically; load testing, high availability, and a full separate-project disaster-recovery drill are not included.

## Why Deploy DBOS Durable Webhooks on Railway?

Railway keeps the services, networking, environment references, deployment logs, and volumes together in one project. This template supplies the tested service configuration. Railway resources and volume storage are billed separately from external email, model, and other service providers. No deployment cost or revenue estimate has been measured.

## Support and Upstream

[Upstream source and release](https://github.com/dbos-inc/dbos-transact-ts/tree/v4.27). This is an independent community integration; upstream licenses, trademarks, and paid-feature restrictions remain in effect. See the [draft readiness record](https://github.com/orenaksakal/railway-templates/blob/codex/remaining-template-drafts/DRAFTS.md). Report issues with redacted logs and image versions; never share credentials.
