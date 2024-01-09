import pytest

from iext import ExtendImports


def test_existent_package():
    class TestClass(ExtendImports):
        def __imports__(self):
            import random

    inst = TestClass()
    assert not hasattr(inst, "__imports__")


def test_nonexistent_package():
    class TestClass(ExtendImports):
        def __imports__(self):
            import asdf

    with pytest.raises(ModuleNotFoundError):
        inst = TestClass()
