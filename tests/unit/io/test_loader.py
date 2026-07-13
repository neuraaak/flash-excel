from pathlib import Path

import pytest

from flash_excel.io.loader import (
    read_csv,
    read_headers,
    read_schema,
    read_unique_values,
)


@pytest.fixture
def csv_file(tmp_path: Path) -> Path:
    path = tmp_path / "data.csv"
    path.write_text("nom;age\nAlice;30\nBob;25\nAlice;30\n", encoding="utf-8")
    return path


def test_read_csv_parses_semicolon_separated_file(csv_file):
    df = read_csv(csv_file, separator=";")
    assert df.columns == ["nom", "age"]
    assert df.shape == (3, 2)


def test_read_headers_csv_returns_column_names_only(csv_file):
    headers = read_headers(csv_file, separator=";")
    assert headers == ["nom", "age"]


def test_read_schema_csv_returns_dtype_mapping(csv_file):
    schema = read_schema(csv_file, separator=";")
    assert "nom" in schema
    assert "age" in schema


def test_read_unique_values_returns_sorted_distinct_values(csv_file):
    values = read_unique_values(csv_file, column="nom", separator=";")
    assert values == ["Alice", "Bob"]


def test_read_csv_missing_file_raises():
    with pytest.raises(FileNotFoundError):
        read_csv(Path("does/not/exist.csv"))
