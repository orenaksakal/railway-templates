"""Publish the explicitly authorized batch; verify configuration before and after."""
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
from catalog_round8 import ROOT, CATALOG

spec=importlib.util.spec_from_file_location('editor',ROOT/'scripts/create-editor-drafts-round8.py')
editor=importlib.util.module_from_spec(spec)
spec.loader.exec_module(editor)

def main():
 parser=argparse.ArgumentParser(description=__doc__)
 parser.add_argument('--verify-only',action='store_true')
 parser.add_argument('--preflight-only',action='store_true')
 args=parser.parse_args()
 os.umask(0o077)
 path=ROOT/'.local/round8/drafts.json'
 receipts=json.loads(path.read_text())
 metadata=json.loads((ROOT/'marketplace.round8.json').read_text())
 subprocess.run(['railway','api','query { __typename }','--compact'],stdout=subprocess.DEVNULL,check=True)
 def save():
  tmp=path.with_suffix('.tmp');tmp.write_text(json.dumps(receipts,indent=2)+'\n');tmp.replace(path)
 if set(receipts)!=set(CATALOG):raise RuntimeError('Receipt catalog mismatch')
 if len({r['templateId'] for r in receipts.values()})!=20:raise RuntimeError('Duplicate template IDs')
 for slug in CATALOG:
  receipt=receipts[slug]
  if receipt['workspaceId']!='09c4d797-8af5-493b-bf8a-558cadc39cfc':raise RuntimeError(slug+': workspace mismatch')
  live=editor.api(editor.READ,{'id':receipt['templateId']})['template']
  actual=live['serializedConfig']
  if isinstance(actual,str):actual=json.loads(actual)
  config=json.loads((ROOT/'templates'/slug/'template.json').read_text())
  if editor.normalized_config(actual)!=editor.normalized_config(config):raise RuntimeError(slug+': preflight configuration mismatch')
  if live['status'] not in ('UNPUBLISHED','PUBLISHED'):raise RuntimeError(slug+': unexpected status')
  if any(live.get(k)!=v for k,v in metadata[slug].items()):raise RuntimeError(slug+': preflight identity/metadata mismatch')
 print('PASS: complete batch preflight, 20 templates / 42 services',flush=True)
 if args.preflight_only:return
 for slug in CATALOG:
  receipt=receipts[slug]
  config=json.loads((ROOT/'templates'/slug/'template.json').read_text())
  readme=ROOT/'templates'/slug/'README.md'
  expected={**metadata[slug],'readme':readme.read_text()}
  def read():
   live=editor.api(editor.READ,{'id':receipt['templateId']})['template']
   actual=live['serializedConfig']
   if isinstance(actual,str):actual=json.loads(actual)
   if editor.normalized_config(actual)!=editor.normalized_config(config):raise RuntimeError(slug+': configuration mismatch; stopped')
   return live
  live=read()
  if live['status'] not in ('UNPUBLISHED','PUBLISHED'):raise RuntimeError(slug+': unexpected status')
  if not args.verify_only and (live['status']!='PUBLISHED' or any(live.get(k)!=v for k,v in expected.items())):
   meta=metadata[slug]
   result=subprocess.run(['railway','templates','publish',receipt['templateId'],'--workspace',receipt['workspaceId'],'--category',meta['category'],'--description',meta['description'],'--image',meta['image'],'--readme-file',str(readme),'--json'],capture_output=True,text=True)
   if result.returncode:raise RuntimeError(slug+': publish failed: '+result.stderr[:1000])
   (ROOT/'.local/round8'/f'{slug}-publish.json').write_text(result.stdout)
   live=read()
  if live['status']!='PUBLISHED' or any(live.get(k)!=v for k,v in expected.items()):raise RuntimeError(slug+': publication metadata mismatch')
  receipt.update(status='PUBLISHED',verified=True,templateCode=live['code'],publicUrl='https://railway.com/deploy/'+live['code'],configHash=hashlib.sha256(json.dumps(config,sort_keys=True).encode()).hexdigest())
  (ROOT/'.local/round8'/f'{slug}-published-readback.json').write_text(json.dumps(live,indent=2)+'\n')
  save()
  print(slug,'PUBLISHED; configuration and metadata verified',receipt['publicUrl'],flush=True)

if __name__=='__main__':main()
