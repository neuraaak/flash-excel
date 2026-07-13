import polars as pl
import pytest

from flash_excel.core.registry import REGISTRY, action


def test_action_registers_function_in_registry():
    name = "test_registry_dummy_action"
    try:

        @action(name)
        def dummy(df: pl.DataFrame) -> pl.DataFrame:
            return df

        assert name in REGISTRY
        assert REGISTRY[name] is dummy
    finally:
        REGISTRY.pop(name, None)


def test_action_duplicate_name_raises():
    name = "test_registry_duplicate_action"
    try:

        @action(name)
        def first(df: pl.DataFrame) -> pl.DataFrame:
            return df

        with pytest.raises(ValueError, match="already registered"):

            @action(name)
            def second(df: pl.DataFrame) -> pl.DataFrame:
                return df
    finally:
        REGISTRY.pop(name, None)
