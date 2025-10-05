"""Configuration utilities for the PD transition matrix project."""

from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Tuple


BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data"
OUTPUTS_DIR = BASE_DIR / "outputs"


@dataclass(frozen=True)
class PipelineFilters:
    """Optional selectors applied before feature engineering."""

    start_period: Optional[str] = None
    end_period: Optional[str] = None
    segments: Tuple[str, ...] = ()


@dataclass(frozen=True)
class PipelineConfig:
    """Container for pipeline paths and settings."""

    raw_data_path: Path = DATA_DIR / "raw_transition_data.csv"
    feature_store_path: Path = OUTPUTS_DIR / "packages" / "transition_features.csv"
    pd_table_path: Path = OUTPUTS_DIR / "reports" / "segment_pd_table.csv"
    filters: PipelineFilters = PipelineFilters()


DEFAULT_PIPELINE_FILTERS = PipelineFilters(start_period="2024-01-01")


pipeline_config = PipelineConfig(filters=DEFAULT_PIPELINE_FILTERS)
