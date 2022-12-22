# Registerer

[![pypi](https://img.shields.io/pypi/v/registerer.svg)](https://pypi.python.org/pypi/registerer/)
[![ci](https://github.com/danialkeimasi/python-registerer/workflows/tests/badge.svg)](https://github.com/danialkeimasi/python-registerer/actions)
[![license](https://img.shields.io/github/license/danialkeimasi/python-registerer.svg)](https://github.com/danialkeimasi/python-registerer/blob/master/LICENSE)

Implement maintainable and easy to use registry patterns in your project.

### TLDR

Write this:

```python exec="true" source="material-block"
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
print("output:", command_handler_registry[command](args))
```

Instead of this, which violates the Open-Closed Principle (OCP):

```python exec="true" source="material-block"
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
print("output:", command_handler(command, args))
```
