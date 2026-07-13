"""Auto-mark all tests collected under tests/unit/ with the 'unit' marker."""

from __future__ import annotations

from pathlib import Path

import pytest

_THIS_DIR = Path(__file__).parent


def pytest_collection_modifyitems(items: list[pytest.Item]) -> None:
    for item in items:
        if _THIS_DIR in item.path.parents:
            item.add_marker(pytest.mark.unit)
