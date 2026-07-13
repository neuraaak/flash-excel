import polars as pl
import pytest

from flash_excel.core.steps.rename import rename_columns


def test_rename_columns_applies_mapping():
    df = pl.DataFrame({"old_name": [1], "other": [2]})
    out = rename_columns(df, mapping={"old_name": "new_name"})
    assert out.columns == ["new_name", "other"]


def test_rename_columns_missing_source_raises():
    df = pl.DataFrame({"a": [1]})
    with pytest.raises(pl.exceptions.ColumnNotFoundError):
        rename_columns(df, mapping={"missing": "x"})
