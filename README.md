# AntiAmyloid-AD-LivingMeta

Anti-Amyloid Antibodies in Early Alzheimer's Disease: Living Meta-Analysis.

A single-file, offline-capable HTML dashboard (`ANTI_AMYLOID_AD_REVIEW.html`)
built on the RapidMeta engine. It pools the included trials, renders forest and
funnel plots (Plotly vendored locally under `assets/`), and reports
heterogeneity and sensitivity statistics (REML and DL tau-squared, Q-profile
I-squared CI, FE-IVW sensitivity pool). `index.html` redirects to the dashboard
for GitHub Pages.

## Run

Open `ANTI_AMYLOID_AD_REVIEW.html` in a browser, or serve the folder and visit
`index.html`.

## Smoke test

```
python -m pytest test_smoke.py -q
```

Checks structural invariants: no BOM, no hardcoded local paths, balanced
`<script>` tags, locally-vendored Plotly, and no unfilled template tokens.

_Status: Submission ready (portfolio registry)._
