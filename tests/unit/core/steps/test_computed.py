import polars as pl

from flash_excel.core.steps.computed import add_computed_column


def test_bracket_syntax_allows_column_with_space():
    df = pl.DataFrame({"Nom Complet": ["alice"]})
    out = add_computed_column(df, "test", "MAJUSCULE([Nom Complet])")
    assert out["test"].to_list() == ["ALICE"]


def test_bracket_syntax_allows_column_starting_with_digit():
    df = pl.DataFrame({"2024_total": [3]})
    out = add_computed_column(df, "test", "ABS([2024_total])")
    assert out["test"].to_list() == [3]


def test_bracket_syntax_allows_special_characters():
    df = pl.DataFrame({"Prix (€)": [1.2]})
    out = add_computed_column(df, "test", "ARRONDI([Prix (€)], 0)")
    assert out["test"].to_list() == [1.0]


def test_bracket_syntax_combines_with_functions():
    df = pl.DataFrame({"N° Client": ["a"], "id": ["1"]})
    out = add_computed_column(df, "test", "CONCATENER([N° Client], id)")
    assert out["test"].to_list() == ["a1"]


def test_plain_identifier_columns_still_work():
    df = pl.DataFrame({"prenom": ["bob"], "nom": ["martin"]})
    out = add_computed_column(df, "test", "MAJUSCULE(CONCATENER(prenom, nom))")
    assert out["test"].to_list() == ["BOBMARTIN"]
