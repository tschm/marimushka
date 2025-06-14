# 📦 marimushka

[![PyPI version](https://badge.fury.io/py/marimushka.svg)](https://badge.fury.io/py/marimushka)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Created with qCradle](https://img.shields.io/badge/Created%20with-qCradle-blue?style=flat-square)](https://github.com/tschm/package)
[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)
[![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/tschm/marimushka/release.yml?label=release)](https://github.com/tschm/marimushka/actions/workflows/release.yml)
[![PyPI Downloads](https://img.shields.io/pypi/dm/marimushka)](https://pypi.org/project/marimushka/)
[![GitHub stars](https://img.shields.io/github/stars/tschm/marimushka)](https://github.com/tschm/marimushka/stargazers)

## 🚀 Overview

Marimushka is a tool for exporting [marimo](https://marimo.io) notebooks
to HTML/WebAssembly format with custom styling. It helps you create beautiful,
interactive web versions of your marimo notebooks and applications.

### ✨ Features

- 📊 Export marimo notebooks (.py files) to HTML/WebAssembly format
- 🎨 Customize the output using Jinja2 templates
- 📱 Support for both interactive notebooks and standalone applications
- 🌐 Generate an index page that lists all your notebooks and apps
- 🔄 Integrate with GitHub Actions for automated deployment

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

## 🛠️ Usage

### Command Line

```bash
# Basic usage (uses default settings)
marimushka

# Specify a custom template
marimushka --template path/to/template.html.j2

# Specify a custom output directory
marimushka --output-dir my_site
```

### Project Structure

Marimushka expects your project to have the following structure:

```bash
your-project/
├── notebooks/     # Regular marimo notebooks (.py files)
├── apps/          # Marimo applications (.py files)
└── templates/     # Optional: Custom templates for export
    └── custom.html.j2  # Default template location
```

### GitHub Action

You can use marimushka in your GitHub Actions workflow:

```yaml
- name: Export marimo notebooks
  uses: tschm/marimushka/actions/export@main
  with:
    template: 'path/to/template.html.j2'
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

## 👥 Contributing

- 🍴 Fork the repository
- 🌿 Create your feature branch (git checkout -b feature/amazing-feature)
- 💾 Commit your changes (git commit -m 'Add some amazing feature')
- 🚢 Push to the branch (git push origin feature/amazing-feature)
- 🔍 Open a Pull Request

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
pytest tests/ -v

# Or use the make command
make test
```

### Cleaning Output Directories

When you run marimushka, it creates output directories (`_site`, `custom_output`, or `output_dir` depending on your configuration). To clean these directories, you can use:

```bash
# Clean all output directories
make clean-output

# Clean all ignored files (including output directories)
make clean
```

## 📄 License

This project is licensed under the [MIT License](LICENSE).
