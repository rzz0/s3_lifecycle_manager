# Variables
VENV_DIR = .venv
PYTHON = $(VENV_DIR)/bin/python
PIP = $(VENV_DIR)/bin/pip
PYTEST = $(VENV_DIR)/bin/pytest
PYLINT = $(VENV_DIR)/bin/pylint
BLACK = $(VENV_DIR)/bin/black
BANDIT = $(VENV_DIR)/bin/bandit
REQUIREMENTS = requirements.txt
SETUP = setup.py

# Targets
all: install test

# Setup virtual environment and install dependencies
$(VENV_DIR)/bin/activate: $(REQUIREMENTS) $(SETUP)
	@echo "Setting up virtual environment..."
	python3 -m venv $(VENV_DIR)
	. $(VENV_DIR)/bin/activate && $(PIP) install --upgrade pip
	. $(VENV_DIR)/bin/activate && $(PIP) install -r $(REQUIREMENTS)
	. $(VENV_DIR)/bin/activate && $(PIP) install .
	@echo "Virtual environment and dependencies are set up."

install: $(VENV_DIR)/bin/activate

# Run tests
test: $(VENV_DIR)/bin/activate
	@echo "Running tests..."
	PYTHONPATH=src $(PYTEST) -v

# Clean the environment
clean:
	@echo "Cleaning up environment..."
	rm -rf $(VENV_DIR)
	rm -rf build/
	rm -rf dist/
	find . -type d -name "*.egg-info" -exec rm -r {} +
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type d -name ".pytest_cache" -exec rm -r {} +

# Format the code
format: $(VENV_DIR)/bin/activate
	@echo "Formatting code..."
	$(BLACK) .

# Static code analysis
lint: $(VENV_DIR)/bin/activate
	@echo "Running linting..."
	PYTHONPATH=src $(PYLINT) --fail-under=9.7 src tests

# Security check
security: $(VENV_DIR)/bin/activate
	@echo "Running security check..."
	PYTHONPATH=src $(BANDIT) -r src

# Update dependencies
update: $(VENV_DIR)/bin/activate
	@echo "Updating dependencies..."
	$(PIP) install --upgrade -r $(REQUIREMENTS)

.PHONY: all install test clean format lint security update
