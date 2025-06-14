"""
Pytest configuration file.

This file contains fixtures and configuration for pytest.
"""

import pytest
from unittest.mock import MagicMock
from pathlib import Path


@pytest.fixture
def mock_logger():
    """Return a mock logger instance."""
    return MagicMock()


@pytest.fixture
def temp_notebook_path():
    """Return a Path object for a temporary notebook."""
    return Path("test_notebook.py")


@pytest.fixture
def temp_output_dir(tmp_path):
    """Return a Path object for a temporary output directory.

    Uses pytest's built-in tmp_path fixture to create a unique temporary directory
    for each test function, which is automatically cleaned up after the test.
    """
    return tmp_path


@pytest.fixture
def sample_notebooks_data():
    """Return sample data for notebooks."""
    return [
        {
            "display_name": "Notebook 1",
            "html_path": "notebook1.html",
        },
        {
            "display_name": "Notebook 2",
            "html_path": "notebook2.html",
        },
    ]


@pytest.fixture
def sample_apps_data():
    """Return sample data for apps."""
    return [
        {
            "display_name": "App 1",
            "html_path": "app1.html",
        },
        {
            "display_name": "App 2",
            "html_path": "app2.html",
        },
    ]
