from pathlib import Path

from flash_excel.core.models import DropColumnsStep, Preset, PresetMeta
from flash_excel.presets.store import delete_preset, list_presets, save_preset


def test_list_presets_returns_sorted_toml_files(tmp_path: Path):
    (tmp_path / "b.toml").write_text("", encoding="utf-8")
    (tmp_path / "a.toml").write_text("", encoding="utf-8")
    (tmp_path / "ignore.txt").write_text("", encoding="utf-8")
    result = list_presets(tmp_path)
    assert [p.name for p in result] == ["a.toml", "b.toml"]


def test_list_presets_missing_directory_returns_empty_list(tmp_path: Path):
    result = list_presets(tmp_path / "does_not_exist")
    assert result == []


def test_save_preset_creates_parent_dirs_and_writes_file(tmp_path: Path):
    preset = Preset(
        meta=PresetMeta(name="Test"),
        steps=[DropColumnsStep(action="drop_columns", columns=["tmp"])],
    )
    path = tmp_path / "nested" / "preset.toml"
    save_preset(preset, path)
    assert path.exists()
    content = path.read_text(encoding="utf-8")
    assert "[meta]" in content
    assert "drop_columns" in content


def test_delete_preset_removes_existing_file(tmp_path: Path):
    path = tmp_path / "preset.toml"
    path.write_text("", encoding="utf-8")
    delete_preset(path)
    assert not path.exists()


def test_delete_preset_missing_file_is_noop(tmp_path: Path):
    path = tmp_path / "missing.toml"
    delete_preset(path)
    assert not path.exists()
