import pytest
from pydantic import ValidationError

from flash_excel.core.models import DropColumnsStep, FilterCondition, Preset, PresetMeta


def test_drop_columns_step_requires_non_empty_columns():
    with pytest.raises(ValidationError):
        DropColumnsStep(action="drop_columns", columns=[])


def test_drop_columns_step_rejects_wrong_action_literal():
    with pytest.raises(ValidationError):
        DropColumnsStep(action="rename_columns", columns=["a"])


def test_preset_meta_defaults():
    meta = PresetMeta(name="Test")
    assert meta.name == "Test"


def test_preset_holds_ordered_steps():
    preset = Preset(
        meta=PresetMeta(name="Test"),
        steps=[DropColumnsStep(action="drop_columns", columns=["a"])],
    )
    assert len(preset.steps) == 1
    assert preset.steps[0].action == "drop_columns"


def test_filter_condition_accepts_scalar_value_types():
    cond = FilterCondition(column="age", operator="gte", value=18)
    assert cond.value == 18
