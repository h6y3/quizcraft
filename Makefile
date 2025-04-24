.PHONY: setup test clean run-extract

# Default Python interpreter
PYTHON := python3

# Virtual environment commands
VENV_DIR := venv
VENV_ACTIVATE := $(VENV_DIR)/bin/activate
VENV_PYTHON := $(VENV_DIR)/bin/python

# Path to sample PDF
SAMPLE_PDF := samples/sample.pdf

# Set up development environment
setup:
	$(PYTHON) -m venv $(VENV_DIR)
	. $(VENV_ACTIVATE) && pip install -e .

# Run tests
test:
	. $(VENV_ACTIVATE) && python -m unittest discover tests

# Clean up temporary files
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	find . -name "__pycache__" -exec rm -rf {} +
	find . -name "*.pyc" -delete

# Run extraction on sample PDF
run-extract:
	. $(VENV_ACTIVATE) && quizcraft extract $(SAMPLE_PDF) --segment

# Run extraction and save to file
run-extract-save:
	. $(VENV_ACTIVATE) && quizcraft extract $(SAMPLE_PDF) --segment --output samples/output.json

# Help command
help:
	@echo "Available commands:"
	@echo "  make setup          Setup development environment"
	@echo "  make test           Run unit tests"
	@echo "  make clean          Clean temporary files"
	@echo "  make run-extract    Run extraction on sample PDF"
	@echo "  make run-extract-save Run extraction and save to file"