#!/usr/bin/env python3
from pathlib import Path
import json, csv, sys
root=Path(__file__).resolve().parents[1]
required=[
 'web/index.html','web/app.js','web/styles.css','web/data/research_index.json',
 'desktop/run_workbench.py','desktop/README_DESKTOP_WORKBENCH.md',
 'docs/APK_INTEGRATION_BRIDGE_v30750.md','artifacts/apk/apk_bridge_manifest_v30750.json'
]
missing=[p for p in required if not (root/p).exists()]
if missing:
    print('MISSING:', missing); sys.exit(1)
idx=json.loads((root/'web/data/research_index.json').read_text(encoding='utf-8'))
assert idx.get('release')=='v3.0.7.5-github-workbench-apk-bridge'
assert isinstance(idx.get('receipts'), list)
assert isinstance(idx.get('manifestPreview'), list)
bridge=json.loads((root/'artifacts/apk/apk_bridge_manifest_v30750.json').read_text(encoding='utf-8'))
assert bridge['apk_role']=='optional_android_runtime_harness'
print('PASS workbench package')
print('receipts:', len(idx.get('receipts',[])))
print('manifestPreview:', len(idx.get('manifestPreview',[])))
