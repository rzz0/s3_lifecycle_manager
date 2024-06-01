# Variables
VENV_DIR = .venv
PYTHON = $(VENV_DIR)/bin/python
PIP = $(VENV_DIR)/bin/pip
PYTEST = $(VENV_DIR)/bin/pytest
PYLINT = $(VENV_DIR)/bin/pylint
BLACK = $(VENV_DIR)/bin/black
BANDIT = $(VENV_DIR)/bin/bandit
REQUIREMENTS = requirements.txt


# Targets
all: install test

# Setup virtual environment and install dependencies
$(VENV_DIR)/bin/activate: $(REQUIREMENTS)
	python3 -m venv $(VENV_DIR)
	$(PIP) install --upgrade pip
	$(PIP) install -r $(REQUIREMENTS)

install: $(VENV_DIR)/bin/activate

# Run tests
test: $(VENV_DIR)/bin/activate
	PYTHONPATH=src $(PYTEST) -v

# Clean the environment
clean:
	rm -rf $(VENV_DIR)
	find . -type d -name "__pycache__" -exec rm -r {} +

# Format the code
format: $(VENV_DIR)/bin/activate
	$(BLACK) .

# Static code analysis
lint: $(VENV_DIR)/bin/activate
	PYTHONPATH=src $(PYLINT) src tests

# Security check
security: $(VENV_DIR)/bin/activate
	PYTHONPATH=src $(BANDIT) -r src

# Update dependencies
update: $(VENV_DIR)/bin/activate
	$(PIP) install --upgrade -r $(REQUIREMENTS)

.PHONY: all install test clean format lint security update
