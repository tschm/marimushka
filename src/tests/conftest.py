"""Pytest configuration file.

This file contains fixtures and configuration for pytest.
"""

from pathlib import Path
from unittest.mock import MagicMock

import pytest


@pytest.fixture
def mock_logger():
    """Return a mock logger instance."""
    return MagicMock()


@pytest.fixture()
def resource_dir():
    """Pytest fixture that provides the path to the test resources directory.

    Returns:
        Path: A Path object pointing to the resources directory within the tests folder.

    """
    return Path(__file__).parent / "resources"
