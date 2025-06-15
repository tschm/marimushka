"""Test complete marimushka build process."""
from loguru import logger

from marimushka.export import main


def test_complete(resource_dir, tmp_path):
    """Test complete marimushka build process."""
    main(notebooks=resource_dir / "notebooks",
         apps=resource_dir / "apps",
         template=resource_dir / "templates" / "default.html.j2",
         output=tmp_path / "output",
         logger_instance=logger)

    assert (tmp_path / "output" / "index.html").exists()
    assert (tmp_path / "output" / "notebooks" ).exists()
    assert (tmp_path / "output" / "apps" ).exists()

    assert (tmp_path / "output" /  "notebooks" / "penguins.html").exists()
    assert (tmp_path / "output" /  "notebooks" / "fibonacci.html").exists()

    assert (tmp_path / "output" / "apps" / "charts.html").exists()

    assert '<a href="notebooks/penguins.html" class="card-link">Open Notebook</a>' in (tmp_path / "output" / "index.html").read_text()
    assert '<a href="notebooks/fibonacci.html" class="card-link">Open Notebook</a>' in (tmp_path / "output" /  "index.html").read_text()
    assert '<a href="apps/charts.html" class="card-link app">Open App</a>' in (tmp_path / "output" /  "index.html").read_text()
