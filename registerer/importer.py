import operator
import typing
from functools import reduce
from importlib import import_module
from pathlib import Path, PosixPath


def relative_module_finder(current_file: str, globes: list[str]) -> typing.Generator[str, None, None]:
    """
    Finds python modules relative to given file and relative globes.
    """
    current_dir_path = Path(current_file).parent
    founded_modules: typing.Iterable[PosixPath] = reduce(operator.add, [current_dir_path.glob(glob) for glob in globes])

    for module in founded_modules:
        if module.is_file() and module.name.endswith(".py"):
            yield (
                str(module.relative_to(current_dir_path))
                .removesuffix(".py")
                .removesuffix("/__init__")
                .replace("/", ".")
            )


def relative_importer(current_file: str, globes: list[str]):
    """
    Import python files relative to current file.

    >>> relative_importer(__file__, ["classes/*", "../somewhere/else/*"])
    """
    for module in relative_module_finder(current_file, globes):
        import_module(module)
