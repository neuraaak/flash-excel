import pytest

pytestmark = pytest.mark.smoke


def test_main_module_imports_without_error():
    import main

    assert hasattr(main, "run")
