"""Resolve image tags without pulling layers. Review and commit lock changes."""
import json
import re
import subprocess
from catalog import ROOT

path = ROOT / 'images.lock.json'
lock = json.loads(path.read_text()) if path.exists() else {}
images = set()
for config in (ROOT / 'templates').glob('*/template.json'):
    for service in json.loads(config.read_text())['services'].values():
        if service['source'].get('image'):
            images.add(service['source']['image'])
dockerfiles = list((ROOT / 'templates').rglob('*Dockerfile'))
for dockerfile in dockerfiles:
    images.update(re.findall(r'^FROM ([^\s]+)', dockerfile.read_text(), re.M))
for image in sorted(images):
    if '@sha256:' in image or '$' in image:
        continue
    digest = subprocess.check_output(['docker', 'buildx', 'imagetools', 'inspect', image, '--format', '{{.Manifest.Digest}}'], text=True).strip()
    if not re.fullmatch(r'sha256:[a-f0-9]{64}', digest):
        raise SystemExit(f'Invalid digest for {image}')
    lock[image] = image + '@' + digest
    print(image, digest)
path.write_text(json.dumps(lock, indent=2, sort_keys=True) + '\n')
for dockerfile in dockerfiles:
    text = dockerfile.read_text()
    text = re.sub(r'^FROM ([^\s]+)', lambda m: 'FROM ' + lock.get(m[1], m[1]), text, flags=re.M)
    dockerfile.write_text(text)
