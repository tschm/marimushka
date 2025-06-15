"""Tests for the export.py module.

This module contains tests for the functions in the export.py module:
- _export_html_wasm
- _generate_index
- _export
- main
- cli
"""

from pathlib import Path
from unittest.mock import patch

from marimushka.export import _export


@patch('marimushka.export._export_html_wasm')
def test_export_success(mock_export_html_wasm, temp_output_dir, mock_logger):
    """Test successful export of notebooks from a folder."""
    # Setup
    folder = Path("notebooks")

    # Mock Path.exists and Path.rglob
    with patch.object(Path, 'exists', return_value=True), patch.object(Path, 'rglob', return_value=[
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
        assert str(result[0]["html_path"]).endswith("notebook1.html")
        assert result[1]["display_name"] == "notebook2"
        assert str(result[1]["html_path"]).endswith("notebook2.html")
        assert mock_export_html_wasm.call_count == 2
        mock_logger.info.assert_called()

def test_export_folder_not_found( temp_output_dir, mock_logger):
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

def test_export_no_notebooks_found(temp_output_dir, mock_logger):
    """Test handling of folder with no notebooks."""
    # Setup
    folder = Path("empty_folder")

    # Mock Path.exists and Path.rglob
    with patch.object(Path, 'exists', return_value=True), patch.object(Path, 'rglob', return_value=[]):
        # Execute
        result = _export(folder, temp_output_dir, logger_instance=mock_logger)

        # Assert
        assert result == []
        mock_logger.warning.assert_called()

@patch('marimushka.export._export_html_wasm')
def test_export_partial_success( mock_export_html_wasm, temp_output_dir, mock_logger):
    """Test partial success when exporting notebooks."""
    # Setup
    folder = Path("notebooks")

    # Mock Path.exists and Path.rglob
    with patch.object(Path, 'exists', return_value=True), patch.object(Path, 'rglob', return_value=[
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
        assert str(result[0]["html_path"]).endswith("notebook1.html")
        assert mock_export_html_wasm.call_count == 2
        mock_logger.info.assert_called()
