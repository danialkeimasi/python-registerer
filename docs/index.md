# Registerer

[![pypi](https://img.shields.io/pypi/v/registerer.svg)](https://pypi.python.org/pypi/registerer/)
[![ci](https://github.com/danialkeimasi/python-registerer/workflows/ci/badge.svg)](https://github.com/danialkeimasi/python-registerer/actions)
[![license](https://img.shields.io/github/license/danialkeimasi/python-registerer.svg)](https://github.com/danialkeimasi/python-registerer/blob/master/LICENSE)

Implement maintainable and easy to use registry patterns in your project.

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
