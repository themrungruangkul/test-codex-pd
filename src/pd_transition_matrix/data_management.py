"""Data management utilities for the PD transition matrix pipeline."""

from pathlib import Path
from typing import Any

import pandas as pd

from .config import PipelineFilters


def load_raw_data(path: Path) -> pd.DataFrame:
    """Load raw data from the provided path.

    Parameters
    ----------
    path:
        Path to the CSV file that stores raw account or loan level data.

    Returns
    -------
    pd.DataFrame
        Data frame containing the raw dataset.
    """

    if not path.exists():
        raise FileNotFoundError(f"Raw data file not found at {path}.")

    df = pd.read_csv(path)

    if "period_end" in df.columns:
        df["period_end"] = pd.to_datetime(df["period_end"], errors="coerce")

    return df


def filter_raw_data(data: pd.DataFrame, filters: PipelineFilters) -> pd.DataFrame:
    """Apply period and segment filters to the raw dataset."""

    filtered = data.copy()

    if filters.start_period:
        start = pd.to_datetime(filters.start_period, errors="raise")
        filtered = filtered[filtered["period_end"] >= start]

    if filters.end_period:
        end = pd.to_datetime(filters.end_period, errors="raise")
        filtered = filtered[filtered["period_end"] <= end]

    if filters.segments:
        filtered = filtered[filtered["segment"].isin(filters.segments)]

    return filtered.reset_index(drop=True)


def save_artifact(data: Any, path: Path) -> None:
    """Persist an artifact to disk, creating parent directories if required."""

    path.parent.mkdir(parents=True, exist_ok=True)

    if isinstance(data, pd.DataFrame):
        if path.suffix == ".csv":
            data.to_csv(path, index=False)
        elif path.suffix == ".parquet":
            data.to_parquet(path, index=False)
        else:
            raise ValueError(
                "Unsupported file extension for DataFrame persistence. "
                "Use .csv or .parquet."
            )
    else:
        raise ValueError("Unsupported artifact type. Provide a Pandas DataFrame.")
