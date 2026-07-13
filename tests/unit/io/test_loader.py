from pathlib import Path

import polars as pl
import pytest

from flash_excel.io.loader import (
    read_csv,
    read_excel,
    read_headers,
    read_schema,
    read_unique_values,
    read_unique_values_many,
)
from flash_excel.io.writer import write_excel


@pytest.fixture
def csv_file(tmp_path: Path) -> Path:
    path = tmp_path / "data.csv"
    path.write_text("nom;age\nAlice;30\nBob;25\nAlice;30\n", encoding="utf-8")
    return path


@pytest.fixture
def xlsx_file(tmp_path: Path) -> Path:
    path = tmp_path / "data.xlsx"
    df = pl.DataFrame({"nom": ["Alice", "Bob", "Alice"], "age": [30, 25, 30]})
    write_excel(df, path)
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


def test_read_excel_returns_dataframe(xlsx_file):
    df = read_excel(xlsx_file)
    assert df.columns == ["nom", "age"]
    assert df.shape == (3, 2)


def test_read_headers_excel_returns_column_names_only(xlsx_file):
    headers = read_headers(xlsx_file)
    assert headers == ["nom", "age"]


def test_read_schema_excel_returns_dtype_mapping(xlsx_file):
    schema = read_schema(xlsx_file)
    assert "nom" in schema
    assert "age" in schema


def test_read_unique_values_excel_returns_sorted_distinct_values(xlsx_file):
    values = read_unique_values(xlsx_file, column="nom")
    assert values == ["Alice", "Bob"]


def test_read_unique_values_many_csv_returns_mapping_per_column(csv_file):
    result = read_unique_values_many(csv_file, columns=["nom", "age"])
    assert result["nom"] == ["Alice", "Bob"]
    assert result["age"] == ["25", "30"]


def test_read_unique_values_many_excel_returns_mapping_per_column(xlsx_file):
    result = read_unique_values_many(xlsx_file, columns=["nom", "age"])
    assert result["nom"] == ["Alice", "Bob"]


def test_read_unique_values_many_empty_columns_returns_empty_dict(csv_file):
    result = read_unique_values_many(csv_file, columns=[])
    assert result == {}


def test_read_unique_values_many_deduplicates_requested_columns(csv_file):
    result = read_unique_values_many(csv_file, columns=["nom", "nom"])
    assert list(result.keys()) == ["nom"]


def test_read_unique_values_many_missing_column_in_csv_raises(csv_file):
    with pytest.raises(pl.exceptions.ColumnNotFoundError):
        read_unique_values_many(csv_file, columns=["nom", "missing"])


def test_read_unique_values_many_missing_column_in_excel_returns_empty_list(xlsx_file):
    result = read_unique_values_many(xlsx_file, columns=["nom", "missing"])
    assert result["missing"] == []
