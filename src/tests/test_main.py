from unittest.mock import patch

from marimushka.export import main


@patch('marimushka.export._export')
@patch('marimushka.export._generate_index')
def test_main_success(mock_generate_index, mock_export, tmp_path, sample_notebooks_data, sample_apps_data, mock_logger):
    """Test successful execution of the main function."""
    # Setup
    mock_export.side_effect = [sample_notebooks_data, sample_apps_data]

    # Execute
    main(output=tmp_path, logger_instance=mock_logger)

    # Assert
    assert mock_export.call_count == 2
    mock_generate_index.assert_called_once()
    mock_logger.info.assert_called()

@patch('marimushka.export._export')
@patch('marimushka.export._generate_index')
def test_main_no_notebooks_or_apps(mock_generate_index, mock_export, tmp_path, mock_logger):
    """Test handling of no notebooks or apps found."""
    # Setup
    mock_export.return_value = []

    # Execute
    main(output=tmp_path, logger_instance=mock_logger)

    # Assert
    assert mock_export.call_count == 2
    mock_generate_index.assert_not_called()
    mock_logger.warning.assert_called()

@patch('marimushka.export._export')
@patch('marimushka.export._generate_index')
def test_main_custom_paths(mock_generate_index, mock_export, sample_notebooks_data, sample_apps_data, mock_logger, tmp_path):
    """Test main function with custom paths."""
    # Setup
    mock_export.side_effect = [sample_notebooks_data, sample_apps_data]

    # Create subdirectories in tmp_path for custom paths
    custom_output_dir = tmp_path / "custom_output"
    custom_notebooks_dir = tmp_path / "custom_notebooks"
    custom_apps_dir = tmp_path / "custom_apps"

    # Execute
    main(
        output=custom_output_dir,
        template="custom_template.html.j2",
        notebooks=custom_notebooks_dir,
        apps=custom_apps_dir,
        logger_instance=mock_logger
    )

    # Assert
    # Check that _export was called with the custom paths
    mock_export.assert_any_call(folder=custom_notebooks_dir, output_dir=custom_output_dir / "notebooks", as_app=False, logger_instance=mock_logger)
    mock_export.assert_any_call(folder=custom_apps_dir, output_dir=custom_output_dir / "apps", as_app=True, logger_instance=mock_logger)
    # Check that _generate_index was called with the custom paths
    mock_generate_index.assert_called_once()
    mock_logger.info.assert_called()

@patch('marimushka.export._export')
@patch('marimushka.export._generate_index')
def test_main_default_logger(mock_generate_index, mock_export, sample_notebooks_data, sample_apps_data, tmp_path):
    """Test main function with default logger."""
    # Setup
    mock_export.side_effect = [sample_notebooks_data, sample_apps_data]

    # Execute
    main(output=tmp_path)  # No logger_instance provided, should use default logger

    # Assert
    assert mock_export.call_count == 2
    mock_generate_index.assert_called_once()
