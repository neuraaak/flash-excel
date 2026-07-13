from pathlib import Path

import polars as pl
import pytest

from flash_excel.core.pipeline import run_pipeline
from flash_excel.presets.parser import load_preset


@pytest.fixture
def preset_file(tmp_path: Path) -> Path:
    content = """
[meta]
name = "Nettoyage RH"

[[steps]]
action = "rename_columns"
mapping = { salaire_brut = "salaire" }

[[steps]]
action = "filter_rows"
conditions = [{ column = "salaire", operator = "gte", value = 30000 }]
combine = "AND"

[[steps]]
action = "sort_rows"
by = ["salaire"]
descending = true
"""
    path = tmp_path / "preset.toml"
    path.write_text(content, encoding="utf-8")
    return path


def test_toml_preset_end_to_end_pipeline(preset_file):
    df = pl.DataFrame({"salaire_brut": [25000, 40000, 35000], "nom": ["A", "B", "C"]})
    preset = load_preset(preset_file)
    out = run_pipeline(df, preset)
    assert out.columns == ["salaire", "nom"]
    assert out["salaire"].to_list() == [40000, 35000]
