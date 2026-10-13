# SpaceX Falcon 9 First-Stage Landing Prediction

A reproducible data-science capstone starter project for exploring SpaceX Falcon 9 launches and predicting whether the first stage lands successfully.

> **Important honesty note:** This repository is a generated project scaffold, not a claim that the analysis has already been executed. The notebooks retrieve public launch data at run time. Model metrics, charts, and conclusions should be reported only after running the workflow and inspecting the generated outputs. Do not submit unverified example numbers as measured results.

## Research question
Can launch metadata available before/around launch help estimate whether a Falcon 9 first stage will land successfully?

## Project workflow
1. Collect launch data from the public SpaceX API.
2. Clean and transform launch, rocket, payload, launchpad, and landing-outcome fields.
3. Explore launch outcomes and launch-site / orbit patterns.
4. Build a model-ready dataset and compare baseline classifiers.
5. Evaluate using a held-out test set, precision/recall/F1, confusion matrix, and ROC-AUC when defined.
6. Optionally run a small dashboard to explore launch outcomes.

## Repository structure
- `notebooks/01_data_collection.ipynb` — retrieve and flatten API data
- `notebooks/02_eda_and_sql.ipynb` — EDA, plots, and SQL examples
- `notebooks/03_modeling.ipynb` — preprocessing, model comparison, evaluation
- `src/spacex_pipeline.py` — reusable data collection and cleaning functions
- `sql/analysis_queries.sql` — starter SQL queries
- `dashboard/app.py` — optional Streamlit dashboard
- `data/` — generated CSVs are saved here when notebooks run
- `outputs/` — generated charts and metrics
- `reports/` — capstone report draft

## Setup
Python 3.10+ recommended.

```bash
python -m venv .venv
# Windows:
.venv\\Scripts\\activate
# macOS/Linux:
source .venv/bin/activate
pip install -r requirements.txt
```

Run notebooks in order from the repository root. The API calls require internet access. If the API schema changes, inspect the raw JSON and update the flattening code.

```bash
jupyter lab
```

Optional dashboard:
```bash
streamlit run dashboard/app.py
```

## Data source
SpaceX public API v4: `https://api.spacexdata.com/v4/`
Launch data is retrieved when the collection notebook/script runs. Please review SpaceX API terms and cite the data source in any submitted report.

## Methodology notes
- The target is `landing_success`, derived from the API's `cores[].landing_success` field. Unknown outcomes are excluded from supervised model training rather than automatically treated as failures.
- Avoid leakage: only use features that would reasonably be known before the landing outcome. This starter uses a limited set of metadata features; decide explicitly whether flight number / mission date are valid for your framing.
- Launch records from the same mission family or repeated sites can be correlated. A random split is a useful baseline, but a time-based split is a stronger robustness check.
- Small categories and class imbalance can make accuracy misleading. Include precision, recall, F1, confusion matrix, and the class distribution.
- Do not infer causality from exploratory plots.
