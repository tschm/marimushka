"""Tests for the notebook.py module.

This module contains tests for the Notebook class in the notebook.py module.
"""
import subprocess
from pathlib import Path
from unittest.mock import patch, MagicMock, mock_open

import jinja2
import pytest
from loguru import logger

from marimushka.export import _folder2notebooks, _generate_index
from marimushka.notebook import Notebook


class TestNotebook:
    """Tests for the Notebook class."""

    def test_init_success(self, resource_dir):
        """Test successful initialization of a Notebook."""
        # Setup
        notebook_path = resource_dir / "notebooks" / "fibonacci.py"

        # Create a mock path that exists and is a Python file
        with patch.object(Path, 'exists', return_value=True), \
             patch.object(Path, 'is_file', return_value=True), \
             patch.object(Path, 'suffix', '.py'):

            # Execute
            notebook = Notebook(notebook_path)

            # Assert
            assert notebook.path == notebook_path
            assert notebook.is_app is False

    def test_init_with_app(self, resource_dir):
        """Test initialization of a Notebook as an app."""
        # Setup
        notebook_path = resource_dir / "apps" / "charts.py"

        # Create a mock path that exists and is a Python file
        with patch.object(Path, 'exists', return_value=True), \
             patch.object(Path, 'is_file', return_value=True), \
             patch.object(Path, 'suffix', '.py'):

            # Execute
            notebook = Notebook(notebook_path, is_app=True)

            # Assert
            assert notebook.path == notebook_path
            assert notebook.is_app is True

    def test_init_file_not_found(self):
        """Test initialization with a non-existent file."""
        # Setup
        notebook_path = Path("nonexistent_file.py")

        # Mock Path.exists to return False
        with patch.object(Path, 'exists', return_value=False):

            # Execute and Assert
            with pytest.raises(FileNotFoundError):
                Notebook(notebook_path)

    def test_init_not_a_file(self):
        """Test initialization with a path that is not a file."""
        # Setup
        notebook_path = Path("directory")

        # Mock Path.exists to return True and Path.is_file to return False
        with patch.object(Path, 'exists', return_value=True), \
             patch.object(Path, 'is_file', return_value=False):

            # Execute and Assert
            with pytest.raises(ValueError):
                Notebook(notebook_path)

    def test_init_not_python_file(self):
        """Test initialization with a non-Python file."""
        # Setup
        notebook_path = Path("file.txt")

        # Mock Path.exists and Path.is_file to return True, but set suffix to .txt
        with patch.object(Path, 'exists', return_value=True), \
             patch.object(Path, 'is_file', return_value=True), \
             patch.object(Path, 'suffix', '.txt'):

            # Execute and Assert
            with pytest.raises(ValueError):
                Notebook(notebook_path)

    @patch('subprocess.run')
    def test_to_wasm_success(self, mock_run, resource_dir, tmp_path, mock_logger):
        """Test successful export of a notebook to WebAssembly."""
        # Setup
        notebook_path = resource_dir / "notebooks" / "fibonacci.py"
        output_dir = tmp_path

        # Mock successful subprocess run
        mock_run.return_value = MagicMock(returncode=0)

        # Create a notebook with mocked path validation
        with patch.object(Path, 'exists', return_value=True), \
             patch.object(Path, 'is_file', return_value=True), \
             patch.object(Path, 'suffix', '.py'):
            notebook = Notebook(notebook_path)

            # Execute
            result = notebook.to_wasm(output_dir, logger_instance=mock_logger)

            # Assert
            assert result is True
            mock_run.assert_called_once()
            mock_logger.info.assert_called()

            # Check that the command includes the notebook-specific flags
            cmd_args = mock_run.call_args[0][0]
            assert "--mode" in cmd_args
            assert "edit" in cmd_args
            assert "--no-show-code" not in cmd_args

    @patch('subprocess.run')
    def test_to_wasm_as_app(self, mock_run, resource_dir, tmp_path, mock_logger):
        """Test export of a notebook as an app."""
        # Setup
        notebook_path = resource_dir / "apps" / "charts.py"
        output_dir = tmp_path

        # Mock successful subprocess run
        mock_run.return_value = MagicMock(returncode=0)

        # Create a notebook with mocked path validation
        with patch.object(Path, 'exists', return_value=True), \
             patch.object(Path, 'is_file', return_value=True), \
             patch.object(Path, 'suffix', '.py'):
            notebook = Notebook(notebook_path, is_app=True)

            # Execute
            result = notebook.to_wasm(output_dir, logger_instance=mock_logger)

            # Assert
            assert result is True
            mock_run.assert_called_once()

            # Check that the command includes the app-specific flags
            cmd_args = mock_run.call_args[0][0]
            assert "--mode" in cmd_args
            assert "run" in cmd_args
            assert "--no-show-code" in cmd_args

    @patch('subprocess.run')
    def test_to_wasm_subprocess_error(self, mock_run, resource_dir, tmp_path, mock_logger):
        """Test handling of subprocess error during export."""
        # Setup
        notebook_path = resource_dir / "notebooks" / "fibonacci.py"
        output_dir = tmp_path

        # Mock subprocess error
        mock_run.side_effect = subprocess.CalledProcessError(1, "cmd", stderr="Error message")

        # Create a notebook with mocked path validation
        with patch.object(Path, 'exists', return_value=True), \
             patch.object(Path, 'is_file', return_value=True), \
             patch.object(Path, 'suffix', '.py'):
            notebook = Notebook(notebook_path)

            # Execute
            result = notebook.to_wasm(output_dir, logger_instance=mock_logger)

            # Assert
            assert result is False
            mock_logger.error.assert_called()

    @patch('subprocess.run')
    def test_to_wasm_general_exception(self, mock_run, resource_dir, tmp_path, mock_logger):
        """Test handling of general exception during export."""
        # Setup
        notebook_path = resource_dir / "notebooks" / "fibonacci.py"
        output_dir = tmp_path

        # Mock general exception
        mock_run.side_effect = Exception("Unexpected error")

        # Create a notebook with mocked path validation
        with patch.object(Path, 'exists', return_value=True), \
             patch.object(Path, 'is_file', return_value=True), \
             patch.object(Path, 'suffix', '.py'):
            notebook = Notebook(notebook_path)

            # Execute
            result = notebook.to_wasm(output_dir, logger_instance=mock_logger)

            # Assert
            assert result is False
            mock_logger.error.assert_called()




