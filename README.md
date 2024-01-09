# iext

[![PyPI - Version](https://img.shields.io/pypi/v/iext)](https://pypi.org/project/iext/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/iext)](https://pypi.org/project/iext/)
[![tests](https://github.com/ilikecubesnstuff/iext/actions/workflows/tests.yml/badge.svg)](https://github.com/ilikecubesnstuff/iext/actions/workflows/tests.yml)
[![pdm-managed](https://img.shields.io/badge/pdm-managed-blueviolet)](https://pdm.fming.dev)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)

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
