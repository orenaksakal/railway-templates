"""Guard exported draft fidelity and prevent credential-bearing CLI errors."""
import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
spec = importlib.util.spec_from_file_location('drafts', ROOT / 'scripts/create-drafts.py')
drafts = importlib.util.module_from_spec(spec)
spec.loader.exec_module(drafts)


class DraftTests(unittest.TestCase):
    def setUp(self):
        self.config = json.loads((ROOT / 'templates/formbricks/template.json').read_text())
        self.export = copy.deepcopy(self.config)
        # Railway does not preserve build settings; the variable must carry the path.
        for service in self.export['services'].values():
            service.pop('build', None)
        self.template = {'serializedConfig': self.export}

    def test_export_without_build_section_keeps_dockerfile_variable(self):
        drafts.verify_draft(self.config, self.template)

    def test_missing_dockerfile_variable_is_rejected(self):
        app = next(s for s in self.export['services'].values() if s['name'] == 'formbricks')
        del app['variables']['RAILWAY_DOCKERFILE_PATH']
        with self.assertRaisesRegex(AssertionError, 'RAILWAY_DOCKERFILE_PATH'):
            drafts.verify_draft(self.config, self.template)

    def test_missing_volume_and_changed_secret_are_rejected(self):
        app = next(s for s in self.export['services'].values() if s['name'] == 'formbricks')
        app['volumeMounts'] = {}
        with self.assertRaisesRegex(AssertionError, 'volume mounts'):
            drafts.verify_draft(self.config, self.template)
        self.setUp()
        app = next(s for s in self.export['services'].values() if s['name'] == 'formbricks')
        app['variables']['NEXTAUTH_SECRET']['defaultValue'] = 'fixed-value'
        with self.assertRaisesRegex(AssertionError, 'NEXTAUTH_SECRET'):
            drafts.verify_draft(self.config, self.template)

    def test_cli_failure_does_not_expose_variables(self):
        secret = 'sensitive-test-value'
        result = subprocess.CompletedProcess(['railway'], 1, secret, secret)
        with patch.object(drafts.subprocess, 'run', return_value=result):
            with self.assertRaises(RuntimeError) as error:
                drafts.api('mutation', {'password': secret})
        self.assertNotIn(secret, str(error.exception))


if __name__ == '__main__':
    unittest.main()
