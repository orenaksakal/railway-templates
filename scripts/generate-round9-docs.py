"""Generate marketplace overviews for the recovered, eligible release batch."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]

def main():
    metadata = json.loads((ROOT / 'marketplace.round9.json').read_text())
    docs = json.loads((ROOT / 'docs.round9.json').read_text())
    sources = json.loads((ROOT / 'sources.round9.lock.json').read_text())
    for slug, meta in metadata.items():
        folder = ROOT / 'templates/round9' / slug
        services = list(json.loads((folder / 'template.json').read_text())['services'].values())
        rows = '\n'.join('| ' + s['name'] + ' | ' + ('Public HTTPS' if s['networking']['serviceDomains'] else 'Private') + ' | ' + (', '.join(v['mountPath'] for v in s.get('volumeMounts', {}).values()) or 'None') + ' |' for s in services)
        required = [f"- `{s['name']}.{key}`: {v['description']}" for s in services for key, v in s['variables'].items() if not v['isOptional'] and not v.get('defaultValue')]
        inputs = '\n'.join(required) or 'No mandatory operator-supplied variables. Retrieve generated credentials from the service variables.'
        d = docs[slug]
        text = f'''# Deploy and Host {meta['name']}

{meta['description']}

## About Hosting

| Service | Access | Persistent storage |
| --- | --- | --- |
{rows}

Railway provides the public HTTPS endpoint. Dependencies stay on private networking. Keep each volume-backed service at one replica.

## Why Deploy {meta['name']} on Railway

This definition includes pinned container sources, documented storage paths and generated credentials where required. It restores the missing repository adapters from the previous draft and keeps the application setup steps explicit.

## Common Use Cases

{meta['description']}

## First use

{inputs}

{d['setup']}

Where an owner gateway is included, the username is admin. API clients can use `X-Template-Key: YOUR_ACCESS_PASSWORD`. The gateway consumes Basic Authorization, preserves Bearer authorization and WebSocket upgrades, and caps requests at 32 MiB; check compatibility with native clients. Generated credentials must remain private.

## Scope and limitations

{d['limitations']}

Source and static configuration checks are recorded in the repository's release report. Container builds, fresh Railway startup, native-client compatibility, full application workflows, backup restoration and costs have not been verified. A proxy healthcheck is not application readiness.

## Acceptance checks

{d['acceptance']}

Verify first use, unauthorized rejection where applicable, and a volume-preserving redeploy. Back up every persistent volume, generated application key and consistent database export. Restore into a separate instance and verify accounts, records and uploaded bytes before using important data. Container rollback does not revert database migrations.

## Dependencies for {meta['name']}

### Deployment Dependencies

A Railway account with capacity for {len(services)} services, access to the selected registries and repository source, and the inputs listed above. External provider accounts and optional integrations are operator-supplied.

### Source and maintenance

- [Upstream project](https://github.com/{sources[slug]['repo']})
- [Reviewed application source](https://github.com/{sources[slug]['repo']}/tree/{sources[slug]['sha']})
- [Deployment adapter](https://github.com/orenaksakal/railway-templates/tree/codex/unique-template-drafts/templates/round9/{slug})
- Repository services build from `orenaksakal/railway-templates`, branch `codex/unique-template-drafts`, with repository-root build context. Keep the branch available.
- Image digests and source references are tracked separately. A source revision is not asserted to match a rolling image unless the image metadata establishes it.

Upstream software retains its own license and trademarks. This community integration does not imply endorsement.
'''
        (folder / 'README.md').write_text(text)

if __name__ == '__main__':
    main()
