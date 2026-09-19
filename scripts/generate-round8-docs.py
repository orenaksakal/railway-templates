"""Product-specific documentation for verified marketplace-gap candidates."""
import json
from catalog_round8 import ROOT, CATALOG, BRANCH, configuration

# title, category, concise description, setup, functional check, limitation
DOCS = {
    'jelu': ('Jelu Reading Tracker', 'Other', 'Reading lists, book metadata and reviews with persistent SQLite.',
        'Create the initial owner account behind the gateway. Database, covers and imports are redirected into the single /data volume.',
        'Add a book by ISBN and one manually; record a reading event and review, attach a cover, restart and confirm the history and image remain.',
        'Metadata lookup depends on upstream book providers. This is a reading tracker, not ebook distribution or library DRM.'),
    'grimoire': ('Grimoire Bookmark Workspace', 'Other', 'Local-first bookmarks and search in a private persistent workspace.',
        'Open the workspace behind the gateway. Optional AI enrichment requires your own model credentials in the application settings. The current v1.2 rewrite is built from a checksum-verified source archive.',
        'Save a URL, import a small bookmark file, extract readable content, search it and verify data after restart. Test semantic search separately if a provider is configured.',
        'Not an upgrade path for legacy v0.5 installations. AI providers cost extra. Build dependencies and the application workflow have not been executed in Railway.'),
    'linkace': ('LinkAce Bookmark Archive', 'Other', 'Bookmarks with SQLite search, persistent storage and protected setup.',
        'Complete LinkAce setup behind the gateway and create an administrator. This draft selects the upstream SQLite/database-search mode, with synchronous jobs, rather than the optional Meilisearch topology.',
        'Save links, assign tags and lists, search them, export and reimport a small set, then verify records after a restart.',
        'Uses one replica and synchronous jobs. Large imports can block requests. SMTP, Internet Archive integration and scheduled maintenance need separate configuration and testing.'),
    'solidinvoice': ('SolidInvoice Billing Workspace', 'Other', 'Quotes and invoices with private MySQL and protected installation.',
        'Complete the protected installer. Copy SETUP_DATABASE_HOST, PORT, NAME, USER and PASSWORD from core into its MySQL form; these helper variables are not automatic application settings. Create your own administrator and organization.',
        'Create a client, quote and invoice; download a PDF, restart, and verify invoice data. Configure SMTP and test delivery only with your own account.',
        'Payment gateways and tax/legal suitability are operator responsibilities. Preserve /etc/solidinvoice and a consistent MySQL backup together. No financial transaction is performed during drafting.'),
    'titra': ('Titra Project Time Tracking', 'Other', 'Project time tracking with private authenticated MongoDB.',
        'Register the owner behind the gateway and review registration permissions in Titra before inviting anyone. ROOT_URL and the private MongoDB URL are prewired.',
        'Create a project, record two time entries, run a report and export, restart and confirm the entries remain.',
        'This is a single MongoDB node, not a replica set or high-availability service. The generated MongoDB administrator is limited to this private project database service.'),
    'fava': ('Fava Beancount Ledger', 'Other', 'A private Beancount web ledger with a persistent starter journal.',
        'Open the seeded ledger behind the gateway. Replace the clearly marked example transaction with your own journal through the editor or an authenticated file-management workflow.',
        'Edit and balance a small synthetic transaction, view account balances, download the journal and confirm changes after restart. A pre-existing main.beancount file is never overwritten by startup.',
        'Fava 1.30.16 is package-pinned; transitive Python dependencies are resolved at build time. This is ledger software, not bank synchronization or accounting certification. Preserve included journal files together.'),
    'yaade': ('Yaade API Workspace', 'Other', 'A private collaborative API client with persistent request collections.',
        'After the gateway, log in as admin with the upstream initial password password and immediately change it in Account settings. The default account is never exposed directly.',
        'Create a collection and environment, call a harmless endpoint you control, save and export the collection, restart and verify it remains.',
        'The upstream latest image is digest-pinned; its source has an older update cadence. Browser extension support, OAuth and client access must be verified independently.'),
    'wiremock': ('WireMock Private API Stubs', 'Starters', 'Persistent HTTP API stubs behind generated owner access.',
        'Use the gateway header X-Template-Key with its generated ACCESS_PASSWORD when calling the admin API and stub endpoints. Create mappings with persistent=true, or save mappings through /__admin/mappings/save.',
        'POST a mapping to /__admin/mappings for GET /hello returning hello, call it, save mappings, restart and verify the same response. Confirm requests without the owner credential are blocked.',
        'No public open proxy or production traffic capture is configured. Request journals are bounded and not persisted. Basic Authorization is stripped by the gateway; tests that inspect that header need an adapted gateway or private access.'),
    'mockserver': ('MockServer Private Expectations', 'Starters', 'HTTP mock expectations with bounded logs and persistent configuration.',
        'Use X-Template-Key for the owner gateway and the standard MockServer HTTP API. A new volume receives an empty expectation array; existing expectations are preserved.',
        'PUT an expectation to /mockserver/expectation, invoke its path, restart and verify the expectation reloads. Test unauthorized rejection separately.',
        'No proxy recording or external forwarding is preconfigured. Only expectations persist, not request logs. Public access uses HTTP through the gateway; other protocol modes are outside this draft.'),
    'sqlpage': ('SQLPage Private App Starter', 'Starters', 'A private SQL-driven web app with persistent pages and SQLite.',
        'Open the starter page through the gateway. Edit /data/www/index.sql or add SQL pages through an authenticated Railway shell. The SQLite database is /data/app.db.',
        'Load the SQLite-version page, add a small table and a read-only SQL page for it, restart and confirm both the page and rows remain.',
        'The starter does not implement per-user application permissions. All gateway users share the app. Review SQL, query access and form validation before turning it into a business application.'),
    'lingarr': ('Lingarr Subtitle Translation', 'Other', 'A private subtitle translation service with persistent SQLite settings.',
        'Configure an operator-owned translation provider and a small subtitle source reachable by the container. For stored test files, use a subdirectory under /app/config and configure the application paths accordingly.',
        'Translate a short synthetic subtitle file, verify its language and timing, restart and confirm settings and queue state. Verify the exact file-ingestion workflow before release.',
        'No GPU, translation model, local NAS mount or media library is bundled. Remote Sonarr/Radarr and provider connectivity require operator setup. Provider costs and subtitle/media rights are separate.'),
    'dumbpad': ('DumbPad Private Notepad', 'Other', 'Autosaving Markdown notes with generated PIN and persistent files.',
        'Unlock the gateway and then enter DUMBPAD_PIN from core. Use the note editor; keep both access controls enabled.',
        'Create two notes, format Markdown, search their text, reload and restart, then confirm both files remain.',
        'Single shared notebook access, not separate per-user accounts. The chosen tagged release is older; review upstream maintenance before production use.'),
    'dumbassets': ('DumbAssets Private Inventory', 'Other', 'Asset records, receipts and warranties with generated owner access.',
        'Unlock the gateway and enter DUMBASSETS_PIN from core. Create your inventory and optionally configure your own Apprise destination.',
        'Add an asset, warranty date and a small receipt/photo, export records, restart and verify the record and attachment.',
        'Single shared household/workshop inventory. Notifications are optional and untested. The chosen tagged release is older; review maintenance suitability.'),
    'dumbbudget': ('DumbBudget Personal Finance', 'Other', 'Manual budgets and transactions with persistent owner-protected data.',
        'Unlock the gateway and enter DUMBBUDGET_PIN from core. Set your currency and create an initial budget.',
        'Add an income and expense, check totals, export records, restart and verify the balances remain.',
        'Manual personal finance tracking. No bank synchronization, regulated accounting or multi-user isolation is included. The rolling image is captured by digest.'),
    'dumbkan': ('DumbKan Private Kanban', 'Other', 'A lightweight persistent Kanban board with generated owner access.',
        'Unlock the gateway and enter DUMBKAN_PIN from core. Create your first board and cards.',
        'Create a card, move it between columns, edit its details, restart and confirm its position and contents.',
        'Shared-board access with file-based storage; use one replica. Upstream uses an older Node base. Treat dependency maintenance as a release gate, not as proof of a broken Railway competitor.'),
    'dumbdrop': ('DumbDrop Private File Inbox', 'Storage', 'A persistent file-upload inbox protected by gateway and generated PIN.',
        'Unlock the gateway and enter DUMBDROP_PIN from core. Files are stored in /app/uploads. The application limit is 25 MB and gateway request limit is 32 MiB.',
        'Upload a small synthetic file, inspect and retrieve it through an authenticated operator workflow, restart and confirm the file remains. Verify oversized uploads are rejected.',
        'An upload inbox, not an anonymous sharing site. No automatic retention or offsite backup is configured; set storage limits and cleanup rules before inviting uploaders.'),
    'maintainerr': ('Maintainerr Media Rules', 'Automation', 'Media-library review rules with persistent configuration and owner access.',
        'Connect your own reachable media server after opening the owner gateway. Begin with a non-destructive review/collection rule and review results before enabling any deletion action.',
        'Connect a disposable library, evaluate a review-only rule, inspect selected items and verify rule persistence after restart. Do not use live deletion as an onboarding test.',
        'No media server or library is bundled. Remote APIs must be reachable from Railway. File deletion or collection changes can affect connected services once explicitly enabled by the operator.'),
    'olivetin': ('OliveTin Private Action Panel', 'Automation', 'A protected command panel with two harmless starter actions.',
        'Open the gateway and try Show UTC time and Show configuration volume usage. Edit /config/config.yaml through an authenticated operator shell to add reviewed actions.',
        'Run both starter actions, verify their output, add a harmless fixed command, restart and confirm the configuration persists.',
        'Actions run inside this container only. No Docker socket, host filesystem, SSH key or remote infrastructure permission is provided. Treat changes to executable commands as privileged configuration.'),
    'go-feature-flag': ('GO Feature Flag Relay', 'Starters', 'A private feature-flag relay with a deterministic starter flag.',
        'Call the relay HTTP API with X-Template-Key carrying the gateway password. The welcome-banner flag defaults to true. Change the baked YAML in a fork and redeploy to manage flags as code.',
        'Evaluate welcome-banner via /v1/feature/welcome-banner/eval for a synthetic user, confirm true, change its default in source and confirm the redeployed value.',
        'No visual editor or mutable flag database is bundled. Native SDKs must support the owner header or use private networking. Exporters and third-party retrievers are not configured.'),
    'flagd': ('Flagd OpenFeature Starter', 'Starters', 'An OpenFeature-compatible evaluator with a private starter flag.',
        'Call /flagd.evaluation.v1.Service/ResolveBoolean with JSON containing flagKey=welcome-banner and context={}, plus X-Template-Key. Flags are baked into the image from source.',
        'Resolve the starter flag over HTTP and confirm true; verify an unknown flag produces the expected error and requests without the gateway key are rejected.',
        'Public routing uses HTTP JSON. Native gRPC clients should use the private core endpoint or a separately tested gRPC gateway. No Kubernetes operator or flag-management UI is included.'),
}


def generate():
    sources = json.loads((ROOT / 'sources.round8.lock.json').read_text())
    eligibility = json.loads((ROOT / 'eligibility.round8.json').read_text())
    metadata = {}
    for slug, (title, category, description, setup, acceptance, limitations) in DOCS.items():
        assert len(description) <= 75, (slug, len(description))
        source = sources[slug]
        services = list(configuration(slug)['services'].values())
        queries = ', '.join('`' + q['query'] + '`' for q in eligibility[slug]['queries'])
        rows = '\n'.join('| ' + s['name'] + ' | ' + ('Public HTTPS' if s['networking']['serviceDomains'] else 'Private') +
                         ' | ' + (', '.join(v['mountPath'] for v in s.get('volumeMounts', {}).values()) or 'None') + ' |'
                         for s in services)
        text = f'''# Deploy and Host {title}

{description}

**Unpublished draft.** This candidate meets the selection criterion through a public marketplace gap: no matching listing was found on September 19, 2026 using {queries}. Searches are bounded; private, unindexed and differently named listings may exist. The selection does not claim any competitor is broken.

## About Hosting

| Service | Network | Persistent mount |
| --- | --- | --- |
{rows}

The public gateway requires username **admin** and **ACCESS_PASSWORD** from the **{slug}** service. API clients can send `X-Template-Key: <ACCESS_PASSWORD>`. Keep core and databases private. The gateway strips Basic Authorization, preserves Bearer authorization and WebSocket upgrades, and limits requests to 32 MiB. Verify native client compatibility before release.

## First use

{setup}

## Recommended acceptance checks

{acceptance}

Test a volume-preserving redeploy as well as a restart. For stateful apps, take an application-consistent backup, including database/WAL and uploaded files, restore it into a separate disposable instance and verify account access and records. For configuration-as-code services, verify a clean rebuild from the saved source. Keep the original data until restoration passes.

## Scope and limitations

{limitations}

This draft has source/configuration review and static checks only. No container build, Railway startup, browser/API workflow, volume recovery or cost measurement was performed. Saved editor fidelity is not deployment proof; `/healthz` proves only gateway readiness. The template has not been published. Set operator-owned provider credentials only where needed and inspect the selected upstream license before commercial use.

## Dependencies and sources

- [Upstream project](https://github.com/{source['repo']})
- [Selected source reference]({source['releaseUrl']})
- Upstream source receipt: `{source['sha']}`.
- Images are digest-pinned in `images.round8.lock.json`. Rolling image tags are frozen at the captured digest, not asserted to match the source commit unless independently established.
- Adapters and the gateway use `orenaksakal/railway-templates`, branch `{BRANCH}`, with repository-root Docker build context. Keep the branch available.
'''
        for url in source['configurationSources'][:6]:
            text += f'- [Configuration reference]({url})\n'
        (ROOT / 'templates' / slug / 'README.md').write_text(text)
        metadata[slug] = {'name': title, 'category': category, 'description': description,
                          'image': 'https://github.com/' + source['repo'].split('/')[0] + '.png'}
    (ROOT / 'marketplace.round8.json').write_text(json.dumps(metadata, indent=2) + '\n')


if __name__ == '__main__':
    generate()
