"""Tests for the export.py module.

This module contains tests for the functions in the export.py module:
- _folder2notebooks
- _generate_index
- main
- cli
"""

import subprocess
from pathlib import Path
from unittest.mock import patch, MagicMock, mock_open

import jinja2
import pytest

from marimushka.export import (
    _folder2notebooks,
    _generate_index,
    main,
    cli
)


class TestFolder2Notebooks:
    """Tests for the _folder2notebooks function."""

    def test_folder2notebooks_none(self):
        """Test _folder2notebooks with None folder."""
        # Execute
        result = _folder2notebooks(folder=None, is_app=False)

        # Assert
        assert result == []

    def test_folder2notebooks_empty(self, tmp_path):
        """Test _folder2notebooks with empty folder."""
        # Setup
        empty_folder = tmp_path / "empty"
        empty_folder.mkdir()

        # Execute
        result = _folder2notebooks(folder=empty_folder, is_app=False)

        # Assert
        assert result == []

    def test_folder2notebooks_with_notebooks(self, tmp_path):
        """Test _folder2notebooks with notebooks."""
        # Setup
        notebooks_folder = tmp_path / "notebooks"
        notebooks_folder.mkdir()

        # Create some test notebook files
        notebook1 = notebooks_folder / "notebook1.py"
        notebook2 = notebooks_folder / "notebook2.py"
        notebook1.write_text("# Test notebook 1")
        notebook2.write_text("# Test notebook 2")

        # Execute
        result = _folder2notebooks(folder=notebooks_folder, is_app=False)

        # Assert
        assert len(result) == 2
        assert all(not notebook.is_app for notebook in result)
        # Check that the paths are correct (convert to string for easier comparison)
        notebook_paths = [str(notebook.path) for notebook in result]
        assert str(notebook1) in notebook_paths
        assert str(notebook2) in notebook_paths

    def test_folder2notebooks_with_apps(self, tmp_path):
        """Test _folder2notebooks with apps."""
        # Setup
        apps_folder = tmp_path / "apps"
        apps_folder.mkdir()

        # Create some test app files
        app1 = apps_folder / "app1.py"
        app2 = apps_folder / "app2.py"
        app1.write_text("# Test app 1")
        app2.write_text("# Test app 2")

        # Execute
        result = _folder2notebooks(folder=apps_folder, is_app=True)

        # Assert
        assert len(result) == 2
        assert all(notebook.is_app for notebook in result)
        # Check that the paths are correct (convert to string for easier comparison)
        app_paths = [str(notebook.path) for notebook in result]
        assert str(app1) in app_paths
        assert str(app2) in app_paths


class TestGenerateIndex:
    """Tests for the _generate_index function."""

    @patch.object(Path, 'open', new_callable=mock_open)
    @patch('jinja2.Environment')
    def test_generate_index_success(self, mock_env, mock_file_open, tmp_path, mock_logger):
        """Test successful generation of index.html."""
        # Setup
        output_dir = tmp_path / "output"
        template_file = Path("template_dir/template.html.j2")

        # Create mock notebooks and apps
        mock_notebook1 = MagicMock()
        mock_notebook2 = MagicMock()
        mock_app1 = MagicMock()

        notebooks = [mock_notebook1, mock_notebook2]
        apps = [mock_app1]

        # Mock the template rendering
        mock_template = MagicMock()
        mock_env.return_value.get_template.return_value = mock_template
        mock_template.render.return_value = "<html>Rendered content</html>"

        # Execute
        _generate_index(output=output_dir, template_file=template_file, notebooks=notebooks, apps=apps)

        # Assert
        # Check that to_wasm was called for each notebook and app
        mock_notebook1.to_wasm.assert_called_once_with(output_dir=output_dir / "notebooks")
        mock_notebook2.to_wasm.assert_called_once_with(output_dir=output_dir / "notebooks")
        mock_app1.to_wasm.assert_called_once_with(output_dir=output_dir / "apps")

        # Check that the template was rendered and written to file
        mock_env.assert_called_once()
        mock_env.return_value.get_template.assert_called_once_with(template_file.name)
        mock_template.render.assert_called_once_with(notebooks=notebooks, apps=apps)
        mock_file_open.assert_called_once_with(output_dir / "index.html", "w")
        mock_file_open().write.assert_called_once_with("<html>Rendered content</html>")

    @patch.object(Path, 'open', side_effect=OSError("File error"))
    @patch('jinja2.Environment')
    def test_generate_index_file_error(self, mock_env, mock_file_open, tmp_path):
        """Test handling of file error during index generation."""
        # Setup
        output_dir = tmp_path / "output"
        template_file = Path("template_dir/template.html.j2")

        # Create mock notebooks
        mock_notebook = MagicMock()
        notebooks = [mock_notebook]
        apps = []

        # Mock the template rendering
        mock_template = MagicMock()
        mock_env.return_value.get_template.return_value = mock_template
        mock_template.render.return_value = "<html>Rendered content</html>"

        # Execute and Assert (should not raise an exception)
        _generate_index(output=output_dir, template_file=template_file, notebooks=notebooks, apps=apps)

        # Check that to_wasm was still called
        mock_notebook.to_wasm.assert_called_once_with(output_dir=output_dir / "notebooks")

    @patch('jinja2.Environment')
    @patch.object(Path, 'mkdir')
    def test_generate_index_template_error(self, mock_mkdir, mock_env, tmp_path):
        """Test handling of template error during index generation."""
        # Setup
        output_dir = tmp_path / "output"
        template_file = Path("template_dir/template.html.j2")

        # Create mock notebooks
        mock_notebook = MagicMock()
        notebooks = [mock_notebook]
        apps = []

        # Mock the template error
        mock_env.side_effect = jinja2.exceptions.TemplateError("Template error")

        # Execute and Assert (should not raise an exception)
        _generate_index(output=output_dir, template_file=template_file, notebooks=notebooks, apps=apps)

        # Check that to_wasm was still called
        mock_notebook.to_wasm.assert_called_once_with(output_dir=output_dir / "notebooks")


class TestMain:
    """Tests for the main function."""

    @patch('marimushka.export._folder2notebooks')
    @patch('marimushka.export._generate_index')
    def test_main_success(self, mock_generate_index, mock_folder2notebooks, mock_logger):
        """Test successful execution of the main function."""
        # Setup
        mock_notebooks = [MagicMock(), MagicMock()]
        mock_apps = [MagicMock()]
        mock_folder2notebooks.side_effect = [mock_notebooks, mock_apps]

        # Execute
        main(logger_instance=mock_logger)

        # Assert
        assert mock_folder2notebooks.call_count == 2
        mock_folder2notebooks.assert_any_call(folder=None, is_app=False)
        mock_folder2notebooks.assert_any_call(folder=None, is_app=True)
        mock_generate_index.assert_called_once()
        mock_logger.info.assert_called()

    @patch('marimushka.export._folder2notebooks')
    @patch('marimushka.export._generate_index')
    def test_main_no_notebooks_or_apps(self, mock_generate_index, mock_folder2notebooks, mock_logger):
        """Test handling of no notebooks or apps found."""
        # Setup
        mock_folder2notebooks.return_value = []

        # Execute
        main(logger_instance=mock_logger)

        # Assert
        assert mock_folder2notebooks.call_count == 2
        mock_generate_index.assert_not_called()
        mock_logger.warning.assert_called_with("No notebooks or apps found!")

    @patch('marimushka.export._folder2notebooks')
    @patch('marimushka.export._generate_index')
    def test_main_custom_paths(self, mock_generate_index, mock_folder2notebooks, mock_logger, tmp_path):
        """Test main function with custom paths."""
        # Setup
        mock_notebooks = [MagicMock(), MagicMock()]
        mock_apps = [MagicMock()]
        mock_folder2notebooks.side_effect = [mock_notebooks, mock_apps]

        custom_output = tmp_path / "custom_output"
        custom_template = tmp_path / "custom_template.html.j2"
        custom_notebooks = tmp_path / "custom_notebooks"
        custom_apps = tmp_path / "custom_apps"

        # Execute
        main(
            output=custom_output,
            template=custom_template,
            notebooks=custom_notebooks,
            apps=custom_apps,
            logger_instance=mock_logger
        )

        # Assert
        mock_folder2notebooks.assert_any_call(folder=custom_notebooks, is_app=False)
        mock_folder2notebooks.assert_any_call(folder=custom_apps, is_app=True)
        mock_generate_index.assert_called_once_with(
            output=custom_output,
            template_file=custom_template,
            notebooks=mock_notebooks,
            apps=mock_apps
        )
        mock_logger.info.assert_called()

    @patch('marimushka.export._folder2notebooks')
    @patch('marimushka.export._generate_index')
    def test_main_default_logger(self, mock_generate_index, mock_folder2notebooks):
        """Test main function with default logger."""
        # Setup
        mock_notebooks = [MagicMock(), MagicMock()]
        mock_apps = [MagicMock()]
        mock_folder2notebooks.side_effect = [mock_notebooks, mock_apps]

        # Execute
        main()  # No logger_instance provided, should use default logger

        # Assert
        assert mock_folder2notebooks.call_count == 2
        mock_generate_index.assert_called_once()
