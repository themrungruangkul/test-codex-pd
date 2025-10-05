"""Entrypoint for executing the PD transition matrix modeling pipeline."""

from src.pd_transition_matrix.pipeline import run_pipeline


def main() -> None:
    """Execute the configured pipeline."""
    run_pipeline()


if __name__ == "__main__":
    main()
