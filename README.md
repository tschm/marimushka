# 📦 marimushka

[![PyPI version](https://badge.fury.io/py/marimushka.svg)](https://badge.fury.io/py/marimushka)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python Tests](https://img.shields.io/github/actions/workflow/status/tschm/marimushka/pytest.yml?label=tests)](https://github.com/tschm/marimushka/actions/workflows/pytest.yml)
[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)
[![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/tschm/marimushka/release.yml?label=release)](https://github.com/tschm/marimushka/actions/workflows/release.yml)
[![GitHub stars](https://img.shields.io/github/stars/tschm/marimushka)](https://github.com/tschm/marimushka/stargazers)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)
[![Created with qCradle](https://img.shields.io/badge/Created%20with-qCradle-blue?style=flat-square)](https://github.com/tschm/package)

## 🚀 Overview

Marimushka is a powerful tool for exporting [marimo](https://marimo.io) notebooks
to HTML/WebAssembly format with custom styling. It helps you create beautiful,
interactive web versions of your marimo notebooks and applications that can be
shared with others or deployed to static hosting services like GitHub Pages.

Named after the nesting doll concept, Marimushka "wraps" your marimo notebooks
in a stylish, customizable HTML template, making them accessible to anyone
with a web browser - no Python installation required!

### ✨ Features

- 📊 **Export marimo notebooks** (.py files) to HTML/WebAssembly format
- 🎨 **Customize the output** using Jinja2 templates
- 📱 **Support for both interactive notebooks and standalone applications**
  - Notebooks are exported in "edit" mode, allowing code modification
  - Apps are exported in "run" mode with hidden code for a clean interface
- 🌐 **Generate an index page** that lists all your notebooks and apps
- 🔄 **Integrate with GitHub Actions** for automated deployment
- 🔍 **Recursive directory scanning** to find all notebooks in a project
- 🧩 **Flexible configuration** with command-line options and Python API

## 📋 Requirements

- Python 3.10+
- [marimo](https://marimo.io) (installed automatically as a dependency)
- [uv](https://github.com/astral-sh/uv) (recommended for installation)

## 📥 Installation

### Using pip

```bash
pip install marimushka
```

### Using uv (recommended)

```bash
uv pip install marimushka
```

### Development Installation

```bash
# Clone the repository
git clone https://github.com/tschm/marimushka.git
cd marimushka

# Install dependencies using the Makefile
make install

# Or manually with uv
uv venv
uv pip install --upgrade pip
uv sync --all-extras
```

## 🛠️ Usage

### Command Line

```bash
# Basic usage (uses default settings)
marimushka

# Specify a custom template
marimushka --template path/to/template.html.j2

# Specify a custom output directory
marimushka --output my_site

# Specify custom notebook and app directories
marimushka --notebooks path/to/notebooks --apps path/to/apps
```

### Python API

```python
# Import the main function
from marimushka.export import main

# Basic usage with default settings
main()

# With custom settings
main(
    output="_site",                        # Output directory
    template="templates/custom.html.j2",   # Custom template
    notebooks="path/to/notebooks",         # Notebooks directory
    apps="path/to/apps"                    # Apps directory
)
```

### Project Structure

Marimushka recommends your project to have the following structure:

```bash
your-project/
├── notebooks/     # Regular marimo notebooks (.py files)
├── apps/          # Marimo applications (.py files)
└── templates/     # Optional: Custom templates for export
    └── custom.html.j2  # Default template location
```

### Marimo Notebook Requirements

All marimo notebooks used with marimushka must follow the modern `--sandbox` convention.
This is a security feature that:

- Restricts the notebook's access to the system
- Prevents potentially harmful code execution
- Creates an isolated environment for the notebook

When developing or testing notebooks locally, always use the `--sandbox` flag:

```bash
# Running a notebook with the sandbox flag
marimo run your_notebook.py --sandbox

# Or with uvx
uvx marimo run your_notebook.py --sandbox
```

Marimushka automatically applies the `--sandbox` flag when exporting notebooks,
but it's important to ensure your notebooks are designed to work within these constraints.

### GitHub Action

You can use marimushka in your GitHub Actions workflow to automatically export
and deploy your notebooks:

```yaml
- name: Export marimo notebooks
  uses: tschm/marimushka/actions/export@main
  with:
    template: 'path/to/template.html.j2'  # Optional: custom template
    notebooks: 'notebooks'                # Optional: notebooks directory
    apps: 'apps'                          # Optional: apps directory
    publish: 'true'                       # Optional: publish to GitHub Pages
                                          # (default: false)
```

When the `publish` parameter is set to `true`, the action will:

1. Create a `.nojekyll` file to prevent GitHub Pages
from processing with Jekyll
2. Create a basic `robots.txt` file for search engine optimization
3. Deploy the exported notebooks to the `gh-pages` branch for GitHub Pages hosting

Note: To use the publish feature, your repository needs to have GitHub Pages
enabled and configured to use the `gh-pages` branch.

Additionally, your workflow will need the following permissions:

```yaml
permissions:
  contents: write  # Required for GitHub Pages deployment
```

This is necessary because the action needs write access to the repository contents
to create or update the `gh-pages` branch.

## 🎨 Customizing Templates

Marimushka uses Jinja2 templates to generate the index.html file.
You can customize the appearance of the index page by creating your own template.

The template has access to two variables:

- `notebooks`: A list of Notebook objects representing regular notebooks
- `apps`: A list of Notebook objects representing app notebooks

Each Notebook object has the following properties:

- `display_name`: The display name of the notebook (derived from the filename)
- `html_path`: The path to the exported HTML file
- `path`: The original path to the notebook file
- `is_app`: Whether the notebook is an app or a regular notebook

Example template structure:

```html
<!DOCTYPE html>
<html>
<head>
  <title>My Marimo Notebooks</title>
  <style>
    /* Your custom CSS here */
  </style>
</head>
<body>
  <h1>My Notebooks</h1>

  {% if notebooks %}
  <h2>Interactive Notebooks</h2>
  <ul>
    {% for notebook in notebooks %}
    <li>
      <a href="{{ notebook.html_path }}">{{ notebook.display_name }}</a>
    </li>
    {% endfor %}
  </ul>
  {% endif %}

  {% if apps %}
  <h2>Applications</h2>
  <ul>
    {% for app in apps %}
    <li>
      <a href="{{ app.html_path }}">{{ app.display_name }}</a>
    </li>
    {% endfor %}
  </ul>
  {% endif %}
</body>
</html>
```

## 🧩 Examples

### Basic Export

```python
# Export all notebooks and apps with default settings
from marimushka.export import main
main()
```

### Custom Template

```python
# Export with a custom template
from marimushka.export import main
main(template="my_templates/custom.html.j2")
```

## 🧹 Cleaning Up

When you run marimushka, it creates output directories
(`_site`, `custom_output`, or
other specified output directories). To clean these directories, you can use:

```bash
# Remove all files and directories that are ignored by git
# This includes the output directories
make clean
```

## 👥 Contributing

Contributions are welcome! Here's how you can contribute:

1. 🍴 Fork the repository
2. 🌿 Create your feature branch (`git checkout -b feature/amazing-feature`)
3. 💾 Commit your changes (`git commit -m 'Add some amazing feature'`)
4. 🚢 Push to the branch (`git push origin feature/amazing-feature`)
5. 🔍 Open a Pull Request

### Development Setup

```bash
# Clone the repository
git clone https://github.com/tschm/marimushka.git
cd marimushka

# Install dependencies
make install

# Run tests
make test

# Run linting and formatting
make fmt
```

### Running Tests

To run the tests, you'll need to install the development dependencies:

```bash
# Install the package with development dependencies
pip install -e ".[dev]"

# Or with uv (recommended)
uv pip install -e ".[dev]"
```

Then you can run the tests using pytest:

```bash
# Run tests with pytest
pytest src/tests/ -v

# Or use the make command
make test
```

## 📄 License

This project is licensed under the [MIT License](LICENSE).

## 🙏 Acknowledgements

- [marimo](https://marimo.io) - The reactive Python notebook that powers this project
- [Jinja2](https://jinja.palletsprojects.com/) - The templating engine
used for HTML generation
- [uv](https://github.com/astral-sh/uv) - The fast Python package installer and resolver
