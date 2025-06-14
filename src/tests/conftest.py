"""global fixtures"""

from __future__ import annotations

from pathlib import Path

import pytest


@pytest.fixture(scope="session", name="resource_dir")
def resource_fixture():
    """resource fixture"""
    return Path(__file__).parent / "resources"


@pytest.fixture(scope="session", name="root_dir")
def root_fixture(resource_dir: Path) -> Path:
    return Path(__file__).parent.parent.parent
