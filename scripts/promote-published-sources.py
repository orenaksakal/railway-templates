"""Promote published template sources to main without creating deployments.

Defaults to read-only preflight. --apply requires main to have been pushed first.
Only branch references and matching README text may differ from live listings.
Full before/after receipts remain in ignored .local/source-promotion/.
"""
import argparse
import importlib.util
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('editor', ROOT / 'scripts/create-editor-drafts-round4.py')
editor = importlib.util.module_from_spec(spec)
spec.loader.exec_module(editor)


def promote(value):
    result = json.loads(json.dumps(value))
    for service in result.get('services', {}).values():
        source = service.get('source', {})
        if source.get('repo') == 'orenaksakal/railway-templates':
            if source.get('branch') not in ('main', 'codex/remaining-template-drafts', 'codex/railway-template-release'):
                raise RuntimeError('Unexpected source branch')
            source['branch'] = 'main'
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--apply', action='store_true')
    args = parser.parse_args()
    subprocess.run(['railway', 'api', 'query { __typename }', '--compact'], check=True, stdout=subprocess.DEVNULL)
    listings = {}
    for receipt in ('.local/published-listings.json', '.local/round3/published.json', '.local/round4/published.json'):
        listings.update(json.loads((ROOT / receipt).read_text()))
    if len(listings) != 25:
        raise RuntimeError('Expected exactly 25 published listings')
    receipts = ROOT / '.local/source-promotion'
    receipts.mkdir(parents=True, exist_ok=True)
    pending = []
    for name, receipt in listings.items():
        live = editor.api(editor.READ, {'id': receipt['id']})['template']
        if live['status'] != 'PUBLISHED':
            raise RuntimeError(name + ': not published')
        raw = live['serializedConfig']
        actual = json.loads(raw) if isinstance(raw, str) else raw
        expected = json.loads((ROOT / 'templates' / name / 'template.json').read_text())
        if editor.normalized_config(promote(actual)) != editor.normalized_config(expected):
            raise RuntimeError(name + ': unexpected configuration drift')
        readme = (ROOT / 'templates' / name / 'README.md').read_text()
        promoted_readme = live['readme'].replace('codex/remaining-template-drafts', 'main').replace('codex/railway-template-release', 'main')
        if promoted_readme != readme:
            raise RuntimeError(name + ': unexpected README drift')
        before = receipts / (name + '-before.json')
        if not before.exists():
            before.write_text(json.dumps(live, indent=2) + '\n')
        pending.append((name, live, actual, expected, readme))
        print(name, 'preflight passed', flush=True)
    if not args.apply:
        return
    for name, live, actual, expected, readme in pending:
        if editor.api(editor.READ, {'id': live['id']})['template'] != live:
            raise RuntimeError(name + ': listing changed after preflight; rerun')
        if editor.normalized_config(actual) != editor.normalized_config(expected) or live['readme'] != readme:
            staged = editor.api('mutation($templateId:String!,$patch:TemplatePatch!,$merge:Boolean){templateChangeSetStage(templateId:$templateId,patch:$patch,merge:$merge){id status}}', {
                'templateId': live['id'], 'patch': {'config': editor.configuration_patch(expected, actual), 'metadata': {'readme': readme}}, 'merge': False})['templateChangeSetStage']
            applied = editor.api('mutation($changeSetId:String!){templateChangeSetApply(changeSetId:$changeSetId){id status}}', {'changeSetId': staged['id']})['templateChangeSetApply']
            if applied['status'] != 'APPLIED':
                raise RuntimeError(name + ': promotion not applied')
        after = editor.api(editor.READ, {'id': live['id']})['template']
        raw = after['serializedConfig']
        config = json.loads(raw) if isinstance(raw, str) else raw
        assert after['status'] == 'PUBLISHED' and after['readme'] == readme, name
        assert editor.normalized_config(config) == editor.normalized_config(expected), name
        for key in ('id', 'code', 'name', 'category', 'description', 'image'):
            assert after[key] == live[key], (name, key)
        (receipts / (name + '-after.json')).write_text(json.dumps(after, indent=2) + '\n')
        print(name, 'PUBLISHED: main source and metadata verified', flush=True)


if __name__ == '__main__':
    main()
