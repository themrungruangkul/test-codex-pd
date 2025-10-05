"""Tests for transition feature engineering utilities."""

import pandas as pd
import pytest

from src.pd_transition_matrix.feature_engineering import build_transition_features


def test_build_transition_features_aggregates_exposure() -> None:
    """Rows with the same grouping keys should be summed into one record."""

    raw = pd.DataFrame(
        [
            {"segment": "Retail", "risk_bucket_start": "A", "risk_bucket_end": "B", "term_months": 12, "exposure": 10},
            {"segment": "Retail", "risk_bucket_start": "A", "risk_bucket_end": "B", "term_months": 12, "exposure": 5},
            {"segment": "Retail", "risk_bucket_start": "A", "risk_bucket_end": "C", "term_months": 12, "exposure": 8},
            {"segment": "SME", "risk_bucket_start": "BB", "risk_bucket_end": "Default", "term_months": 6, "exposure": 2},
        ]
    )

    features = build_transition_features(raw)

    assert list(features.columns) == [
        "segment",
        "risk_bucket_start",
        "risk_bucket_end",
        "term_months",
        "exposure",
    ]
    # Aggregation check: the duplicated observation should be summed to 15
    retail_ab = features[features["risk_bucket_end"] == "B"]["exposure"].iloc[0]
    assert retail_ab == pytest.approx(15)


def test_build_transition_features_validates_schema() -> None:
    """Missing columns should raise an informative error."""

    raw = pd.DataFrame(
        [
            {"segment": "Retail", "risk_bucket_start": "A", "term_months": 12, "exposure": 10},
        ]
    )

    with pytest.raises(ValueError, match="Raw data is missing required columns"):
        build_transition_features(raw)
