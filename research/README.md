# Immune Error Radar — Research Pipeline v0.4

This folder is the desktop-side research bridge. The Android APK collects private local cases and runs literature discovery. These scripts are for public dataset ingestion and offline experiments.

Boundary: research only. No diagnosis, no treatment, no drug recommendation.

Recommended flow:

```bash
python3 dataset_registry_loader.py docs/DATASET_REGISTRY_v0.3.csv
python3 marker_dictionary.py
python3 unit_normalizer.py examples/sample_markers.csv
python3 immune_matrix_builder.py examples/sample_cases.csv
python3 baseline_classifier.py examples/sample_matrix.csv
python3 cross_condition_bridge.py examples/sample_matrix.csv
```

## v0.5 aging/autonomic bridge

Run:

```bash
python3 research/aging_autonomic_bridge.py research/examples/sample_cases.csv
```

This produces hypothesis-grade patterns only:
- preserved_responsiveness_candidate
- chronic_irritation_inflammaging_candidate
- weak_responsiveness_candidate
- autonomic_mast_cell_bp_competition_candidate
- mixed_or_undermeasured
