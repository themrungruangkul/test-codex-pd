# PD Transition Matrix Model Service

This repository provides a structured playground for developing a Probability of Default (PD) model that relies on the transition matrix technique.  It contains everything required to explore the data, craft features, estimate PD term structures, and package the results for stakeholders.

## Project Map

| Path | Purpose |
| --- | --- |
| `run.py` | Single entry point that wires together the end-to-end PD pipeline. |
| `requirements.txt` | Minimal runtime dependency set (pandas). |
| `requirements-dev.txt` | Developer conveniences such as linters, notebooks, and pytest. |
| `data/` | Storage for raw datasets. Ships with `raw_transition_data.csv` as an example. |
| `inputs/` | Drop-in location for auxiliary configuration files or lookup tables. |
| `outputs/` | All generated artifacts. See sub-folders for deliverables, saved features, and reports. |
| `notebooks/` | Exploratory notebooks used during discovery and experimentation. |
| `src/pd_transition_matrix/` | Python package that implements configuration, data loading, feature building, modeling, and pipeline orchestration. |
| `tests/` | Automated checks that exercise feature engineering, modeling, and the pipeline contract. |

> **Tip:** Start with `run.py` and follow the import trail into the package to understand how each module participates in the workflow.

## Data Contract

The transition matrix workflow expects the following columns in the raw dataset:

| Column | Description |
| --- | --- |
| `period_end` | Reporting snapshot date for the observed transitions (YYYY-MM-DD). |
| `segment` | Portfolio slice (e.g. `Retail`, `SME`). Drives dynamic reporting. |
| `risk_bucket_start` | Origination risk state at the beginning of the observation window. |
| `risk_bucket_end` | Risk state after the observation window. `Default` denotes credit events. |
| `term_months` | Elapsed months during which the transition occurred. |
| `exposure` | Exposure at Default (EAD) or account count used for probability weighting. |

You can replace `data/raw_transition_data.csv` with institution-specific extracts provided they meet this schema.

## Pipeline Walkthrough

1. **Configuration** – `src/pd_transition_matrix/config.py` centralises file paths through the `PipelineConfig` dataclass. Tests patch this configuration to keep execution isolated.
2. **Data Management** – `data_management.load_raw_data` enforces the data contract and safeguards against missing files. `save_artifact` persists tabular outputs to CSV or Parquet.
3. **Feature Engineering** – `feature_engineering.build_transition_features` aggregates exposures by period, segment, start/end risk buckets, and term horizon to form the transition matrix.
4. **Modeling** – `modeling.calculate_segment_pd` derives PD term structures per segment by comparing total exposure versus default exposure for each state and tenor.
5. **Orchestration** – `pipeline.run_pipeline` strings the steps together, saves intermediate/final artifacts to `outputs/`, and prints the PD table for quick inspection.

The output PD table contains the columns `segment`, `risk_bucket`, `term_structure`, and `PD`, making it simple to plug into downstream reporting layers. The latest run is also persisted to `outputs/reports/segment_pd_table.csv` so that analysts can pick up the result without rerunning the pipeline.

## Getting Started

1. **Create a virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```
2. **Install dependencies**
   ```bash
   pip install -r requirements-dev.txt
   ```
3. **Run the pipeline**
   ```bash
   python run.py
   ```
   The PD table will be displayed in the console and written to `outputs/reports/segment_pd_table.csv`.

## Working with Notebooks

The repository includes three placeholder notebooks that map to key analysis stages:

1. `01_initial_data_exploration.ipynb` – Inspect raw portfolio snapshots.
2. `02_feature_engineering_prototyping.ipynb` – Prototype feature transformations or alternative aggregation logic.
3. `03_model_selection_experiments.ipynb` – Compare PD estimation strategies or stress scenarios.

Launch JupyterLab with `jupyter lab` (once the dev dependencies are installed) to build out the analysis story.

## Testing & Quality Gates

Continuous feedback is provided through pytest.  The suite covers:

- Transition feature aggregation to guarantee consistent grouping.
- PD computation logic, ensuring segment-aware probabilities are reported.
- The pipeline contract, validating that artifacts are produced and display output is generated.

Run the full suite with:

```bash
pytest
```

Consider running `black` and `flake8` before committing changes to keep the codebase tidy:

```bash
black src tests
flake8 src tests
```

## Next Steps

- Replace the synthetic dataset with production transitions or integrate with your data warehouse ingestion process.
- Add calibration layers (e.g. smoothing, overrides) on top of the baseline PD table.
- Extend the pipeline to push outputs into BI dashboards or model monitoring systems.

Feel free to adapt the structure as your PD modeling service matures.
