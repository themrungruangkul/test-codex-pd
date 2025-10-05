"""Feature engineering helpers for transition matrix modeling."""

from typing import Tuple

import pandas as pd


def build_transition_features(raw_data: pd.DataFrame) -> Tuple[pd.DataFrame, pd.Series]:
    """Transform raw records into model-ready features and targets.

    This placeholder implementation simply returns the input frame and a dummy
    target column to demonstrate the interface expected by the pipeline.
    """

    features = raw_data.copy()
    if "target" in raw_data.columns:
        target = raw_data["target"]
    else:
        target = pd.Series(dtype="float64", name="target")

    return features, target
