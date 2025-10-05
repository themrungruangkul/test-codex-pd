"""Data management utilities for the PD transition matrix pipeline."""

from pathlib import Path
from typing import Any

import pandas as pd


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

    return pd.read_csv(path)


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
