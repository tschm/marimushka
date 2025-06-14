# Makefile for the package project template
# This Makefile provides commands for setting up the development environment,
# running tests, starting interactive notebooks, and maintaining code quality.

# Set the default target to 'help' when running make without arguments
.DEFAULT_GOAL := help

# Create a Python virtual environment using uv (faster alternative to venv)
venv:
	@curl -LsSf https://astral.sh/uv/install.sh | sh  # Install uv if not already installed
	@uv venv --python '3.12'  # Create a virtual environment with Python 3.12


# Mark 'install' as a phony target (not associated with a file)
.PHONY: install
install: venv ## Install a virtual environment
	@uv pip install --upgrade pip  # Ensure pip is up to date
	@uv sync --all-extras --dev --frozen  # Install all dependencies from pyproject.toml


# Mark 'fmt' as a phony target
.PHONY: fmt
fmt: venv ## Run autoformatting and linting
	@uv pip install pre-commit  # Install pre-commit in the virtual environment
	@uv run pre-commit install  # Install pre-commit hooks in the git repository
	@uv run pre-commit run --all-files  # Run all pre-commit hooks on all files


# Mark 'clean' as a phony target
.PHONY: clean
clean:  ## Clean up caches and build artifacts
	# Remove all files and directories that are ignored by git
	# -X: only remove files ignored by git, -d: include directories, -f: force
	@git clean -X -d -f


# Mark 'help' as a phony target
.PHONY: help
help:  ## Display this help screen
	@echo -e "\033[1mAvailable commands:\033[0m"  # Print header in bold
	# Find all targets with comments (##) and display them as a help menu
	# This grep/awk command extracts target names and their descriptions from the Makefile
	@grep -E '^[a-z.A-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-18s\033[0m %s\n", $$1, $$2}' | sort


# Mark 'marimo' as a phony target
.PHONY: marimo
marimo: install ## Install Marimo
	@uv pip install marimo  # Install Marimo interactive notebook tool
	@uv run marimo edit book/marimo  # Start Marimo in edit mode, opening the book/marimo directory


# Mark 'test' as a phony target
.PHONY: test
test: install  ## Run pytests
	@uv pip install pytest  # Install pytest testing framework
	@uv run pytest src/tests  # Run all tests in the src/tests directory
