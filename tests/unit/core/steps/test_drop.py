import polars as pl
import pytest

from flash_excel.core.steps.drop import drop_columns


def test_drop_columns_removes_named_columns():
    df = pl.DataFrame({"a": [1], "b": [2], "tmp": [3]})
    out = drop_columns(df, columns=["tmp"])
    assert out.columns == ["a", "b"]


def test_drop_columns_missing_column_raises():
    df = pl.DataFrame({"a": [1]})
    with pytest.raises(pl.exceptions.ColumnNotFoundError):
        drop_columns(df, columns=["missing"])
