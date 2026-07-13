import polars as pl
import pytest

from flash_excel.core.steps.sort import sort_rows


def test_sort_rows_descending_single_column():
    df = pl.DataFrame({"salaire": [50000, 30000, 40000]})
    out = sort_rows(df, by=["salaire"], descending=True)
    assert out["salaire"].to_list() == [50000, 40000, 30000]


def test_sort_rows_ascending_default():
    df = pl.DataFrame({"salaire": [30000, 50000, 40000]})
    out = sort_rows(df, by=["salaire"])
    assert out["salaire"].to_list() == [30000, 40000, 50000]


def test_sort_rows_missing_column_raises():
    df = pl.DataFrame({"a": [1]})
    with pytest.raises(pl.exceptions.ColumnNotFoundError):
        sort_rows(df, by=["missing"])
