"""Build the script for marimo notebooks.

This script exports marimo notebooks to HTML/WebAssembly format and generates
an index.html file that lists all the notebooks. It handles both regular notebooks
(from the notebooks/ directory) and apps (from the apps/ directory).

The script can be run from the command line with optional arguments:
    uvx marimushka [--output-dir OUTPUT_DIR]

The exported files will be placed in the specified output directory (default: _site).
"""

# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "jinja2==3.1.3",
#     "fire==0.7.0",
#     "loguru==0.7.0"
# ]
# ///

from logging import Logger
from pathlib import Path

import fire
import jinja2
from loguru import logger

from marimushka.notebook import Notebook

from . import __version__


def _folder2notebooks(folder: Path | str | None, is_app: bool) -> list[Notebook]:
    """Find all marimo notebooks in a directory."""
    if folder is None or folder == "":
        return []

    notebooks = list(Path(folder).rglob("*.py"))

    return [Notebook(path=nb, is_app=is_app) for nb in notebooks]


def _generate_index(
    output: Path,
    template_file: Path,
    notebooks: list[Notebook] | None = None,
    apps: list[Notebook] | None = None,
    logger_instance=logger,
) -> None:
    """Generate an index.html file that lists all the notebooks.

    This function creates an HTML index page that displays links to all the exported
    notebooks. The index page includes the marimo logo and displays each notebook
    with a formatted title and a link to open it.

    Args:
        notebooks (List[Notebook]): List of notebooks with data for notebooks
        apps (List[Notebook]): List of notebooks with data for apps
        output (Path): Directory where the index.html file will be saved
        template_file (Path, optional): Path to the template file. If None, uses the default template.
        logger_instance: Logger instance to use. Defaults to the standard logger.

    Returns:
        None

    """
    # Initialize empty lists if None is provided
    notebooks = notebooks or []
    apps = apps or []

    # Export notebooks to WebAssembly
    for nb in notebooks:
        nb.to_wasm(output_dir=output / "notebooks")

    # Export apps to WebAssembly
    for nb in apps:
        nb.to_wasm(output_dir=output / "apps")

    # Create the full path for the index.html file
    index_path: Path = Path(output) / "index.html"

    # Ensure the output directory exists
    Path(output).mkdir(parents=True, exist_ok=True)

    # Set up Jinja2 environment and load template
    template_dir = template_file.parent
    template_name = template_file.name

    try:
        # Create Jinja2 environment and load template
        env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(template_dir), autoescape=jinja2.select_autoescape(["html", "xml"])
        )
        template = env.get_template(template_name)

        # Render the template with notebook and app data
        rendered_html = template.render(notebooks=notebooks, apps=apps)

        # Write the rendered HTML to the index.html file
        try:
            with Path.open(index_path, "w") as f:
                f.write(rendered_html)
            logger_instance.info(f"Successfully generated index file at {index_path}")
        except OSError as e:
            logger_instance.error(f"Error writing index file to {index_path}: {e}")
    except jinja2.exceptions.TemplateError as e:
        logger_instance.error(f"Error rendering template {template_file}: {e}")


def main(
    output: str | Path | None = None,
    template: str | Path = "templates/default.html.j2",
    notebooks: str | Path | None = None,
    apps: str | Path | None = None,
    logger_instance: Logger | None = None,
) -> None:
    """Export marimo notebooks.

    This function:
    1. Parses command line arguments
    2. Exports all marimo notebooks in 'notebooks' and 'apps' directories
    3. Generates an index.html file that lists all the notebooks

    Command line arguments:
        --output: Directory where the exported files will be saved (default: _site)
        --template: Path to the template file (default: templates/index.html.j2)
        --logger_instance: Logger instance to use. Defaults to the standard loguru logger.

    Returns:
        None

    """
    if logger_instance is None:
        logger_instance = logger

    logger_instance.info("Starting marimushka build process")
    logger_instance.info(f"Version of Marimushka: {__version__}")
    output = output or "_site"

    # Convert output_dir explicitly to Path (not done by fire)
    output_dir: Path = Path(output)
    logger_instance.info(f"Output directory: {output_dir}")

    # Make sure the output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)

    # Convert template to Path if provided
    template_file: Path = Path(template)
    logger_instance.info(f"Using template file: {template_file}")
    logger_instance.info(f"Notebooks: {notebooks}")
    logger_instance.info(f"Apps: {apps}")

    notebooks_data = _folder2notebooks(folder=notebooks, is_app=False)
    apps_data = _folder2notebooks(folder=apps, is_app=True)

    logger.info(f"# notebooks_data: {len(notebooks_data)}")
    logger.info(f"# apps_data: {len(apps_data)}")

    # Exit if no notebooks or apps were found
    if not notebooks_data and not apps_data:
        logger_instance.warning("No notebooks or apps found!")
        return

    _generate_index(
        output=output_dir,
        template_file=template_file,
        notebooks=notebooks_data,
        apps=apps_data,
    )


def cli():
    """Command line interface for marimushka build process."""
    fire.Fire(main)
