import polars as pl
import pytest

from flash_excel.core.steps.replace import replace_values


def test_replace_values_maps_exact_values():
    df = pl.DataFrame({"statut": ["YES", "NO", "YES"]})
    out = replace_values(df, column="statut", mapping={"YES": "Oui", "NO": "Non"})
    assert out["statut"].to_list() == ["Oui", "Non", "Oui"]


def test_replace_values_unmapped_left_unchanged():
    df = pl.DataFrame({"statut": ["MAYBE"]})
    out = replace_values(df, column="statut", mapping={"YES": "Oui"})
    assert out["statut"].to_list() == ["MAYBE"]


def test_replace_values_missing_column_raises():
    df = pl.DataFrame({"a": [1]})
    with pytest.raises(pl.exceptions.ColumnNotFoundError):
        replace_values(df, column="missing", mapping={"a": "b"})
