"""Feature engineering helpers for transition matrix modeling."""

from typing import Iterable

import pandas as pd


EXPECTED_COLUMNS: Iterable[str] = (
    "segment",
    "risk_bucket_start",
    "risk_bucket_end",
    "term_months",
    "exposure",
)


def build_transition_features(raw_data: pd.DataFrame) -> pd.DataFrame:
    """Aggregate raw transition observations into exposure summaries.

    The transition matrix method requires the number of accounts or exposure
    amount that moved from one risk bucket to another over a time horizon. This
    function validates the input structure and aggregates exposures by segment,
    originating risk bucket, destination bucket, and term structure.
    """

    missing_columns = [column for column in EXPECTED_COLUMNS if column not in raw_data.columns]
    if missing_columns:
        missing = ", ".join(missing_columns)
        raise ValueError(f"Raw data is missing required columns: {missing}.")

    aggregated = (
        raw_data.groupby(list(EXPECTED_COLUMNS[:-1]), dropna=False)["exposure"]
        .sum()
        .reset_index()
    )

    # Ensure deterministic ordering for downstream reporting
    aggregated.sort_values(
        by=["segment", "risk_bucket_start", "term_months", "risk_bucket_end"],
        inplace=True,
    )

    return aggregated
