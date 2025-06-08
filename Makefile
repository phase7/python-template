# Development workflow commands
.DEFAULT_GOAL := help

# Variables
PYTHON := python
UV := uv
PACKAGE_NAME := python_template

# Colors for output
BLUE := \033[36m
GREEN := \033[32m
YELLOW := \033[33m
RED := \033[31m
RESET := \033[0m

.PHONY: help
help: ## Show this help message
	@echo "$(BLUE)Available commands:$(RESET)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(GREEN)%-20s$(RESET) %s\n", $$1, $$2}'

.PHONY: dev
dev: ## Set up complete development environment
	@echo "$(BLUE)Setting up development environment...$(RESET)"
	$(UV) sync --dev
	$(UV) run pre-commit install
	@echo "$(GREEN)Development environment ready!$(RESET)"

.PHONY: install
install: ## Install package dependencies
	@echo "$(BLUE)Installing dependencies...$(RESET)"
	$(UV) sync

.PHONY: install-dev
install-dev: ## Install development dependencies
	@echo "$(BLUE)Installing development dependencies...$(RESET)"
	$(UV) sync --dev

.PHONY: test
test: ## Run tests
	@echo "$(BLUE)Running tests...$(RESET)"
	$(UV) run pytest

.PHONY: test-verbose
test-verbose: ## Run tests with verbose output
	@echo "$(BLUE)Running tests (verbose)...$(RESET)"
	$(UV) run pytest -v

.PHONY: test-coverage
test-coverage: ## Run tests with coverage report
	@echo "$(BLUE)Running tests with coverage...$(RESET)"
	$(UV) run pytest --cov-report=html --cov-report=term

.PHONY: format
format: ## Format code with ruff
	@echo "$(BLUE)Formatting code...$(RESET)"
	$(UV) run ruff format .

.PHONY: format-check
format-check: ## Check code formatting
	@echo "$(BLUE)Checking code formatting...$(RESET)"
	$(UV) run ruff format --check .

.PHONY: lint
lint: ## Run ruff linting
	@echo "$(BLUE)Running ruff linting...$(RESET)"
	$(UV) run ruff check .

.PHONY: lint-fix
lint-fix: ## Run ruff linting with auto-fix
	@echo "$(BLUE)Running ruff linting with auto-fix...$(RESET)"
	$(UV) run ruff check --fix .

.PHONY: all-checks
all-checks: format-check lint test check-version ## Run all quality checks
	@echo "$(GREEN)All checks passed!$(RESET)"

.PHONY: pre-commit
pre-commit: ## Run pre-commit hooks
	@echo "$(BLUE)Running pre-commit hooks...$(RESET)"
	$(UV) run pre-commit run --all-files

.PHONY: pre-commit-install
pre-commit-install: ## Install pre-commit hooks
	@echo "$(BLUE)Installing pre-commit hooks...$(RESET)"
	$(UV) run pre-commit install

.PHONY: run
run: ## Run the application
	@echo "$(BLUE)Running application...$(RESET)"
	$(UV) run python -m $(PACKAGE_NAME)

.PHONY: run-direct
run-direct: ## Run application via direct import
	@echo "$(BLUE)Running application (direct import)...$(RESET)"
	$(UV) run python -c "import $(PACKAGE_NAME); $(PACKAGE_NAME).main()"

.PHONY: build
build: ## Build the package
	@echo "$(BLUE)Building package...$(RESET)"
	$(UV) build

.PHONY: clean
clean: ## Clean up artifacts
	@echo "$(BLUE)Cleaning up...$(RESET)"
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf htmlcov/
	rm -rf .coverage
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

.PHONY: clean-all
clean-all: clean ## Clean up everything including virtual environment
	@echo "$(BLUE)Cleaning everything...$(RESET)"
	rm -rf .venv/

.PHONY: update-deps
update-deps: ## Update dependencies
	@echo "$(BLUE)Updating dependencies...$(RESET)"
	$(UV) lock --upgrade

.PHONY: check-deps
check-deps: ## Check for dependency issues
	@echo "$(BLUE)Checking dependencies...$(RESET)"
	$(UV) tree

.PHONY: shell
shell: ## Open development shell
	@echo "$(BLUE)Opening development shell...$(RESET)"
	$(UV) shell

.PHONY: info
info: ## Show project information
	@echo "$(BLUE)Project Information:$(RESET)"
	@echo "Package: $(PACKAGE_NAME)"
	@echo "Python: $(shell $(PYTHON) --version)"
	@echo "UV: $(shell $(UV) --version)"
	@echo "Current directory: $(shell pwd)"

.PHONY: check-version
check-version: ## Check version consistency across all project files
	@echo "$(BLUE)Checking version consistency...$(RESET)"
	$(UV) run python scripts/check_version.py
