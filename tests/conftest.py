"""Pytest configuration helpers."""

import sys
from pathlib import Path

# Ensure the project package is importable when tests run in isolation.
PROJECT_SRC = Path(__file__).resolve().parents[1] / "src"
if str(PROJECT_SRC) not in sys.path:
    sys.path.insert(0, str(PROJECT_SRC))
