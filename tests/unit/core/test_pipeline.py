import polars as pl

from flash_excel.core.models import (
    DropColumnsStep,
    Preset,
    PresetMeta,
    RenameColumnsStep,
    ReorderColumnsStep,
)
from flash_excel.core.pipeline import compute_schema_at_step, run_pipeline


def test_run_pipeline_executes_steps_in_order():
    df = pl.DataFrame({"a": [1], "b": [2], "tmp": [3]})
    preset = Preset(
        meta=PresetMeta(name="test"),
        steps=[DropColumnsStep(action="drop_columns", columns=["tmp"])],
    )
    out = run_pipeline(df, preset)
    assert out.columns == ["a", "b"]


def test_run_pipeline_empty_steps_returns_input_unchanged():
    df = pl.DataFrame({"a": [1]})
    preset = Preset(meta=PresetMeta(name="test"), steps=[])
    out = run_pipeline(df, preset)
    assert out.equals(df)


def test_compute_schema_at_step_drop_columns():
    steps = [DropColumnsStep(action="drop_columns", columns=["tmp"])]
    result = compute_schema_at_step(steps, ["a", "b", "tmp"], index=1)
    assert result == ["a", "b"]


def test_compute_schema_at_step_rename_then_reorder():
    steps = [
        RenameColumnsStep(action="rename_columns", mapping={"old": "new"}),
        ReorderColumnsStep(action="reorder_columns", columns=["new"]),
    ]
    result = compute_schema_at_step(steps, ["old", "b"], index=2)
    assert result == ["new", "b"]


def test_compute_schema_at_step_zero_index_returns_original_headers():
    steps = [DropColumnsStep(action="drop_columns", columns=["a"])]
    result = compute_schema_at_step(steps, ["a", "b"], index=0)
    assert result == ["a", "b"]
