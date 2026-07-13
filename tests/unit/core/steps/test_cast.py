import polars as pl
import pytest

from flash_excel.core.steps.cast import cast_types


def test_cast_types_int_and_bool():
    df = pl.DataFrame({"amount": ["100", "200"], "active": [1, 0]})
    out = cast_types(df, casts={"amount": "int", "active": "bool"})
    assert out["amount"].to_list() == [100, 200]
    assert out.schema["amount"] == pl.Int64
    assert out["active"].to_list() == [True, False]


def test_cast_types_empty_casts_returns_unchanged():
    df = pl.DataFrame({"a": [1]})
    out = cast_types(df, casts={})
    assert out.equals(df)


def test_cast_types_unknown_column_raises():
    df = pl.DataFrame({"a": [1]})
    with pytest.raises(pl.exceptions.ColumnNotFoundError):
        cast_types(df, casts={"missing": "int"})


def test_cast_types_unknown_type_name_raises():
    df = pl.DataFrame({"a": ["1"]})
    with pytest.raises(KeyError):
        cast_types(df, casts={"a": "not_a_type"})
