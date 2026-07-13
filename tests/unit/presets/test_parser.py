from pathlib import Path

import pytest

from flash_excel.presets.parser import load_preset


def test_load_preset_valid_toml(tmp_path: Path):
    content = """
[meta]
name = "Test preset"

[[steps]]
action = "drop_columns"
columns = ["tmp"]
"""
    path = tmp_path / "preset.toml"
    path.write_text(content, encoding="utf-8")
    preset = load_preset(path)
    assert preset.meta.name == "Test preset"
    assert len(preset.steps) == 1


def test_load_preset_missing_file_raises(tmp_path: Path):
    with pytest.raises(FileNotFoundError):
        load_preset(tmp_path / "missing.toml")


def test_load_preset_invalid_toml_syntax_raises(tmp_path: Path):
    path = tmp_path / "broken.toml"
    path.write_text("this is not [valid toml", encoding="utf-8")
    with pytest.raises(ValueError, match="invalid TOML syntax"):
        load_preset(path)


def test_load_preset_schema_validation_error_raises(tmp_path: Path):
    content = """
[meta]
name = "Test preset"

[[steps]]
action = "drop_columns"
columns = []
"""
    path = tmp_path / "invalid_schema.toml"
    path.write_text(content, encoding="utf-8")
    with pytest.raises(ValueError, match="configuration errors"):
        load_preset(path)
