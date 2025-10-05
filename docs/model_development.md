# PD Transition Matrix Model Development Narrative

## Objective and Scope
This document records the end-to-end development workflow for the sample Probability of Default (PD) service delivered in this repository. It explains the modeling assumptions, data handling decisions, and validation checks so that readers can quickly understand how the transition-matrix approach operates and how to extend it.

## Data Sources and Preparation
- **Primary dataset:** `data/raw_transition_data.csv` contains synthetic exposures observed across multiple reporting `period_end` dates, portfolio `segment`s, originating `risk_bucket_start`, ending `risk_bucket_end`, and the `term_months` horizon over which the transition occurred. Exposure values act as weights when computing probabilities.
- **Loader responsibilities:** `src/pd_transition_matrix/data_management.py` enforces the data contract (columns, dtypes) through `load_raw_data`. `filter_raw_data` then applies configuration-driven guards—such as restricting to post-2024 observations or a subset of segments—so exploratory work mirrors production safeguards.
- **Artifact persistence:** `save_artifact` centralises saving CSV/Parquet outputs to `outputs/` and is reused by the pipeline to persist intermediate features and final PD tables.

## Exploratory Analysis
Notebook `notebooks/01_initial_data_exploration.ipynb` inspects the raw timeline and segment mix to build intuition around volume, migration patterns, and default rates. Subsequent notebooks progressively prototype feature transformations and scenario experiments:
1. `02_feature_engineering_prototyping.ipynb` – experiments with different grouping levels or smoothing strategies.
2. `03_model_selection_experiments.ipynb` – benchmarks transition-matrix PDs against alternative estimators or stress tests.

These notebooks consume the same loader utilities to ensure parity between exploratory work and the production pipeline.

## Feature Engineering Methodology
`build_transition_features` in `src/pd_transition_matrix/feature_engineering.py` aggregates exposures into a transition matrix for each `period_end`, `segment`, `risk_bucket_start`, `risk_bucket_end`, and `term_months`. Key design points:
- **Dynamic segmentation:** The function groups by `segment`, enabling any number of portfolio slices to flow through without code changes.
- **Timeline awareness:** Retaining `period_end` supports term-structure comparisons over time and allows future back-testing.
- **Exposure preservation:** Both total and default exposures are calculated, providing the numerator and denominator required for PD estimation.

The resulting feature table is saved to `outputs/packages/transition_features.csv` for traceability.

## PD Estimation Approach
The transition-based modeling logic lives in `src/pd_transition_matrix/modeling.py` and revolves around `calculate_segment_pd`:
1. **Default identification:** Rows where `risk_bucket_end == "Default"` are tagged as credit events for each segment/bucket/term.
2. **Probability calculation:** PDs are calculated as `default_exposure / total_exposure` for each combination of `segment`, `risk_bucket_start` (reported as `risk_bucket`), and `term_months` (reported as `term_structure`). This preserves the dynamic segmentation requirement—new segments in the raw data automatically flow to the output table.
3. **Term structure presentation:** Results are sorted by segment and ascending term to create an intuitive PD curve.

The model produces the consolidated table stored at `outputs/reports/segment_pd_table.csv`, which contains the required columns: `segment`, `risk_bucket`, `term_structure`, and `PD`.

## Pipeline Orchestration
`src/pd_transition_matrix/pipeline.py` defines `run_pipeline`, which wires together configuration, loading, filtering, feature engineering, modeling, and artifact persistence. The top-level script `run.py` calls this function, prints the PD table for quick review, and returns the DataFrame for programmatic reuse. Because the configuration is encapsulated in `PipelineConfig`, swapping data sources, adjusting filters, or redirecting outputs requires minimal edits.

## Validation and Quality Controls
Automated tests in the `tests/` package provide regression coverage:
- `test_feature_engineering.py` checks grouping logic, exposure totals, and timeline preservation.
- `test_modeling.py` verifies PD calculations, dynamic segment handling, and graceful behaviour when no defaults occur.
- `test_pipeline.py` ensures the orchestrated run produces both feature and PD artifacts in the expected locations.

Running `pytest` before committing changes confirms the analytical pipeline remains sound.

## Reproducibility and Extension Guidelines
- **Configuration-first:** Keep file paths and tunable parameters inside `PipelineConfig` to avoid hard-coded values scattered across modules.
- **Notebook-to-production parity:** Prototype transformations with the helper functions used by the pipeline to minimise translation effort.
- **Version control of outputs:** Checked-in sample artifacts demonstrate expected shapes; regenerate them after materially changing logic so readers can compare before/after behaviour.
- **Future enhancements:** Consider incorporating calibration layers (e.g., smoothing transition rates, blending expert overrides) or integrating macroeconomic adjustments. Monitoring hooks can be added by extending the pipeline to log metrics per run.

By following this workflow, practitioners can understand the methodology behind the PD transition matrix model, audit intermediate steps, and build confidence in extending the solution to real-world data.
