import polars as pl

from flash_excel.core.steps.clean import clean_text


def test_clean_text_trim_and_collapse():
    df = pl.DataFrame({"nom": ["  Alice   Martin  "]})
    out = clean_text(df, columns=["nom"], ops=["trim", "collapse"])
    assert out["nom"].to_list() == ["Alice Martin"]


def test_clean_text_accents_and_case_upper():
    df = pl.DataFrame({"nom": ["élève"]})
    out = clean_text(df, columns=["nom"], ops=["accents"], case="upper")
    assert out["nom"].to_list() == ["ELEVE"]


def test_clean_text_special_removes_punctuation():
    df = pl.DataFrame({"nom": ["a.b,c!"]})
    out = clean_text(df, columns=["nom"], ops=["special"])
    assert out["nom"].to_list() == ["abc"]


def test_clean_text_empty_columns_returns_unchanged():
    df = pl.DataFrame({"nom": ["A"]})
    out = clean_text(df, columns=[])
    assert out.equals(df)
