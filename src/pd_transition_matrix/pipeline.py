"""Pipeline orchestration for the PD transition matrix service."""

import json
from pathlib import Path
from typing import Any

import joblib

from . import config
from .data_management import load_raw_data, save_artifact
from .feature_engineering import build_transition_features
from .modeling import train_transition_model


def _persist_model(model: Any, path: Path) -> None:
    """Save a trained model artifact to disk."""

    path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, path)


def _persist_report(report: dict, path: Path) -> None:
    """Serialize evaluation metrics to JSON."""

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2))


def run_pipeline() -> None:
    """Run the full PD transition matrix modeling pipeline."""

    raw_data = load_raw_data(config.pipeline_config.raw_data_path)
    features, target = build_transition_features(raw_data)
    model, report = train_transition_model(features, target)

    save_artifact(features, config.pipeline_config.feature_store_path)
    _persist_model(model, config.pipeline_config.model_path)
    _persist_report(report, config.pipeline_config.report_path)
