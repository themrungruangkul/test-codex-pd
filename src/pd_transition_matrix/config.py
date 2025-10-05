"""Configuration utilities for the PD transition matrix project."""

from dataclasses import dataclass
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data"
OUTPUTS_DIR = BASE_DIR / "outputs"


@dataclass(frozen=True)
class PipelineConfig:
    """Container for pipeline paths and settings."""

    raw_data_path: Path = DATA_DIR / "raw_data.csv"
    feature_store_path: Path = OUTPUTS_DIR / "packages" / "feature_store.parquet"
    model_path: Path = OUTPUTS_DIR / "packages" / "pd_model.pkl"
    report_path: Path = OUTPUTS_DIR / "reports" / "model_report.json"


pipeline_config = PipelineConfig()
