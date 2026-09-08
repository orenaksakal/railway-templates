# Ten additional Railway templates

This batch contains 49 services across ten community integrations. Release and publication were authorized September 7, 2026. Current evidence and marketplace links are in [RELEASE_VALIDATION.md](RELEASE_VALIDATION.md). Each product README documents setup, dependencies, persistence, tested workflows and limitations.

## Reproduce static validation

```sh
python3 scripts/catalog_round3.py
python3 scripts/validate-round3.py
python3 scripts/create-editor-drafts.py --workspace YOUR_WORKSPACE_ID --verify-only
python3 scripts/validate.py
python3 -m unittest discover -s tests -p 'test_*.py'
node --test tests/*.test.mjs
```

The additional catalog uses `codex/remaining-template-drafts` and `images.round3.lock.json`. It does not regenerate the original five templates. Repository-backed adapters build from this branch; retain it for deployed consumers. `marketplace.round3.json` and each README are the listing sources. The editor tool creates/updates unpublished templates and can verify published templates without changing them.

Images and application revisions are pinned. Large images were built/tested on Railway rather than pulled locally. Static checks establish configuration consistency; live workflow evidence is separately recorded. AppFlowy requires the operator's GoTrue administrator email and is subject to upstream license limits. Matrix requires a deliberate server-name/domain choice before first use. No Docker-socket executor, GPU service or TURN infrastructure is supplied.

Local Compose generation remains available through `scripts/prepare-local.py`; it is not a substitute for the Railway validation record. Secrets and receipts stay in ignored `.local/`.
