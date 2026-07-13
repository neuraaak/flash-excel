from pathlib import Path

import pytest

from flash_excel.io.models import FileLoaderResult


def test_from_path_builds_metadata_for_csv(tmp_path: Path):
    path = tmp_path / "data.csv"
    path.write_text("a,b\n1,2\n", encoding="utf-8")
    result = FileLoaderResult.from_path(path)
    assert result.file_type == "csv"
    assert result.is_csv is True
    assert result.is_excel is False


def test_from_path_unsupported_extension_raises(tmp_path: Path):
    path = tmp_path / "data.txt"
    path.write_text("hello", encoding="utf-8")
    with pytest.raises(ValueError, match="Unsupported file format"):
        FileLoaderResult.from_path(path)


def test_from_path_missing_file_raises(tmp_path: Path):
    missing = tmp_path / "missing.csv"
    with pytest.raises(ValueError, match="existing file"):
        FileLoaderResult(
            path=missing,
            file_name="missing.csv",
            directory=tmp_path,
            suffix=".csv",
            size_bytes=0,
            file_type="csv",
        )
