from pathlib import Path

from lazydocs import MarkdownGenerator

from registerer import exceptions, registry, validators

generator = MarkdownGenerator()
root_dir = Path(__file__).parent


def generate_examples_md():
    examples_dir = root_dir / "examples"
    return "\n\n".join(
        [
            f"### Register a {file_path.name.removesuffix('.py').replace('-', ' ').title()}\n\n```python\n{open(file_path).read()}\n```"
            for file_path in examples_dir.glob("*.py")
        ]
    )


def generate_reference_md():
    modules = [registry, validators, exceptions]
    return "\n\n\n".join([generator.import2md(module, depth=3) for module in modules])


docs = f"""
## Examples

{generate_examples_md()}

## Reference

{generate_reference_md()}
"""

template = open(root_dir / "README.template").read()


open(root_dir / "README.md", "w+").write(template.format(docs=docs))
