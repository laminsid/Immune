# ImmuneErrorRadar Desktop / GitHub Workbench v3.0.7.5

This is a lightweight local browser interface for researchers. It mirrors the practical workflow of the Android UI without requiring Android Studio, APK installation, or a phone.

Run:

```bash
python3 desktop/run_workbench.py
```

Open:

```text
http://127.0.0.1:8501/web/
```

Capabilities:

- Paste a hypothesis or generated report.
- Upload reports, receipts, manifests, or notes.
- Derive report titles from hypothesis content.
- Group report history by date.
- Open, copy, download, and print report text.
- Maintain a local browser calibration ledger: killed, watchlist, data-only, not measurable, null-like, survivor.
- Inspect receipts/hashes and targeted GPL5175 manifest preview.
- Read Tier-0 and replay boundaries.
- View APK bridge notes for users who want to connect the Android harness to another project.

Boundary:

The workbench is a researcher-facing interface and index. It does not prove biology, run clinical validation, or provide medical advice. It does not replace the Kotlin engine or Gradle CI; it makes the GitHub research package usable immediately.
