"""Keep source deletion normalization narrow so release mismatches fail closed."""
import importlib.util
from pathlib import Path
import sys
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
spec = importlib.util.spec_from_file_location('editor', Path(__file__).resolve().parents[1] / 'scripts/create-editor-drafts.py')
editor = importlib.util.module_from_spec(spec)
spec.loader.exec_module(editor)

class SourceNormalizationTests(unittest.TestCase):
    def test_only_null_source_fields_are_ignored(self):
        local = {'services': {'a': {'source': {'repo': 'owner/repo'}, 'variables': {'SECRET': {'defaultValue': 'generated'}}}}}
        live = {'services': {'a': {'source': {'repo': 'owner/repo', 'image': None}, 'variables': {'SECRET': {'defaultValue': 'generated'}}}}}
        self.assertEqual(editor.normalized_config(local), editor.normalized_config(live))
        live['services']['a']['variables']['SECRET']['defaultValue'] = None
        self.assertNotEqual(editor.normalized_config(local), editor.normalized_config(live))
        self.assertIn('image', live['services']['a']['source'])

if __name__ == '__main__':
    unittest.main()
