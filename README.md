# PD Transition Matrix Model Service

This project scaffolds a Probability of Default (PD) modeling service that leverages the transition matrix methodology. The repository provides a production-ready structure for managing data, engineering features, computing transition matrices, and orchestrating end-to-end pipelines.

## Project Structure

```
final_template_project/
├── run.py
├── requirements.txt
├── requirements-dev.txt
├── notebooks/
├── src/pd_transition_matrix/
├── inputs/
├── data/
└── outputs/
```

## Getting Started

1. Create and activate a virtual environment.
2. Install production dependencies with `pip install -r requirements.txt`.
3. Install development tooling with `pip install -r requirements-dev.txt`.
4. Explore the provided notebooks for exploratory analysis and experimentation.
5. Execute `python run.py` to trigger the end-to-end pipeline.

## Pipeline Overview

The pipeline orchestrates the following stages:

1. Load and validate raw transition data stored in `data/raw_transition_data.csv`.
2. Aggregate exposures by segment, risk bucket, and term structure for transition-matrix analysis.
3. Derive Probability of Default (PD) term structures for each segment and originating risk bucket.
4. Persist intermediate features in `outputs/packages/transition_features.csv` and final PD tables in `outputs/reports/segment_pd_table.csv`.
5. Display the PD table in the console for rapid inspection.

## Sample Data

The repository ships with a synthetic dataset containing exposure transitions across three segments (`Retail`, `SME`, and `Corporate`). You can replace `data/raw_transition_data.csv` with institution-specific extracts that follow the same schema to run the analytics on your own portfolio.
