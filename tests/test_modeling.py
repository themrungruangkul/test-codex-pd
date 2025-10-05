"""Tests for PD calculation utilities."""

import pandas as pd
import pytest

from src.pd_transition_matrix.modeling import calculate_segment_pd


def _sample_transitions() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "period_end": "2023-12-31",
                "segment": "Retail",
                "risk_bucket_start": "A",
                "risk_bucket_end": "Default",
                "term_months": 12,
                "exposure": 2,
            },
            {
                "period_end": "2023-12-31",
                "segment": "Retail",
                "risk_bucket_start": "A",
                "risk_bucket_end": "B",
                "term_months": 12,
                "exposure": 8,
            },
            {
                "period_end": "2024-06-30",
                "segment": "Retail",
                "risk_bucket_start": "B",
                "risk_bucket_end": "Default",
                "term_months": 12,
                "exposure": 1,
            },
            {
                "period_end": "2024-06-30",
                "segment": "Retail",
                "risk_bucket_start": "B",
                "risk_bucket_end": "C",
                "term_months": 12,
                "exposure": 9,
            },
            {
                "period_end": "2024-06-30",
                "segment": "SME",
                "risk_bucket_start": "BB",
                "risk_bucket_end": "Default",
                "term_months": 6,
                "exposure": 3,
            },
            {
                "period_end": "2024-06-30",
                "segment": "SME",
                "risk_bucket_start": "BB",
                "risk_bucket_end": "BBB",
                "term_months": 6,
                "exposure": 7,
            },
        ]
    )


def test_calculate_segment_pd_returns_expected_probabilities() -> None:
    """Default exposure divided by total exposure yields PD per segment and bucket."""

    pd_table = calculate_segment_pd(_sample_transitions())

    assert list(pd_table.columns) == ["segment", "risk_bucket", "term_structure", "PD"]
    retail_a = pd_table[(pd_table["segment"] == "Retail") & (pd_table["risk_bucket"] == "A")]
    assert retail_a["PD"].iloc[0] == pytest.approx(0.2)

    sme_bb = pd_table[(pd_table["segment"] == "SME") & (pd_table["risk_bucket"] == "BB")]
    assert sme_bb["PD"].iloc[0] == pytest.approx(0.3)


def test_calculate_segment_pd_validates_input_columns() -> None:
    transitions = _sample_transitions().drop(columns=["segment"])

    with pytest.raises(ValueError, match="Transitions data is missing required columns"):
        calculate_segment_pd(transitions)
