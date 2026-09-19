"""Update the 18 recovered drafts in place; never create or publish templates."""
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('editor', ROOT / 'scripts/create-editor-drafts-round8.py')
editor = importlib.util.module_from_spec(spec)
spec.loader.exec_module(editor)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verify-only', action='store_true')
    args = parser.parse_args()
    os.umask(0o077)
    root = ROOT / '.local/round9'
    receipt_path = root / 'drafts.json'
    receipts = json.loads(receipt_path.read_text())
    metadata = json.loads((ROOT / 'marketplace.round9.json').read_text())
    assert len(receipts) == 18 and set(receipts) == set(metadata)
    assert len({r['templateId'] for r in receipts.values()}) == 18
    subprocess.run(['railway', 'api', 'query { __typename }', '--compact'], check=True, stdout=subprocess.DEVNULL)
    prepared = {}
    def save():
        tmp = receipt_path.with_suffix('.tmp')
        tmp.write_text(json.dumps(receipts, indent=2) + '\n')
        tmp.replace(receipt_path)
    for slug, receipt in receipts.items():
        assert receipt['workspaceId'] == '09c4d797-8af5-493b-bf8a-558cadc39cfc'
        config = json.loads((ROOT / 'templates/round9' / slug / 'template.json').read_text())
        meta = {**metadata[slug], 'readme': (ROOT / 'templates/round9' / slug / 'README.md').read_text()}
        live = editor.api(editor.READ, {'id': receipt['templateId']})['template']
        if live['status'] != 'UNPUBLISHED':
            raise RuntimeError(slug + ': refusing to modify a published template')
        actual = live['serializedConfig']
        if isinstance(actual, str):
            actual = json.loads(actual)
        if not args.verify_only:
            before = json.loads((root / (receipt['templateId'] + '.json')).read_text())
            original = before['serializedConfig']
            if isinstance(original, str):
                original = json.loads(original)
            if editor.normalized_config(actual) not in [editor.normalized_config(original), editor.normalized_config(config)]:
                raise RuntimeError(slug + ': unexpected concurrent configuration change')
            for key in meta:
                if live.get(key) not in (before.get(key), meta[key]):
                    raise RuntimeError(slug + ': unexpected concurrent metadata change: ' + key)
        prepared[slug] = (config, meta, actual, live)
    print('PASS: preflight 18 existing unpublished draft IDs; duplicates excluded', flush=True)
    for slug, (config, meta, actual, live) in prepared.items():
        receipt = receipts[slug]
        if editor.normalized_config(actual) != editor.normalized_config(config) or any(live.get(k) != v for k, v in meta.items()):
            if args.verify_only:
                raise RuntimeError(slug + ': draft does not match local release files')
            patch = editor.configuration_patch(config, actual)
            staged = editor.api('mutation($templateId:String!,$patch:TemplatePatch!,$merge:Boolean){templateChangeSetStage(templateId:$templateId,patch:$patch,merge:$merge){id status}}', {'templateId': receipt['templateId'], 'patch': {'config': patch, 'metadata': meta}, 'merge': False})['templateChangeSetStage']
            applied = editor.api('mutation($changeSetId:String!){templateChangeSetApply(changeSetId:$changeSetId){id status}}', {'changeSetId': staged['id']})['templateChangeSetApply']
            if applied['status'] != 'APPLIED':
                raise RuntimeError(slug + ': changeset not applied')
            live = editor.api(editor.READ, {'id': receipt['templateId']})['template']
            actual = live['serializedConfig']
            if isinstance(actual, str):
                actual = json.loads(actual)
        if live['status'] != 'UNPUBLISHED' or editor.normalized_config(actual) != editor.normalized_config(config) or any(live.get(k) != v for k, v in meta.items()):
            raise RuntimeError(slug + ': saved configuration or metadata mismatch')
        (root / (slug + '-readback.json')).write_text(json.dumps(live, indent=2) + '\n')
        receipt.update(status=live['status'], verified=True, serviceCount=len(config['services']), configHash=hashlib.sha256(json.dumps(config, sort_keys=True).encode()).hexdigest())
        save()
        print(slug, 'UNPUBLISHED; full configuration and overview verified', flush=True)

if __name__ == '__main__':
    main()
