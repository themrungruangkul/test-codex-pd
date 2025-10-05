"""Pipeline orchestration for the PD transition matrix service."""

from . import config
from .data_management import load_raw_data, save_artifact
from .feature_engineering import build_transition_features
from .modeling import calculate_segment_pd


def run_pipeline() -> None:
    """Execute the PD estimation workflow using the transition matrix method."""

    raw_data = load_raw_data(config.pipeline_config.raw_data_path)
    transition_features = build_transition_features(raw_data)
    pd_table = calculate_segment_pd(transition_features)

    save_artifact(transition_features, config.pipeline_config.feature_store_path)
    save_artifact(pd_table, config.pipeline_config.pd_table_path)

    # Display the resulting PD term structures to the console for quick review
    print(pd_table.to_string(index=False))
