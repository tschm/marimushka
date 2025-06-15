"""Demo script for marimushka."""

from pathlib import Path

from marimushka.notebook import folder2notebooks, generate_index

if __name__ == "__main__":
    template = Path("src/tests/resources/templates/default.html.j2")
    notebooks = folder2notebooks(Path("src/tests/resources/notebooks"), is_app=False)
    apps = folder2notebooks(Path("src/tests/resources/apps"), is_app=True)
    print(notebooks)
    print(apps)

    output = Path("yyy")
    generate_index(output, template, notebooks, apps)
