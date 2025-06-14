# 📦 [marimograd](https://tschm.github.io/marimograd/book)

[![PyPI version](https://badge.fury.io/py/marimograd.svg)](https://badge.fury.io/py/marimograd)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE.txt)
[![Created with qCradle](https://img.shields.io/badge/Created%20with-qCradle-blue?style=flat-square)](https://github.com/tschm/package)

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/tschm/marimograd)

## 🚀 Overview

Marimograd is a tool for exporting [marimo](https://marimo.io) notebooks
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
pip install marimograd
```

### Using uv (recommended)

```bash
uv pip install marimograd
```

## 🛠️ Usage

### Command Line

```bash
# Basic usage (uses default settings)
marimograd

# Specify a custom template
marimograd --template path/to/template.html.j2

# Specify a custom output directory
marimograd --output-dir my_site
```

### Project Structure

Marimograd expects your project to have the following structure:

```bash
your-project/
├── notebooks/     # Regular marimo notebooks (.py files)
├── apps/          # Marimo applications (.py files)
└── templates/     # Optional: Custom templates for export
    └── custom.html.j2  # Default template location
```

### GitHub Action

You can use marimograd in your GitHub Actions workflow:

```yaml
- name: Export marimo notebooks
  uses: tschm/marimograd/actions/export@main
  with:
    template: 'path/to/template.html.j2'
```

## 🧩 Examples

### Basic Export

```python
# Export all notebooks and apps with default settings
from marimograd.export import main
main()
```

### Custom Template

```python
# Export with a custom template
from marimograd.export import main
main(template="my_templates/custom.html.j2")
```

## 👥 Contributing

- 🍴 Fork the repository
- 🌿 Create your feature branch (git checkout -b feature/amazing-feature)
- 💾 Commit your changes (git commit -m 'Add some amazing feature')
- 🚢 Push to the branch (git push origin feature/amazing-feature)
- 🔍 Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file
for details.
