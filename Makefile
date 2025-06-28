# Variables
PYTHON := python
PIP := pip
PYTEST := pytest

# Default target
.DEFAULT_GOAL := help

# Colors
BLUE := \033[34m
GREEN := \033[32m
NC := \033[0m

# Help
.PHONY: help
help: ## Show available commands
	@echo "$(BLUE)ETL Project Commands$(NC)"
	@echo "===================="
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "$(GREEN)%-15s$(NC) %s\n", $$1, $$2}' $(MAKEFILE_LIST)

# Install dependencies
.PHONY: install
install: ## Install project dependencies
	$(PIP) install -r requirements.txt

# Run tests
.PHONY: test
test: ## Run all tests
	$(PYTEST) tests/ -v

# Test coverage
.PHONY: coverage
coverage: ## Run tests with coverage report
	$(PYTEST) tests/ --cov=etl --cov-report=term-missing

# Test coverage HTML
.PHONY: coverage-html
coverage-html: ## Generate HTML coverage report
	$(PYTEST) tests/ --cov=etl --cov-report=html
	@echo "$(GREEN)HTML coverage report generated in htmlcov/index.html$(NC)"

# Test coverage HTML and open in browser
.PHONY: coverage-open
coverage-open: ## Generate HTML coverage report and open in browser
	$(PYTEST) tests/ --cov=etl --cov-report=html
	@echo "$(GREEN)Opening coverage report in browser...$(NC)"
	@if command -v xdg-open > /dev/null; then \
		xdg-open htmlcov/index.html; \
	elif command -v open > /dev/null; then \
		open htmlcov/index.html; \
	else \
		echo "$(BLUE)Please open htmlcov/index.html manually in your browser$(NC)"; \
	fi

# Lint code
.PHONY: lint
lint: ## Run code linting
	flake8 .

# Format code
.PHONY: format
format: ## Format code with black
	black .

# Execute ETL
.PHONY: run
run: ## Execute the ETL process
	$(PYTHON) main.py

# Clean files
.PHONY: clean
clean: ## Clean generated files
	rm -rf output/ htmlcov/ .coverage .pytest_cache/
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true 