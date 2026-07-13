import polars as pl
import pytest

from flash_excel.core.steps.select import select_columns


def test_select_columns_keeps_and_orders():
    df = pl.DataFrame({"a": [1], "b": [2], "c": [3]})
    out = select_columns(df, columns=["c", "a"])
    assert out.columns == ["c", "a"]


def test_select_columns_missing_column_raises():
    df = pl.DataFrame({"a": [1]})
    with pytest.raises(pl.exceptions.ColumnNotFoundError):
        select_columns(df, columns=["missing"])
