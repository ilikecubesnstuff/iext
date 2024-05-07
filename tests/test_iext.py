import pytest

from iext import ExtendImports
from iext.importextension import ImportExtensionError


def test_no_imports():
    class TestClass(ExtendImports):
        pass

    inst = TestClass()
    assert not hasattr(inst, "__imports__")


def test_existent_import():
    class TestClass(ExtendImports):
        def __imports__(self):
            import tests.module_dummy as module_dummy

    inst = TestClass()
    assert not hasattr(inst, "__imports__")


def test_problematic_import():
    with pytest.warns(UserWarning):

        class TestClass(ExtendImports):
            def __imports__(self):
                import tests.module_throw_exception as module_throw_exception

    with pytest.raises(Exception):
        inst = TestClass()


def test_nonexistent_import():
    class TestClass(ExtendImports):
        def __imports__(self):
            import test.module_nonexistent as module_nonexistent

    with pytest.raises(ModuleNotFoundError):
        inst = TestClass()


class TestIllFormedImports:
    def test_docstring(self):
        with pytest.raises(ImportExtensionError):

            class TestClass(ExtendImports):
                def __imports__(self):
                    """
                    This is a docstring.
                    """
                    import tests.module_dummy as module_dummy

    def test_nested_function(self):
        with pytest.raises(ImportExtensionError):

            class TestClass(ExtendImports):
                def __imports__(self):
                    def test():
                        pass

    def test_multiline_import(self):
        with pytest.raises(ImportExtensionError):

            class TestClass(ExtendImports):
                def __imports__(self):
                    import module_dummy

    def test_multiline_collection(self):
        with pytest.raises(ImportExtensionError):

            class TestClass(ExtendImports):
                def __imports__(self):
                    x = [1, 2, 3]


class TestWellFormedImports:
    def test_pass(self):
        class TestClass(ExtendImports):
            def __imports__(self):
                pass

        inst = TestClass()
        assert not hasattr(inst, "__imports__")

    def test_single_line_docstring(self):
        class TestClass(ExtendImports):
            def __imports__(self):
                "single line docstring"

        inst = TestClass()
        assert not hasattr(inst, "__imports__")

    def test_single_line_function(self):
        class TestClass(ExtendImports):
            def __imports__(self):
                def add(a, b):
                    return a + b

        inst = TestClass()
        assert not hasattr(inst, "__imports__")

    def test_lambda(self):
        class TestClass(ExtendImports):
            def __imports__(self):
                add = lambda a, b: a + b

        inst = TestClass()
        assert not hasattr(inst, "__imports__")

    def test_assignment(self):
        class TestClass(ExtendImports):
            def __imports__(self):
                a = 1
                b = 2
                c = 3
                d = "testing"

        inst = TestClass()
        assert not hasattr(inst, "__imports__")


def test_namespace_population():
    class TestClass(ExtendImports):
        def __imports__(self):
            a = 1
            b = 2
            c = 3
            d = "testing"

    inst = TestClass()
    assert hasattr(inst, "a")
    assert hasattr(inst, "b")
    assert hasattr(inst, "c")
    assert hasattr(inst, "d")


def test_inheritance():
    class TestClassA(ExtendImports):
        def __imports__(self):
            import tests.module_dummy as module_dummy

    class TestClassB(TestClassA):
        def __imports__(self):
            pass

    inst = TestClassB()
    assert hasattr(inst, "module_dummy")
