"""Tests for the _export_html_wasm function."""
import subprocess
from unittest.mock import patch, MagicMock

from marimushka.export import _export_html_wasm


@patch('subprocess.run')
def test_export_html_wasm_success(mock_run, temp_notebook_path, temp_output_dir, mock_logger):
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
def test_export_html_wasm_as_app(mock_run, temp_notebook_path, temp_output_dir, mock_logger):
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
def test_export_html_wasm_subprocess_error(mock_run, temp_notebook_path, temp_output_dir, mock_logger):
    """Test handling of subprocess error during export."""
    # Setup
    mock_run.side_effect = subprocess.CalledProcessError(1, "cmd", stderr="Error message")

    # Execute
    result = _export_html_wasm(temp_notebook_path, temp_output_dir, logger_instance=mock_logger)

    # Assert
    assert result is False
    mock_logger.error.assert_called()

@patch('subprocess.run')
def test_export_html_wasm_general_exception( mock_run, temp_notebook_path, temp_output_dir, mock_logger):
    """Test handling of general exception during export."""
    # Setup
    mock_run.side_effect = Exception("Unexpected error")

    # Execute
    result = _export_html_wasm(temp_notebook_path, temp_output_dir, logger_instance=mock_logger)

    # Assert
    assert result is False
    mock_logger.error.assert_called()