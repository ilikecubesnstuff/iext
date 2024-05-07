import inspect
import textwrap
import warnings


def _unavailable(e):
    """
    Creates a placeholder type that raises the provided exception on instantiation.
    """

    class Unavailable:
        """
        Placeholder class that raises an exception upon instantiation.
        """

        def __init__(self):
            raise e

    return Unavailable


class ImportExtensionError(Exception):
    """
    Base class for all exceptions raised by the import extension module.
    """

    pass


class ExtendImportsMeta(type):
    """
    A metaclass that dynamically extends classes with additional imports.

    This metaclass allows classes to extend their functionality by providing extra
    imports that might not be present in the environment. It attempts the specified
    imports and injects them into the class's namespace, enabling the class to use them.
    If any import fails, the class becomes unavailable and raises an exception on
    instantiation.
    """

    def __new__(metacls, name, bases, namespace):
        """
        Create a new class with dynamically injected imports.
        """
        if "__imports__" not in namespace:
            return super().__new__(metacls, name, bases, namespace)

        __imports__ = namespace.pop("__imports__")

        src_file = inspect.getsourcefile(__imports__)
        src_lines, line_number = inspect.getsourcelines(__imports__)
        src = "".join(src_lines)

        _, _, src = src.partition("\n")
        line_number += 1
        src = textwrap.dedent(src)

        try:
            for line in src.split("\n"):
                exec(line, {}, namespace)
                line_number += 1
        except ModuleNotFoundError as e:
            return _unavailable(e)
        except SyntaxError as e:
            raise ImportExtensionError(
                f"the __imports__ body must contain no docstrings or multi-line expressions."
            )
        except Exception as e:
            warnings.warn_explicit(
                f"failed to create {name} due to {e.__class__.__name__}: {e}",
                UserWarning,
                src_file,
                line_number,
            )
            return _unavailable(e)
        return super().__new__(metacls, name, bases, namespace)


class ExtendImports(metaclass=ExtendImportsMeta):
    """
    A base class that allows extending functionality with additional imports.

    This class serves as a base for other classes that need to dynamically extend their
    functionality with extra imports. The '__imports__' method should be defined in
    subclasses to provide the required additional imports.
    """

    pass
