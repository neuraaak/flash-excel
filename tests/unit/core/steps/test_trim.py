import polars as pl
import pytest

from flash_excel.core.steps.trim import trim_whitespace


def test_trim_whitespace_strips_leading_trailing():
    df = pl.DataFrame({"nom": ["  Alice  ", "  Bob  "]})
    out = trim_whitespace(df, columns=["nom"])
    assert out["nom"].to_list() == ["Alice", "Bob"]


def test_trim_whitespace_empty_columns_returns_unchanged():
    df = pl.DataFrame({"nom": ["  Alice  "]})
    out = trim_whitespace(df, columns=[])
    assert out.equals(df)


def test_trim_whitespace_missing_column_raises():
    df = pl.DataFrame({"a": [1]})
    with pytest.raises(pl.exceptions.ColumnNotFoundError):
        trim_whitespace(df, columns=["missing"])
