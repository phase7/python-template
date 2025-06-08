# Python Template

A modern Python template library for miscellaneous operations and tools, built with contemporary development practices and comprehensive tooling.

## Features

- **Modern Python**: Built for Python 3.12+ with full type hints
- **Quality Tooling**: Integrated ruff (formatting/linting), typos (type checking), pytest (testing)
- **Development Workflow**: Comprehensive Makefile with helpful commands
- **Functional Programming**: Emphasizes simple, testable functions over complex classes
- **CLI Interface**: Built-in command-line interface using Click
- **Configuration Management**: Environment-based settings with Pydantic
- **Comprehensive Testing**: Test-driven development with >85% coverage requirement
- **Pre-commit Hooks**: Automated quality gates before commits

## Quick Start

### Prerequisites

- Python 3.12+
- [uv](https://github.com/astral-sh/uv) (modern Python package manager)

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd python-template

# Set up development environment
make dev
```

### Basic Usage

```bash
# Run the application
make run

# Run with custom data
uv run python -m python_template --data "your_data"

# Run with debug logging
uv run python -m python_template --debug

# Show help
uv run python -m python_template --help
```

### Development Commands

```bash
# Show all available commands
make help

# Run tests
make test

# Run all quality checks
make all-checks

# Format code
make format

# Run linting
make lint

# Type checking
make type-check

# Build package
make build

# Clean artifacts
make clean
```

## Project Structure

```
python-template/
├── Makefile                 # Development workflow commands
├── pyproject.toml          # Project configuration and dependencies
├── .pre-commit-config.yaml # Pre-commit hooks configuration
├── README.md               # This file
├── docs/                   # Documentation and changelogs
│   ├── CHANGELOG.md        # Project changelog
│   └── copilot-changes/    # AI-generated change summaries
├── python_template/        # Main package directory
│   ├── __init__.py         # Package initialization
│   ├── __main__.py         # Module execution entry point
│   └── main.py             # Main application logic
└── tests/                  # Test suite
    ├── __init__.py
    └── test_main.py
```

## Usage Examples

### Command Line Interface

```bash
# Basic usage
python -m python_template

# Process custom data
python -m python_template --data "hello world"

# Enable debug logging
python -m python_template --debug --data "test"
```

### Programmatic Usage

```python
from python_template import main
from python_template.main import process_data, validate_input

# Direct function usage
result = process_data("sample data")
print(f"Status: {result['status']}")
print(f"Processed: {result['processed']}")

# Input validation
if validate_input("user_input"):
    result = process_data("user_input")

# Run main application
main()
```

## Development

### Setting Up Development Environment

```bash
# Install all dependencies and set up pre-commit hooks
make dev

# Or step by step:
uv sync --dev
uv run pre-commit install
```

### Running Tests

```bash
# Run tests with coverage
make test

# Run tests with verbose output
make test-verbose

# Generate HTML coverage report
make test-coverage
```

### Code Quality

```bash
# Run all quality checks
make all-checks

# Individual checks
make format      # Format code
make lint        # Run linting
```

### Adding Dependencies

```bash
# Add runtime dependency
uv add <package-name>

# Add development dependency
uv add --dev <package-name>

# Update dependencies
make update-deps
```

## Architecture

This template follows functional programming principles with an emphasis on:

- **Simple Functions**: One function, one responsibility
- **Immutable Data**: Prefer immutable types and functional transformations
- **Pure Functions**: Minimize side effects for easier testing
- **Module Organization**: Group related functions in modules rather than classes
- **Type Safety**: Full type hints for better code quality and IDE support

### Core Components

- **`main.py`**: Core application logic with CLI interface
- **`Settings`**: Environment-based configuration using Pydantic
- **`process_data()`**: Example data processing function
- **`validate_input()`**: Input validation with business rules
- **CLI**: Click-based command-line interface

## Testing

The project uses pytest with comprehensive testing patterns:

- **Unit Tests**: Test individual functions in isolation
- **Integration Tests**: Test complete workflows
- **Parametrized Tests**: Test multiple inputs efficiently
- **Mocking**: Mock external dependencies
- **Coverage**: Maintain >85% test coverage

### Test Structure

```python
# Example test patterns used in this project
def test_function_with_valid_input():
    """Test function behavior with valid input."""
    result = my_function("valid_input")
    assert result["status"] == "success"

@pytest.mark.parametrize("input_value,expected", [
    ("valid", True),
    ("", False),
])
def test_function_parametrized(input_value, expected):
    """Test function with multiple inputs."""
    assert my_function(input_value) == expected
```

## Configuration

Configuration is handled through environment variables with sensible defaults:

```bash
# Environment variables (optional)
export PYTHON_TEMPLATE_LOG_LEVEL=DEBUG
export PYTHON_TEMPLATE_DEBUG=true
```

## Contributing

1. **Fork and Clone**: Fork the repository and clone your fork
2. **Set Up Environment**: Run `make dev` to set up development environment
3. **Create Feature Branch**: `git checkout -b feature/your-feature`
4. **Write Tests First**: Follow TDD practices
5. **Implement Feature**: Write the minimal code to make tests pass
6. **Quality Checks**: Run `make all-checks` to ensure code quality
7. **Commit Changes**: Use conventional commit messages
8. **Submit PR**: Create a pull request with clear description

### Code Style

- Follow PEP 8 with 88-character line length
- Use type hints for all functions and methods
- Write Google-style docstrings
- Prefer functional programming patterns
- Maintain >85% test coverage

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Changelog

See [CHANGELOG.md](docs/CHANGELOG.md) for a detailed history of changes.

## Support

For questions, issues, or contributions, please:

1. Check existing issues
2. Create a new issue with detailed description
3. Follow the contributing guidelines above
