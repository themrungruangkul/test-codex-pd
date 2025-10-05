"""Integration test for the PD pipeline."""

from dataclasses import replace

import pandas as pd

from src.pd_transition_matrix import config
from src.pd_transition_matrix.pipeline import run_pipeline


def test_run_pipeline_produces_outputs(tmp_path, monkeypatch, capsys) -> None:
    """Pipeline should consume raw data, persist artifacts, and print the PD table."""

    raw_path = tmp_path / "raw.csv"
    pd.DataFrame(
        [
            {
                "period_end": "2024-06-30",
                "segment": "Corporate",
                "risk_bucket_start": "A",
                "risk_bucket_end": "Default",
                "term_months": 12,
                "exposure": 4,
            },
            {
                "period_end": "2024-06-30",
                "segment": "Corporate",
                "risk_bucket_start": "A",
                "risk_bucket_end": "AA",
                "term_months": 12,
                "exposure": 6,
            },
        ]
    ).to_csv(raw_path, index=False)

    feature_store = tmp_path / "packages" / "features.csv"
    pd_table_path = tmp_path / "reports" / "pd.csv"

    monkeypatch.setattr(
        config,
        "pipeline_config",
        replace(
            config.pipeline_config,
            raw_data_path=raw_path,
            feature_store_path=feature_store,
            pd_table_path=pd_table_path,
        ),
    )

    run_pipeline()

    captured = capsys.readouterr()
    assert "Corporate" in captured.out
    assert feature_store.exists()
    assert pd_table_path.exists()

    pd_table = pd.read_csv(pd_table_path)
    assert list(pd_table.columns) == ["segment", "risk_bucket", "term_structure", "PD"]
    assert pd_table["PD"].iloc[0] == 0.4
