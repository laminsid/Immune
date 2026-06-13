#!/usr/bin/env python3
from pathlib import Path
import json, csv, sys
root = Path(__file__).resolve().parents[1]
required = [
    'index.html','README.md','RESEARCHER_QUICKSTART.md','LICENSE','NOTICE','CHANGELOG.md',
    'docs/RECEIPTS_HASHES_v30698.md','docs/TARGETED_GPL5175_REVIEW_MANIFEST_v30698.md',
    'docs/TIER0_BOUNDARIES_v30698.md','docs/REPLAY_DESCRIPTION_v30698.md',
    'assets/receipts/receipts_hashes_index_v30698.json','assets/receipts/receipts_hashes_index_v30698.csv',
    'assets/manifests/targeted_GPL5175_review_manifest_v30698.csv',
    'assets/manifests/gpl5175_targeted_probe_manifest_v1.source.json'
]
missing=[p for p in required if not (root/p).exists()]
if missing:
    print('MISSING:', missing)
    sys.exit(1)
# Ensure Android is excluded from lite release.
for forbidden in ['app','gradle','build.gradle.kts','settings.gradle.kts','gradlew','gradlew.bat']:
    if (root/forbidden).exists():
        print('FORBIDDEN_IN_LITE_RELEASE:', forbidden)
        sys.exit(1)
json.loads((root/'assets/receipts/receipts_hashes_index_v30698.json').read_text(encoding='utf-8'))
json.loads((root/'assets/manifests/gpl5175_targeted_probe_manifest_v1.source.json').read_text(encoding='utf-8'))
with (root/'assets/receipts/receipts_hashes_index_v30698.csv').open(newline='', encoding='utf-8') as f:
    list(csv.reader(f))
with (root/'assets/manifests/targeted_GPL5175_review_manifest_v30698.csv').open(newline='', encoding='utf-8') as f:
    list(csv.reader(f))
print('PASS GitHub interface-only lite package')
