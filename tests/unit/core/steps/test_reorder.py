import polars as pl
import pytest

from flash_excel.core.steps.reorder import reorder_columns


def test_reorder_columns_leading_first_remaining_after():
    df = pl.DataFrame({"b": [2], "a": [1], "c": [3]})
    out = reorder_columns(df, columns=["a", "b"])
    assert out.columns == ["a", "b", "c"]


def test_reorder_columns_missing_column_raises():
    df = pl.DataFrame({"a": [1]})
    with pytest.raises(pl.exceptions.ColumnNotFoundError):
        reorder_columns(df, columns=["missing"])
