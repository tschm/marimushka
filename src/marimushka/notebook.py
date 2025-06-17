"""Notebook module for handling marimo notebooks.

This module provides the Notebook class for representing and exporting marimo notebooks.
"""

import dataclasses
import subprocess
from pathlib import Path

from loguru import logger

from enum import Enum

class Kind(Enum):
    NB = "notebook"
    NB_WASM = "notebook_wasm"
    APP = "app"

    @property
    def command(self) -> list[str]:
        match self:
            case Kind.NB:
                return ["uvx", "marimo", "export", "html", "--sandbox"]
            case Kind.NB_WASM:
                return ["uvx", "marimo", "export", "html-wasm", "--sandbox", "--mode", "edit"]
            case Kind.APP:
                return ["uvx", "marimo", "export", "html-wasm", "--sandbox", "--mode", "run"]

    @property
    def html_path(self) -> Path:
        match self:
            case Kind.NB:
                return Path("notebooks")
            case Kind.NB_WASM:
                return Path("notebooks_wasm")
            case Kind.APP:
                return Path("apps")


def folder2notebooks(folder: Path | str | None, kind: Kind) -> list[Notebook]:
    """Find all marimo notebooks in a directory."""
    if folder is None or folder == "":
        return []

    # which files are included here?
    notebooks = list(Path(folder).rglob("*.py"))

    # uvx marimo export html-wasm / html --sandbox (--mode edit/run) (
    return [Notebook(path=nb, kind=kind) for nb in notebooks]
    
@dataclasses.dataclass(frozen=True)
class Notebook:
    """Represents a marimo notebook.

    This class encapsulates a marimo notebook (.py file) and provides methods
    for exporting it to HTML/WebAssembly format.

    Attributes:
        path (Path): Path to the marimo notebook (.py file)
        kind (Kind): How the notebook ts treated
    """

    path: Path
    kind: Kind = Kind.NB

    def __post_init__(self):
        """Validate the notebook path after initialization.

        Raises:
            FileNotFoundError: If the file does not exist
            ValueError: If the path is not a file or not a Python file

        """
        if not self.path.exists():
            raise FileNotFoundError(f"File not found: {self.path}")
        if not self.path.is_file():
            raise ValueError(f"Path is not a file: {self.path}")
        if not self.path.suffix == ".py":
            raise ValueError(f"File is not a Python file: {self.path}")

    def export(self, output_dir: Path) -> bool:
        """Export the notebook to HTML/WebAssembly format.

        This method exports the marimo notebook to HTML/WebAssembly format.
        If is_app is True, the notebook is exported in "run" mode with code hidden,
        suitable for applications. Otherwise, it's exported in "edit" mode,
        suitable for interactive notebooks.

        Args:
            output_dir (Path): Directory where the exported HTML file will be saved

        Returns:
            bool: True if export succeeded, False otherwise

        """
        # Base command for marimo export
        # cmd: list[str] = ["uvx", "marimo", "export", "html-wasm", "--sandbox"]

        # Configure export mode based on whether it's an app or a notebook
        #if self.is_app:
        #    logger.info(f"Export {self.path.stem} as app")
        cmd = self.kind.command
        #cmd.extend(["--mode", "run", "--no-show-code"])  # Apps run in "run" mode with hidden code
        #else:
        #    logger.info(f"Export {self.path.stem} as notebook")
        #    cmd.extend(["--mode", "edit"])  # Notebooks run in "edit" mode

        try:
            # Create the full output path and ensure the directory exists
            output_file: Path = output_dir / f"{self.path.stem}.html"
            output_file.parent.mkdir(parents=True, exist_ok=True)

            # Add the notebook path and output file to command
            cmd.extend([str(self.path), "-o", str(output_file)])

            # Run marimo export command
            # logger_instance.debug(f"Running command: {cmd}")
            subprocess.run(cmd, capture_output=True, text=True, check=True)
            # logger_instance.info(f"Successfully exported {self.path.stem}")
            return True
        except subprocess.CalledProcessError as e:
            # Handle marimo export errors
            logger.error(f"Error exporting {self.path}:")
            logger.error(f"Command output: {e.stderr}")
            return False
        except Exception as e:
            # Handle unexpected errors
            logger.error(f"Unexpected error exporting {self.path}: {e}")
            return False

    @property
    def display_name(self) -> str:
        """Return the display name for the notebook."""
        return self.path.stem.replace("_", " ")

    @property
    def html_path(self) -> Path:
        """Return the path to the exported HTML file."""
        return self.kind.path / f"{self.path.stem}.html"
