"""Tests for the __version__ variable in the marimushka package."""

import importlib.metadata
import marimushka


def test_version():
    """Test that __version__ matches the version in pyproject.toml."""
    # Get the version from pyproject.toml via package metadata
    expected_version = importlib.metadata.version("marimushka")
    
    # Check that __version__ is defined
    assert hasattr(marimushka, "__version__")
    
    # Check that __version__ matches the expected version
    assert marimushka.__version__ == expected_version