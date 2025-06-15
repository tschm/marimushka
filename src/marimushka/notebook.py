"""Notebook module for handling marimo notebooks.

This module provides the Notebook class for representing and exporting marimo notebooks.
"""

import dataclasses
import subprocess
from pathlib import Path

from loguru import logger


@dataclasses.dataclass(frozen=True)
class Notebook:
    """Represents a marimo notebook.

    This class encapsulates a marimo notebook (.py file) and provides methods
    for exporting it to HTML/WebAssembly format.

    Attributes:
        path (Path): Path to the marimo notebook (.py file)
        is_app (bool): Whether the notebook should be treated as an app (run mode)
                      or a regular notebook (edit mode). Defaults to False.

    """

    path: Path
    is_app: bool = False

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

    def to_wasm(self, output_dir: Path, logger_instance=logger) -> bool:
        """Export the notebook to HTML/WebAssembly format.

        This method exports the marimo notebook to HTML/WebAssembly format.
        If is_app is True, the notebook is exported in "run" mode with code hidden,
        suitable for applications. Otherwise, it's exported in "edit" mode,
        suitable for interactive notebooks.

        Args:
            output_dir (Path): Directory where the exported HTML file will be saved
            logger_instance: Logger instance to use. Defaults to the standard logger.

        Returns:
            bool: True if export succeeded, False otherwise

        """
        # Base command for marimo export
        cmd: list[str] = ["uvx", "marimo", "export", "html-wasm", "--sandbox"]

        # Configure export mode based on whether it's an app or a notebook
        if self.is_app:
            logger_instance.info(f"Export {self.path.stem} as app")
            cmd.extend(["--mode", "run", "--no-show-code"])  # Apps run in "run" mode with hidden code
        else:
            logger_instance.info(f"Export {self.path.stem} as notebook")
            cmd.extend(["--mode", "edit"])  # Notebooks run in "edit" mode

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
            logger_instance.error(f"Error exporting {self.path}:")
            logger_instance.error(f"Command output: {e.stderr}")
            return False
        except Exception as e:
            # Handle unexpected errors
            logger_instance.error(f"Unexpected error exporting {self.path}: {e}")
            return False

    @property
    def display_name(self) -> str:
        """Return the display name for the notebook."""
        return self.path.stem.replace("_", " ")

    @property
    def html_path(self) -> Path:
        """Return the path to the exported HTML file."""
        return Path("apps") / f"{self.path.stem}.html" if self.is_app else Path("notebooks") / f"{self.path.stem}.html"
