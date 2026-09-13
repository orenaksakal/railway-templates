"""Failure-path tests for credential validation and persistent-site migration gates."""
import importlib.util
import os
from pathlib import Path
import runpy
import sys
import tempfile
import types
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]

class TimeTaggerCredentials(unittest.TestCase):
    def run_adapter(self, username, password):
        bcrypt = types.SimpleNamespace(hashpw=lambda *_: b'$2b$test-hash', gensalt=lambda: b'salt')
        with patch.dict(sys.modules, {'bcrypt': bcrypt}), patch.dict(os.environ, {'ADMIN_USERNAME': username, 'ADMIN_PASSWORD': password}, clear=True), patch('os.execvp') as execute:
            runpy.run_path(str(ROOT/'templates/timetagger/start.py'))
            return os.environ.get('TIMETAGGER_CREDENTIALS'), execute.call_args

    def test_valid_credentials_launch_native_app_with_hash(self):
        credential, call = self.run_adapter('owner', 'a'*40)
        self.assertEqual(credential, 'owner:$2b$test-hash')
        self.assertEqual(call.args, ('python', ['python', '-m', 'timetagger']))

    def test_rejects_credential_delimiters_and_bcrypt_truncation(self):
        for user, password in [('owner:admin', 'a'*40), ('owner', 'short'), ('owner', 'a'*73), ('owner', 'é'*40)]:
            with self.subTest(user=user, size=len(password.encode())), self.assertRaises(SystemExit):
                self.run_adapter(user, password)

class FrappeMigrationGate(unittest.TestCase):
    def test_existing_site_never_migrates_without_explicit_flag(self):
        spec = importlib.util.spec_from_file_location('round6_frappe', ROOT/'shared/round6-frappe/start.py')
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        with tempfile.TemporaryDirectory() as directory:
            data = Path(directory)
            site = data/'site.localhost'
            site.mkdir()
            (site/'site_config.json').write_text('{}')
            (data/'.template-release').write_text('previous-release')
            env = {'FRAPPE_APP':'lms', 'PUBLIC_URL':'https://example.test', 'DB_HOST':'private-db', 'REDIS_URL':'redis://private-cache:6379', 'TEMPLATE_RELEASE':'next-release', 'ALLOW_MIGRATION':'false'}
            with patch.object(module, 'DATA', data), patch.dict(os.environ, env), patch.object(module.socket, 'create_connection'), patch.object(module, 'run') as run:
                with self.assertRaisesRegex(SystemExit, 'Back up database'):
                    module.main()
                run.assert_not_called()
                self.assertEqual((data/'.template-release').read_text(), 'previous-release')
                self.assertEqual((site/'site_config.json').read_text(), '{}')

if __name__=='__main__':unittest.main()
