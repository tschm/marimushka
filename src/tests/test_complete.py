import pytest

from marimushka.export import main
from loguru import logger

@pytest.fixture
def output(resource_dir):
    return resource_dir / "output"

def test_complete(resource_dir, output):
    main(notebooks=resource_dir / "notebooks",
         apps=resource_dir / "apps",
         template=resource_dir / "templates" / "default.html.j2",
         output=resource_dir / "output",
         logger_instance=logger)

    assert (output / "index.html").exists()
    assert (output / "notebooks" ).exists()
    assert (output / "apps" ).exists()

    assert (output / "notebooks" / "penguins.html").exists()
    assert (output / "notebooks" / "fibonacci.html").exists()

    assert (output / "apps" / "charts.html").exists()

    assert '<a href="notebooks/penguins.html" class="card-link">Open Notebook</a>' in (output / "index.html").read_text()
    assert '<a href="notebooks/fibonacci.html" class="card-link">Open Notebook</a>' in (output / "index.html").read_text()
    assert '<a href="apps/charts.html" class="card-link app">Open App</a>' in (output / "index.html").read_text()