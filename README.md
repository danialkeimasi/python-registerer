# Registerer

[![pypi](https://img.shields.io/pypi/v/registerer.svg)](https://pypi.python.org/pypi/registerer/)
[![ci](https://github.com/danialkeimasi/python-registerer/workflows/ci/badge.svg)](https://github.com/danialkeimasi/python-registerer/actions)
[![codecov](https://codecov.io/gh/danialkeimasi/python-registerer/branch/main/graph/badge.svg?token=Q5MG14RKJL)](https://codecov.io/gh/danialkeimasi/python-registerer)
[![license](https://img.shields.io/github/license/danialkeimasi/python-registerer.svg)](https://github.com/danialkeimasi/python-registerer/blob/master/LICENSE)

Sometimes you may want to use a string to identify a specific function or class. This is a common way of designing your code, but it can be tricky to do it without repeating yourself. Registerer is a tool that helps you to do this easily, and also makes sure that your code is explicit and type safe.

## TLDR

Write this:

```python exec="true" source="above"
import registerer

command_handler_registry = registerer.Registerer()


@command_handler_registry.register()
def info(args):
    return "how can i help you?"


@command_handler_registry.register()
def play(args):
    return "let me play a song for you"


command = "info"
args = {}
assert command_handler_registry[command](args) == "how can i help you?"
```

Instead of this, which violates the Open-Closed Principle (OCP):

```python exec="true" source="above"
def info(args):
    return "how can i help you?"


def play(args):
    return "let me play a song for you"


def command_handler(command, args):
    if command == "info":
        return info(args)
    if command == "play":
        return play(args)


command = "play"
args = {}
assert command_handler(command, args) == "let me play a song for you"
```

## Links

- For more information [Read the docs](https://danialkeimasi.github.io/python-registerer/).

## Installation

You can install the latest version of registerer from PyPI:

```sh
pip install registerer
```

## Features

- It's completely type-safe, thus you will get suggestions from your IDE.
- Writing custom validations for registered items is provided without any inheritance.
- generate choices for Django from registered items.
- And so on...
