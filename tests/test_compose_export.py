import importlib.util
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
spec = importlib.util.spec_from_file_location('compose_export', ROOT / 'scripts/export-compose.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class ComposeExportTests(unittest.TestCase):
    def test_preserves_catalog_inputs_for_every_service(self):
        for path in (ROOT / 'templates').glob('*/template.json'):
            config = json.loads(path.read_text())
            exported = module.export(config)
            services = {s['name']: s for s in config['services'].values()}
            self.assertEqual(exported['services'].keys(), services.keys())
            for name, source in services.items():
                target = exported['services'][name]
                for key, variable in source['variables'].items():
                    if 'defaultValue' in variable:
                        self.assertEqual(target['environment'][key], variable['defaultValue'])
                    else:
                        self.assertTrue(target['environment'][key].startswith('${' + key + ':?'))
                        self.assertNotEqual(target['environment'][key], '')
                if source['source'].get('image'):
                    self.assertEqual(target['image'], source['source']['image'])
                else:
                    self.assertEqual(target['build']['dockerfile'], source['build']['dockerfilePath'])
                    self.assertIn(source['source']['repo'], target['build']['context'])
                paths = [v['mountPath'] for v in source.get('volumeMounts', {}).values()]
                self.assertEqual([v.split(':', 1)[1] for v in target.get('volumes', [])], paths)
                self.assertEqual(bool(target.get('ports')), bool(source.get('networking', {}).get('serviceDomains')))


if __name__ == '__main__':
    unittest.main()
