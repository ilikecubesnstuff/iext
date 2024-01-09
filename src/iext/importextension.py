import inspect
import textwrap


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


class ExtendImportsMeta(type):
    """
    A metaclass that dynamically extends classes with additional imports.

    This metaclass allows classes to extend their functionality by providing extra
    imports that might not be present in the environment. It attempts the specified
    imports and injects them into the class's namespace, enabling the class to use them.
    If any import fails, the class becomes unavailable and raises an exception on
    instantiation.
    """

    def __imports__():
        """
        This method name must be used to define additional imports.
        """
        pass

    def __new__(metacls, name, bases, namespace):
        """
        Create a new class with dynamically injected imports.
        """
        imports = namespace.pop("__imports__", metacls.__imports__)
        src = inspect.getsource(imports)
        *_, body = src.partition("\n")
        try:
            exec(textwrap.dedent(body), {}, namespace)
        except ModuleNotFoundError as e:
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
