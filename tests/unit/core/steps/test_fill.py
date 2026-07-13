import polars as pl
import pytest

from flash_excel.core.steps.fill import fill_nulls


def test_fill_nulls_strategy_value():
    df = pl.DataFrame({"pays": ["France", None, "Espagne"]})
    out = fill_nulls(df, columns=["pays"], strategy="value", value="Inconnu")
    assert out["pays"].to_list() == ["France", "Inconnu", "Espagne"]


def test_fill_nulls_strategy_forward():
    df = pl.DataFrame({"pays": ["France", None, None]})
    out = fill_nulls(df, columns=["pays"], strategy="forward")
    assert out["pays"].to_list() == ["France", "France", "France"]


def test_fill_nulls_value_strategy_without_value_raises():
    df = pl.DataFrame({"pays": [None]})
    with pytest.raises(ValueError, match="requires a non-null"):
        fill_nulls(df, columns=["pays"], strategy="value", value=None)


def test_fill_nulls_invalid_strategy_raises():
    df = pl.DataFrame({"pays": [None]})
    with pytest.raises(ValueError, match="Invalid fill_nulls strategy"):
        fill_nulls(df, columns=["pays"], strategy="bogus")
