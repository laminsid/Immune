# GitHub Web Workbench

`web/index.html` is a static research interface suitable for GitHub Pages or local serving.

Recommended local mode:

```bash
python3 desktop/run_workbench.py
```

GitHub Pages mode:

- Serve the repository root or the `web/` folder.
- The workbench reads `web/data/research_index.json`.
- If browser restrictions block local `fetch()`, use the Python local server rather than opening the HTML file directly.
