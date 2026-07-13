import polars as pl
import pytest

from flash_excel.core.steps.deduplicate import deduplicate_rows


def test_deduplicate_rows_keep_first_by_subset():
    df = pl.DataFrame({"id": [1, 1, 2], "nom": ["A", "A2", "B"]})
    out = deduplicate_rows(df, subset=["id"], keep="first")
    assert out.sort("id")["nom"].to_list() == ["A", "B"]


def test_deduplicate_rows_keep_none_drops_all_duplicates():
    df = pl.DataFrame({"id": [1, 1, 2]})
    out = deduplicate_rows(df, subset=["id"], keep="none")
    assert out["id"].to_list() == [2]


def test_deduplicate_rows_invalid_keep_raises():
    df = pl.DataFrame({"id": [1, 2]})
    with pytest.raises(ValueError, match="Invalid keep value"):
        deduplicate_rows(df, keep="bogus")
