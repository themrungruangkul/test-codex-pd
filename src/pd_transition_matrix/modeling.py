"""Model training utilities for PD transition matrix models."""

from typing import Dict, Tuple

import pandas as pd
from sklearn.dummy import DummyClassifier
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split


DefaulterReport = Dict[str, Dict[str, float]]


def train_transition_model(features: pd.DataFrame, target: pd.Series) -> Tuple[DummyClassifier, DefaulterReport]:
    """Train a baseline model for PD estimation.

    A dummy classifier is used as a placeholder until a transition matrix
    implementation is provided.
    """

    if target.empty:
        raise ValueError("Target series is empty. Provide labeled training data.")

    X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)

    model = DummyClassifier(strategy="most_frequent")
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    report = classification_report(y_test, predictions, output_dict=True)

    return model, report
