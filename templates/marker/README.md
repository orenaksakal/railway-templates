# Deploy and Host Marker PDF to Markdown API on Railway

Authenticated CPU API for converting digital PDFs to Markdown.

**Deployment template.** Deployment incurs Railway charges. Supply your own required model, search and external-service credentials; no example provider credentials are included.

## About Hosting Marker PDF to Markdown API

This template provisions 2 services in one Railway project, with image digests or upstream source revisions pinned, generated internal credentials, linked environment variables and the persistent paths listed below. Public HTTP routes use Railway HTTPS. SQL and internal dependency endpoints stay private. Keep stateful services single-replica and configure your own backup policy.

## Live verification — 2026-09-08

Source build with compatible CPU Torch/Torchvision, public authentication and real digital-PDF-to-Markdown conversion passed. Unit tests cover temporary-path isolation, cleanup on failure, invalid/oversized file rejection and concurrent-job rejection. OCR is disabled. Scanned PDFs, load capacity and model-license suitability for each deployer were not tested.

## Setup

POST a PDF multipart field named file to /convert on marker-api. Supply gateway Basic Auth (ACCESS_USER/ACCESS_PASSWORD) plus header X-API-Key equal to marker.API_KEY. The API returns markdown and metadata. /docs requires the same credentials.

## Dependencies for Marker PDF to Markdown API Hosting

### Deployment Dependencies

| Service | Source | Persistent volume | Public HTTP |
|---|---|---|---|
| marker | repository adapter: templates/marker/Dockerfile | /data | Private only |
| marker-api | repository adapter: shared/round4-gateway/Dockerfile | None | 8080 |

## Required inputs

No external secrets are required for initial configuration. Follow the setup instructions for application-level onboarding.

Generated credentials: `marker.API_KEY`, `marker-api.ACCESS_PASSWORD`. Keep them private and preserve relevant encryption keys with backups. Every editor variable includes a description.

## Scope and limitations

Custom narrow wrapper around pinned Marker: no caller-supplied filesystem paths, no original /marker route, random temporary upload filenames, deletion in finally, 32 MiB gateway limit and one conversion at a time. Fast CPU mode disables OCR; scanned PDFs and image-rich OCR workloads are not supported by this draft. Model downloads are lazy and cached in /data. Marker code and model weights have different licenses; review the upstream model-weight commercial terms, including the stated revenue/funding threshold. Python transitive dependencies require a resolved lock before release.

## Recommended acceptance checks

CPU image build; model download; reject missing credentials and oversized requests; adversarial filenames; digital PDF conversion; temporary-file cleanup after failure; concurrent request rejection; memory/timeout measurements; model-license review.

## Operations

Keep database and internal service endpoints private. Railway provides HTTPS for the explicitly exposed HTTP services. Back up the listed persistent volumes and database exports, preserve encryption keys, and test a restore before relying on this instance. Review upstream migrations before upgrades. Single-volume services use one replica; no multi-region or high-availability guarantee is made. A gateway health response only proves the gateway is alive.

## Sources

- [Upstream project](https://github.com/datalab-to/marker)
- [Reviewed source snapshot](https://github.com/datalab-to/marker/tree/36b3947d05b16787937fc77db47422c9a6bc0e29)
- Image digest pins: `images.round4.lock.json` in the template source repository. Source snapshots are research references; image digests do not prove the image was built from that same commit.
- Base-image pins do not lock every package installed by apt/apk/pip. See the verification scope above before relying on this deployment.

## Common Use Cases

- Convert digital PDFs to Markdown through an authenticated API.
- Extract text for downstream indexing without exposing filesystem-path inputs.

## Why Deploy Marker PDF to Markdown API on Railway?

Railway groups service deployment, logs, private networking, generated environment references and persistent volumes in one project. This community template supplies the configuration and setup notes; Railway resource charges and external provider costs remain separate. No fixed cost or capacity guarantee is made.
