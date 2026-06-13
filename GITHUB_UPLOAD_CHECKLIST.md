# GitHub Upload Checklist — v3.0.8.0

Upload **only these files** to the repository root:

```text
index.html
README.md
CHANGELOG.md
LICENSE
NOTICE
CITATION.cff
ImmuneErrorRadar_Preprint_v5_1_submission_clean.pdf
ImmuneErrorRadar_Evidence_Bundle_v3.0.8.0.zip
GITHUB_UPLOAD_CHECKLIST.md
DELETE_OLD_REPO_FILES.md
UPLOAD_MANIFEST_v3.0.8.0.json
```

Do not upload Android source for this minimal public interface.

## After upload

The repository root should look small. It should not contain `app/`, `gradle/`, `research/`, `modules/`, `desktop/`, `tools/`, `web/`, or `.github/` unless you intentionally keep a development branch.

## Recommended GitHub description

```text
Claim-bounded evidence archive and local viewer for executed ImmuneErrorRadar hypothesis stress-tests. Viewer-only; no live biomedical computation.
```

## GitHub Pages

If you enable GitHub Pages from the root branch, `index.html` can act as the public evidence viewer. It still performs only local browser-side viewing and hash verification.
