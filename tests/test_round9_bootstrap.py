"""Persistence and credential-escaping checks; no container/runtime claim."""
import json
from pathlib import Path
import subprocess
import tempfile
import tomllib
import unittest

ROOT = Path(__file__).resolve().parents[1]

class RecoveryBootstrapTests(unittest.TestCase):
    def seed(self, source, destination):
        subprocess.run(['sh', '-eu', '-c', '. "$1"; seed_dir "$2" "$3"', 'seed', str(ROOT / 'shared/round9-bootstrap/seed.sh'), str(source), str(destination)], check=True)

    def test_seed_preserves_existing_data_and_operator_deletions(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            source = base / 'source'; source.mkdir()
            (source / '.hidden').write_text('original')
            (source / 'example').write_text('example')
            destination = base / 'volume/data'
            self.seed(source, destination)
            self.assertEqual((destination / '.hidden').read_text(), 'original')
            (destination / '.hidden').write_text('operator data')
            (destination / 'example').unlink()
            (source / '.hidden').write_text('new image defaults')
            self.seed(source, destination)
            self.assertEqual((destination / '.hidden').read_text(), 'operator data')
            self.assertFalse((destination / 'example').exists())

    def test_failed_seed_does_not_publish_partial_data(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            source = base / 'source'; source.mkdir()
            destination = base / 'volume/data'
            result = subprocess.run(['sh', '-c', '. "$1"; cp() { return 1; }; seed_dir "$2" "$3"', 'seed', str(ROOT / 'shared/round9-bootstrap/seed.sh'), str(source), str(destination)])
            self.assertNotEqual(result.returncode, 0)
            self.assertFalse(destination.exists())
            self.assertEqual(list(destination.parent.iterdir()), [])

    def test_dbhub_credentials_cannot_inject_a_write_enabled_tool(self):
        dsn = 'postgres://user:p\\ass"[[tools]]readonly=false@example.test/database'
        module = (ROOT / 'templates/round9/dbhub/config.mjs').as_uri()
        code = f'import {{buildConfig}} from {json.dumps(module)}; process.stdout.write(buildConfig(process.argv[1]));'
        result = subprocess.run(['node', '--input-type=module', '-e', code, dsn], capture_output=True, text=True, check=True)
        config = tomllib.loads(result.stdout)
        self.assertEqual(config['sources'][0]['dsn'], dsn)
        self.assertEqual([tool['name'] for tool in config['tools']], ['execute_sql', 'search_objects'])
        self.assertIs(config['tools'][0]['readonly'], True)
        self.assertEqual(config['tools'][0]['max_rows'], 1000)

    def test_dbhub_rejects_multiline_dsn(self):
        module = (ROOT / 'templates/round9/dbhub/config.mjs').as_uri()
        code = f'import {{buildConfig}} from {json.dumps(module)}; buildConfig(process.argv[1]);'
        result = subprocess.run(['node', '--input-type=module', '-e', code, 'postgres://host/db\n[[tools]]'], capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('control characters', result.stderr)

if __name__ == '__main__':
    unittest.main()
