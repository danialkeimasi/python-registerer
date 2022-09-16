from pathlib import Path

import lazydocs
import registerer

docs_dir = Path(__file__).parent
root_dir = docs_dir.parent


def generate_template_md():
    with open(docs_dir / "README.py") as file:
        blocks = [s for s in file.read().strip().split('"""') if s]

    markdown = "".join(
        [
            block if (index == len(blocks) - 1) else (block + ("```python" if (index % 2 == 0) else "```"))
            for index, block in enumerate(blocks)
        ]
    )

    return markdown


def generate_reference_md():
    generator = lazydocs.MarkdownGenerator(
        src_root_path="registerer",
        src_base_url="https://github.com/danialkeimasi/python-registerer/tree/main/registerer",
    )
    return {
        "Registerer": generator.class2md(registerer.Registerer, depth=3),
        "exceptions": generator.module2md(registerer.exceptions, depth=4),
    }


def main():
    markdown = generate_template_md()
    for variable, value in generate_reference_md().items():
        markdown = markdown.replace("{{%s}}" % variable, value)

    with open(root_dir / "README.md", "w+") as f:
        f.write(markdown)


if __name__ == "__main__":
    main()
