# iext

Add new imports tied to a specific class.

## Installation

Install this package via `pip`:

```
python -m pip install iext
```

## Usage

To extend the imports within a specific class, subclass `ExtendImports` and add an `__imports__` method with all the extra imports. Everything imported here will be added to the namespace of `self`.

```py
from iext import ExtendImports

class ExampleClass(ExtendImports):
    def __imports__(self):
        import pkg1
        from pkg2 import thing

    def example_method(self):
        return self.pkg1.func(self.thing)
```
