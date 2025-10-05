# PD Transition Matrix Model Service

This project scaffolds a Probability of Default (PD) modeling service that leverages the transition matrix methodology. The repository provides a production-ready structure for managing data, engineering features, training models, and orchestrating end-to-end pipelines.

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

1. Load and validate raw data assets.
2. Engineer features required for transition matrix computation.
3. Train and evaluate PD models based on transition probabilities.
4. Persist artifacts and reports inside the `outputs/` directory hierarchy.

## Next Steps

Populate the data management, feature engineering, and modeling modules with domain-specific logic to implement the transition matrix workflow for PD modeling.
