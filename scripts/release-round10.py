"""Create, publish and verify only the authorized fifteen-template batch.

No application projects or deployments are created. Private receipts allow
resuming publication without duplicating successfully created drafts.
"""
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = '09c4d797-8af5-493b-bf8a-558cadc39cfc'
BRANCH = 'codex/unique-template-drafts'
spec = importlib.util.spec_from_file_location('editor', ROOT / 'scripts/create-editor-drafts-round8.py')
editor = importlib.util.module_from_spec(spec)
spec.loader.exec_module(editor)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--draft-only', action='store_true')
    parser.add_argument('--verify-only', action='store_true')
    args = parser.parse_args()
    os.umask(0o077)
    subprocess.run(['python3', str(ROOT / 'scripts/validate-round10.py')], check=True)
    meta = json.loads((ROOT / 'marketplace.round10.json').read_text())
    out = ROOT / '.local/round10'
    out.mkdir(parents=True, exist_ok=True)
    path = out / 'drafts.json'
    receipts = json.loads(path.read_text()) if path.exists() else {}
    if set(receipts) - set(meta):
        raise RuntimeError('Unexpected template in release receipts')

    def save():
        tmp = path.with_suffix('.tmp')
        tmp.write_text(json.dumps(receipts, indent=2) + '\n')
        tmp.replace(path)

    def inventory():
        result = subprocess.run(['railway', 'templates', 'list', '--workspace', WORKSPACE, '--json'],
                                check=True, capture_output=True, text=True)
        return json.loads(result.stdout)

    subprocess.run(['railway', 'api', 'query { __typename }', '--compact'],
                   stdout=subprocess.DEVNULL, check=True)
    before_path = out / 'before.json'
    if not before_path.exists():
        before = inventory()
        if len(before) != 85 or any(t['status'] != 'PUBLISHED' for t in before):
            raise RuntimeError('Expected starting inventory of exactly 85 published templates')
        before_path.write_text(json.dumps(before, indent=2) + '\n')
    before = json.loads(before_path.read_text())
    protected_ids = {t['id'] for t in before}
    current = inventory()
    known_ids = protected_ids | {r['templateId'] for r in receipts.values()}
    unexpected = [t for t in current if t['id'] not in known_ids]
    if unexpected:
        # A create request can succeed while its response is lost. Stop before
        # creating more drafts; inspect the unexpected IDs and recover an exact
        # matching receipt rather than silently creating a duplicate.
        (out / 'unexpected-inventory.json').write_text(json.dumps(unexpected, indent=2) + '\n')
        raise RuntimeError('Unrecorded templates found; reconcile private unexpected-inventory.json before resuming')
    if not protected_ids <= {t['id'] for t in current if t['status'] == 'PUBLISHED'}:
        raise RuntimeError('An original published template is missing or changed status')
    source_commit = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
    remote = subprocess.check_output(['git', 'ls-remote', 'origin', 'refs/heads/' + BRANCH], cwd=ROOT, text=True).split()
    if not remote or source_commit != remote[0]:
        raise RuntimeError('Current source commit must be pushed before publishing')
    release_paths = ['scripts/assemble-round10.py', 'scripts/validate-round10.py',
                     'scripts/release-round10.py', 'templates/round10',
                     'marketplace.round10.json', 'eligibility.round10.json',
                     'images.round10.lock.json', 'sources.round10.lock.json']
    release_paths += ['shared/round10-gateway', 'tests/round10-gateway.test.py']
    release_paths += [str(p.relative_to(ROOT)) for pattern in ('*round10-*.json', 'scripts/catalog_round10_*.py') for p in ROOT.glob(pattern)]
    dirty = subprocess.check_output(['git', 'status', '--porcelain', '--', *release_paths], cwd=ROOT, text=True)
    if dirty:
        raise RuntimeError('Release inputs must be committed before publishing')
    desired = {}
    for slug, m in meta.items():
        folder = ROOT / 'templates/round10' / slug
        config = json.loads((folder / 'template.json').read_text())
        expected = {**m, 'readme': (folder / 'README.md').read_text()}
        desired[slug] = (config, expected)
        if slug not in receipts:
            if args.verify_only:
                raise RuntimeError(slug + ': missing receipt')
            created = editor.api('mutation($input:TemplateCreateV2Input!){templateCreateV2(input:$input){id code status}}',
                                 {'input': {'metadata': expected, 'serializedConfig': config, 'workspaceId': WORKSPACE}})['templateCreateV2']
            receipts[slug] = {'templateId': created['id'], 'workspaceId': WORKSPACE,
                              'verified': False, 'sourceCommit': source_commit}
            save()
        r = receipts[slug]
        if r['workspaceId'] != WORKSPACE or r['templateId'] in protected_ids:
            raise RuntimeError(slug + ': identity mismatch')
        if len({v['templateId'] for v in receipts.values()}) != len(receipts):
            raise RuntimeError('Duplicate template IDs')
        live = editor.api(editor.READ, {'id': r['templateId']})['template']
        actual = live['serializedConfig']
        if isinstance(actual, str):
            actual = json.loads(actual)
        if editor.normalized_config(actual) != editor.normalized_config(config) or any(live.get(k) != v for k, v in expected.items()):
            raise RuntimeError(slug + ': saved configuration or metadata mismatch')
        if live['status'] not in ('PUBLISHED', 'UNPUBLISHED'):
            raise RuntimeError(slug + ': unexpected state')
        (out / (slug + '-readback.json')).write_text(json.dumps(live, indent=2) + '\n')
        r.update(status=live['status'], name=live['name'], templateCode=live['code'], verified=True)
        save()
        print(slug + ': saved configuration and metadata verified', flush=True)
    if args.draft_only:
        return
    for slug, (config, expected) in desired.items():
        r = receipts[slug]
        if r['status'] != 'PUBLISHED' and not args.verify_only:
            m = meta[slug]
            result = subprocess.run(['railway', 'templates', 'publish', r['templateId'], '--workspace', WORKSPACE,
                                     '--category', m['category'], '--description', m['description'], '--image', m['image'],
                                     '--readme-file', str(ROOT / 'templates/round10' / slug / 'README.md'), '--json'],
                                    capture_output=True, text=True)
            (out / (slug + '-publish.json')).write_text(json.dumps({'returncode': result.returncode, 'stdout': result.stdout, 'stderr': result.stderr}))
            if result.returncode:
                raise RuntimeError(slug + ': publish failed; see private receipt')
        live = editor.api(editor.READ, {'id': r['templateId']})['template']
        actual = live['serializedConfig']
        if isinstance(actual, str):
            actual = json.loads(actual)
        if live['status'] != 'PUBLISHED' or editor.normalized_config(actual) != editor.normalized_config(config) or any(live.get(k) != v for k, v in expected.items()):
            raise RuntimeError(slug + ': final publication verification failed')
        r.update(status='PUBLISHED', verified=True, templateCode=live['code'], publicUrl='https://railway.com/deploy/' + live['code'],
                 configHash=hashlib.sha256(json.dumps(config, sort_keys=True).encode()).hexdigest())
        (out / (slug + '-published-readback.json')).write_text(json.dumps(live, indent=2) + '\n')
        save()
        print(slug + ': PUBLISHED ' + r['publicUrl'], flush=True)
    after = inventory()
    (out / 'after.json').write_text(json.dumps(after, indent=2) + '\n')
    expected_ids = protected_ids | {r['templateId'] for r in receipts.values()}
    if len(after) != 100 or {t['id'] for t in after} != expected_ids or any(t['status'] != 'PUBLISHED' for t in after):
        raise RuntimeError('Final inventory did not match 100 published templates')
    by_id = {t['id']: t for t in after}
    if any(by_id[t['id']] != t for t in before):
        raise RuntimeError('An existing template inventory record changed; inspect receipts')
    public_checks = {}
    for slug, r in receipts.items():
        request = urllib.request.Request(r['publicUrl'], headers={'User-Agent': 'Railway-template-publication-check'})
        with urllib.request.urlopen(request, timeout=30) as response:
            body = response.read().decode('utf-8')
            if response.status != 200 or r['name'] not in body:
                raise RuntimeError(slug + ': public page verification failed')
            public_checks[slug] = {'url': r['publicUrl'], 'status': response.status,
                                   'nameFound': True, 'sha256': hashlib.sha256(body.encode()).hexdigest()}
    (out / 'public-pages.json').write_text(json.dumps(public_checks, indent=2) + '\n')
    print('PASS: all fifteen public listing pages return HTTP 200 and contain the expected name.', flush=True)
    print('VERIFIED: 100 published templates; 0 unpublished; original 85 inventory records unchanged.', flush=True)


if __name__ == '__main__':
    main()
