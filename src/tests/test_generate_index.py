from pathlib import Path
from unittest.mock import patch, MagicMock, mock_open

import jinja2

from marimushka.export import _generate_index


@patch.object(Path, 'open', new_callable=mock_open)
@patch('jinja2.Environment')
def test_generate_index_success(mock_env, mock_file_open, temp_output_dir, sample_notebooks_data, sample_apps_data, mock_logger):
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

@patch.object(Path, 'open', side_effect=OSError("File error"))
def test_generate_index_file_error(temp_output_dir, sample_notebooks_data, mock_logger):
    """Test handling of file error during index generation."""
    # Setup
    template_file = Path("template_dir/template.html.j2")

    # Execute
    _generate_index(temp_output_dir, template_file, sample_notebooks_data, logger_instance=mock_logger)

    # Assert
    mock_logger.error.assert_called()

@patch('jinja2.Environment')
def test_generate_index_template_error(mock_env, temp_output_dir, sample_notebooks_data, mock_logger):
    """Test handling of template error during index generation."""
    # Setup
    template_file = Path("template_dir/template.html.j2")

    # Mock the template error
    mock_env.return_value.get_template.side_effect = jinja2.exceptions.TemplateError("Template error")

    # Execute
    _generate_index(temp_output_dir, template_file, sample_notebooks_data, logger_instance=mock_logger)

    # Assert
    mock_logger.error.assert_called()