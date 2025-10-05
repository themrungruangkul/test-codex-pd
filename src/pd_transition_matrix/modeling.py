"""Transition matrix analytics for PD estimation."""

from typing import Iterable

import pandas as pd


def calculate_segment_pd(
    transitions: pd.DataFrame,
    default_bucket: str = "Default",
    segment_column: str = "segment",
    start_bucket_column: str = "risk_bucket_start",
    end_bucket_column: str = "risk_bucket_end",
    term_column: str = "term_months",
    exposure_column: str = "exposure",
) -> pd.DataFrame:
    """Compute PD term structures from transition exposures.

    Parameters
    ----------
    transitions:
        Aggregated exposures produced by :func:`build_transition_features`.
    default_bucket:
        Label that represents the default state in the transition matrix.
    segment_column, start_bucket_column, end_bucket_column, term_column, exposure_column:
        Column names that can be overridden to support different schemas.

    Returns
    -------
    pd.DataFrame
        Table with columns ``segment``, ``risk_bucket``, ``term_structure``, and ``PD``.
    """

    required_columns: Iterable[str] = (
        segment_column,
        start_bucket_column,
        end_bucket_column,
        term_column,
        exposure_column,
    )

    missing_columns = [column for column in required_columns if column not in transitions.columns]
    if missing_columns:
        missing = ", ".join(missing_columns)
        raise ValueError(f"Transitions data is missing required columns: {missing}.")

    grouping_keys = [segment_column, start_bucket_column, term_column]

    totals = (
        transitions.groupby(grouping_keys, dropna=False)[exposure_column]
        .sum()
        .reset_index()
        .rename(columns={exposure_column: "total_exposure"})
    )

    defaults = (
        transitions[transitions[end_bucket_column] == default_bucket]
        .groupby(grouping_keys, dropna=False)[exposure_column]
        .sum()
        .reset_index()
        .rename(columns={exposure_column: "default_exposure"})
    )

    pd_table = totals.merge(defaults, on=grouping_keys, how="left").fillna({"default_exposure": 0.0})

    pd_table["PD"] = pd_table["default_exposure"] / pd_table["total_exposure"]
    pd_table["term_structure"] = pd_table[term_column].astype(str) + "M"

    final_columns = [
        segment_column,
        start_bucket_column,
        "term_structure",
        "PD",
    ]

    final = pd_table[final_columns].rename(
        columns={
            segment_column: "segment",
            start_bucket_column: "risk_bucket",
        }
    )

    final.sort_values(by=["segment", "risk_bucket", "term_structure"], inplace=True)
    final.reset_index(drop=True, inplace=True)

    return final
