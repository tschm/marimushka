"""Tests for the command line interface."""
from unittest.mock import patch

from marimushka.export import MarimushkaCLI, cli


@patch('fire.Fire')
def test_cli(mock_fire):
    """Test the cli function."""
    # Execute
    cli()

    # Assert
    mock_fire.assert_called_once_with(MarimushkaCLI, name="marimushka")
