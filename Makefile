# Makefile for docker-scaffold development
# Provides convenient commands for local development and testing

SHELL := /bin/bash
PYTHON := python3
VENV := venv
VENV_BIN := $(VENV)/bin
SCRIPTS_DIR := ansible/scripts
PROJECT_YML := project.yml
DEFAULTS_YML := ansible/vars/defaults.yml

.PHONY: help venv install clean test merge lint format check-deps dev all

# Default target
help:
	@echo ""
	@echo "Available targets:"
	@echo ""
	@echo "  make venv        - Create Python virtual environment"
	@echo "  make install     - Install Python dependencies"
	@echo "  make dev         - Setup complete dev environment (venv + install)"
	@echo "  make test        - Run Python unit tests"
	@echo "  make merge       - Test config merge locally"
	@echo "  make lint        - Run Python linter (flake8)"
	@echo "  make format      - Format Python code (black)"
	@echo "  make check-deps  - Check if dependencies are installed"
	@echo "  make clean       - Remove virtual environment and cache files"
	@echo "  make all         - Run full development setup and tests"
	@echo ""

# Create virtual environment
venv:
	@echo "Creating Python virtual environment..."
	@$(PYTHON) -m venv $(VENV)
	@echo "✓ Virtual environment created at $(VENV)"
	@echo ""
	@echo "To activate manually:"
	@echo "  source $(VENV)/bin/activate"
	@echo ""

# Install dependencies in virtual environment
install: venv
	@echo "Installing Python dependencies..."
	@$(VENV_BIN)/pip install --upgrade pip
	@$(VENV_BIN)/pip install -r $(SCRIPTS_DIR)/requirements.txt
	@echo "✓ Dependencies installed"
	@echo ""

# Development setup (venv + install)
dev: install
	@echo "✓ Development environment ready!"
	@echo ""
	@echo "To activate virtual environment:"
	@echo "  source $(VENV)/bin/activate"
	@echo ""
	@echo "To run tests:"
	@echo "  make test"
	@echo ""

# Run Python unit tests
test:
	@if [ ! -d "$(VENV)" ]; then \
		echo "❌ Virtual environment not found. Run 'make dev' first."; \
		exit 1; \
	fi
	@echo "Running unit tests..."
	@cd $(SCRIPTS_DIR) && ../../$(VENV_BIN)/python test_merge_config.py
	@echo "✓ Tests completed"

# Test configuration merge locally
merge:
	@if [ ! -d "$(VENV)" ]; then \
		echo "❌ Virtual environment not found. Run 'make dev' first."; \
		exit 1; \
	fi
	@if [ ! -f "$(PROJECT_YML)" ]; then \
		echo "❌ $(PROJECT_YML) not found"; \
		exit 1; \
	fi
	@echo "Testing configuration merge..."
	@mkdir -p /tmp
	@cp $(PROJECT_YML) /tmp/project.yml
	@if [ -f "$(DEFAULTS_YML)" ]; then \
		cd ansible && ../$(VENV_BIN)/python scripts/merge_config.py; \
	else \
		echo "⚠ Warning: $(DEFAULTS_YML) not found, using project.yml only"; \
		cd ansible && ../$(VENV_BIN)/python scripts/merge_config.py; \
	fi
	@if [ -f "/tmp/merged_config.yml" ]; then \
		echo ""; \
		echo "✓ Merge successful! Output:"; \
		cat /tmp/merged_config.yml; \
	fi

# Run Python linter
lint:
	@if [ ! -d "$(VENV)" ]; then \
		echo "❌ Virtual environment not found. Run 'make dev' first."; \
		exit 1; \
	fi
	@echo "Running Python linter..."
	@$(VENV_BIN)/pip install flake8 -q
	@$(VENV_BIN)/flake8 $(SCRIPTS_DIR)/*.py --max-line-length=120 --exclude=$(VENV) || true
	@echo "✓ Linting completed"

# Format Python code
format:
	@if [ ! -d "$(VENV)" ]; then \
		echo "❌ Virtual environment not found. Run 'make dev' first."; \
		exit 1; \
	fi
	@echo "Formatting Python code..."
	@$(VENV_BIN)/pip install black -q
	@$(VENV_BIN)/black $(SCRIPTS_DIR)/*.py
	@echo "✓ Code formatted"

# Check if required dependencies are available
check-deps:
	@echo "Checking dependencies..."
	@command -v $(PYTHON) >/dev/null 2>&1 || { echo "❌ python3 not found"; exit 1; }
	@$(PYTHON) --version
	@echo "✓ Python is available"
	@if [ -d "$(VENV)" ]; then \
		echo "✓ Virtual environment exists"; \
		$(VENV_BIN)/pip list | grep PyYAML && echo "✓ PyYAML installed" || echo "⚠ PyYAML not installed"; \
	else \
		echo "⚠ Virtual environment not created yet"; \
	fi
	@echo ""

# Clean up virtual environment and cache files
clean:
	@echo "Cleaning up..."
	@rm -rf $(VENV)
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@find . -type f -name "*.pyo" -delete 2>/dev/null || true
	@find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	@rm -f /tmp/merged_config.yml 2>/dev/null || true
	@echo "✓ Cleanup completed"

# Run full development setup and tests
all: clean dev test
	@echo ""
	@echo "======================================================================"
	@echo "✓ All tasks completed successfully!"
	@echo "======================================================================"
	@echo ""
