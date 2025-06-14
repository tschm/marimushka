"""
Tests for the export.py module.

This module contains tests for the functions in the export.py module:
- _export_html_wasm
- _generate_index
- _export
- main
- cli
"""

import subprocess
from pathlib import Path
from unittest.mock import patch, MagicMock, mock_open

import jinja2

from marimushka.export import (
    _export_html_wasm,
    _generate_index,
    _export,
    main,
    cli
)


class TestExportHtmlWasm:
    """Tests for the _export_html_wasm function."""

    @patch('subprocess.run')
    def test_export_html_wasm_success(self, mock_run, temp_notebook_path, temp_output_dir, mock_logger):
        """Test successful export of a notebook."""
        # Setup
        mock_run.return_value = MagicMock(returncode=0)

        # Execute
        result = _export_html_wasm(temp_notebook_path, temp_output_dir, logger_instance=mock_logger)

        # Assert
        assert result is True
        mock_run.assert_called_once()
        mock_logger.info.assert_called()

    @patch('subprocess.run')
    def test_export_html_wasm_as_app(self, mock_run, temp_notebook_path, temp_output_dir, mock_logger):
        """Test export of a notebook as an app."""
        # Setup
        mock_run.return_value = MagicMock(returncode=0)

        # Execute
        result = _export_html_wasm(temp_notebook_path, temp_output_dir, as_app=True, logger_instance=mock_logger)

        # Assert
        assert result is True
        mock_run.assert_called_once()
        # Check that the command includes the app-specific flags
        cmd_args = mock_run.call_args[0][0]
        assert "--mode" in cmd_args
        assert "run" in cmd_args
        assert "--no-show-code" in cmd_args

    @patch('subprocess.run')
    def test_export_html_wasm_subprocess_error(self, mock_run, temp_notebook_path, temp_output_dir, mock_logger):
        """Test handling of subprocess error during export."""
        # Setup
        mock_run.side_effect = subprocess.CalledProcessError(1, "cmd", stderr="Error message")

        # Execute
        result = _export_html_wasm(temp_notebook_path, temp_output_dir, logger_instance=mock_logger)

        # Assert
        assert result is False
        mock_logger.error.assert_called()

    @patch('subprocess.run')
    def test_export_html_wasm_general_exception(self, mock_run, temp_notebook_path, temp_output_dir, mock_logger):
        """Test handling of general exception during export."""
        # Setup
        mock_run.side_effect = Exception("Unexpected error")

        # Execute
        result = _export_html_wasm(temp_notebook_path, temp_output_dir, logger_instance=mock_logger)

        # Assert
        assert result is False
        mock_logger.error.assert_called()


class TestGenerateIndex:
    """Tests for the _generate_index function."""

    @patch('builtins.open', new_callable=mock_open)
    @patch('jinja2.Environment')
    def test_generate_index_success(self, mock_env, mock_file_open, temp_output_dir, sample_notebooks_data, sample_apps_data, mock_logger):
        """Test successful generation of index.html."""
        # Setup
        template_file = Path("template_dir/template.html.j2")

        # Mock the template rendering
        mock_template = MagicMock()
        mock_env.return_value.get_template.return_value = mock_template
        mock_template.render.return_value = "<html>Rendered content</html>"

        # Execute
        _generate_index(temp_output_dir, template_file, sample_notebooks_data, sample_apps_data, logger_instance=mock_logger)

        # Assert
        mock_env.assert_called_once()
        mock_env.return_value.get_template.assert_called_once_with(template_file.name)
        mock_template.render.assert_called_once_with(notebooks=sample_notebooks_data, apps=sample_apps_data)
        mock_file_open.assert_called_once_with(temp_output_dir / "index.html", "w")
        mock_file_open().write.assert_called_once_with("<html>Rendered content</html>")
        mock_logger.info.assert_called()

    @patch('builtins.open', side_effect=OSError("File error"))
    def test_generate_index_file_error(self, mock_file_open, temp_output_dir, sample_notebooks_data, mock_logger):
        """Test handling of file error during index generation."""
        # Setup
        template_file = Path("template_dir/template.html.j2")

        # Execute
        _generate_index(temp_output_dir, template_file, sample_notebooks_data, logger_instance=mock_logger)

        # Assert
        mock_logger.error.assert_called()

    @patch('jinja2.Environment')
    def test_generate_index_template_error(self, mock_env, temp_output_dir, sample_notebooks_data, mock_logger):
        """Test handling of template error during index generation."""
        # Setup
        template_file = Path("template_dir/template.html.j2")

        # Mock the template error
        mock_env.return_value.get_template.side_effect = jinja2.exceptions.TemplateError("Template error")

        # Execute
        _generate_index(temp_output_dir, template_file, sample_notebooks_data, logger_instance=mock_logger)

        # Assert
        mock_logger.error.assert_called()


class TestExport:
    """Tests for the _export function."""

    @patch('marimushka.export._export_html_wasm')
    def test_export_success(self, mock_export_html_wasm, temp_output_dir, mock_logger):
        """Test successful export of notebooks from a folder."""
        # Setup
        folder = Path("notebooks")

        # Mock Path.exists and Path.rglob
        with patch.object(Path, 'exists', return_value=True):
            with patch.object(Path, 'rglob', return_value=[
                Path("notebooks/notebook1.py"),
                Path("notebooks/notebook2.py")
            ]):
                # Mock successful export for all notebooks
                mock_export_html_wasm.return_value = True

                # Execute
                result = _export(folder, temp_output_dir, logger_instance=mock_logger)

                # Assert
                assert len(result) == 2
                assert result[0]["display_name"] == "notebook1"
                assert result[0]["html_path"] == "notebooks/notebook1.html"
                assert result[1]["display_name"] == "notebook2"
                assert result[1]["html_path"] == "notebooks/notebook2.html"
                assert mock_export_html_wasm.call_count == 2
                mock_logger.info.assert_called()

    def test_export_folder_not_found(self, temp_output_dir, mock_logger):
        """Test handling of non-existent folder."""
        # Setup
        folder = Path("nonexistent_folder")

        # Mock Path.exists
        with patch.object(Path, 'exists', return_value=False):
            # Execute
            result = _export(folder, temp_output_dir, logger_instance=mock_logger)

            # Assert
            assert result == []
            mock_logger.warning.assert_called()

    def test_export_no_notebooks_found(self, temp_output_dir, mock_logger):
        """Test handling of folder with no notebooks."""
        # Setup
        folder = Path("empty_folder")

        # Mock Path.exists and Path.rglob
        with patch.object(Path, 'exists', return_value=True):
            with patch.object(Path, 'rglob', return_value=[]):
                # Execute
                result = _export(folder, temp_output_dir, logger_instance=mock_logger)

                # Assert
                assert result == []
                mock_logger.warning.assert_called()

    @patch('marimushka.export._export_html_wasm')
    def test_export_partial_success(self, mock_export_html_wasm, temp_output_dir, mock_logger):
        """Test partial success when exporting notebooks."""
        # Setup
        folder = Path("notebooks")

        # Mock Path.exists and Path.rglob
        with patch.object(Path, 'exists', return_value=True):
            with patch.object(Path, 'rglob', return_value=[
                Path("notebooks/notebook1.py"),
                Path("notebooks/notebook2.py")
            ]):
                # Mock success for first notebook, failure for second
                mock_export_html_wasm.side_effect = [True, False]

                # Execute
                result = _export(folder, temp_output_dir, logger_instance=mock_logger)

                # Assert
                assert len(result) == 1
                assert result[0]["display_name"] == "notebook1"
                assert result[0]["html_path"] == "notebooks/notebook1.html"
                assert mock_export_html_wasm.call_count == 2
                mock_logger.info.assert_called()


class TestMain:
    """Tests for the main function."""

    @patch('marimushka.export._export')
    @patch('marimushka.export._generate_index')
    def test_main_success(self, mock_generate_index, mock_export, tmp_path, sample_notebooks_data, sample_apps_data, mock_logger):
        """Test successful execution of the main function."""
        # Setup
        mock_export.side_effect = [sample_notebooks_data, sample_apps_data]

        # Execute
        main(output_dir=tmp_path, logger_instance=mock_logger)

        # Assert
        assert mock_export.call_count == 2
        mock_generate_index.assert_called_once()
        mock_logger.info.assert_called()

    @patch('marimushka.export._export')
    @patch('marimushka.export._generate_index')
    def test_main_no_notebooks_or_apps(self, mock_generate_index, mock_export, tmp_path, mock_logger):
        """Test handling of no notebooks or apps found."""
        # Setup
        mock_export.return_value = []

        # Execute
        main(output_dir=tmp_path, logger_instance=mock_logger)

        # Assert
        assert mock_export.call_count == 2
        mock_generate_index.assert_not_called()
        mock_logger.warning.assert_called()

    @patch('marimushka.export._export')
    @patch('marimushka.export._generate_index')
    def test_main_custom_paths(self, mock_generate_index, mock_export, sample_notebooks_data, sample_apps_data, mock_logger, tmp_path):
        """Test main function with custom paths."""
        # Setup
        mock_export.side_effect = [sample_notebooks_data, sample_apps_data]

        # Create subdirectories in tmp_path for custom paths
        custom_output_dir = tmp_path / "custom_output"
        custom_notebooks_dir = tmp_path / "custom_notebooks"
        custom_apps_dir = tmp_path / "custom_apps"

        # Execute
        main(
            output_dir=custom_output_dir,
            template="custom_template.html.j2",
            notebooks=custom_notebooks_dir,
            apps=custom_apps_dir,
            logger_instance=mock_logger
        )

        # Assert
        # Check that _export was called with the custom paths
        mock_export.assert_any_call(custom_notebooks_dir, custom_output_dir, as_app=False, logger_instance=mock_logger)
        mock_export.assert_any_call(custom_apps_dir, custom_output_dir, as_app=True, logger_instance=mock_logger)
        # Check that _generate_index was called with the custom paths
        mock_generate_index.assert_called_once()
        mock_logger.info.assert_called()

    @patch('marimushka.export._export')
    @patch('marimushka.export._generate_index')
    def test_main_default_logger(self, mock_generate_index, mock_export, sample_notebooks_data, sample_apps_data, tmp_path):
        """Test main function with default logger."""
        # Setup
        mock_export.side_effect = [sample_notebooks_data, sample_apps_data]

        # Execute
        main(output_dir=tmp_path)  # No logger_instance provided, should use default logger

        # Assert
        assert mock_export.call_count == 2
        mock_generate_index.assert_called_once()


class TestCli:
    """Tests for the cli function."""

    @patch('fire.Fire')
    def test_cli(self, mock_fire):
        """Test the cli function."""
        # Execute
        cli()

        # Assert
        mock_fire.assert_called_once_with(main)
