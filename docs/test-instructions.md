# Test Instructions

This document outlines the testing standards and best practices for the Python Template project.

## Testing Philosophy

This project follows **function-based testing** aligned with the overall functional programming paradigm. Tests should be simple, focused, and easy to understand.

## Test Structure Guidelines

### Function-Based Tests (Preferred)

- **Use function-based tests** rather than class-based tests
- Each test function should test one specific behavior or scenario
- Test function names should follow the pattern: `test_<function_name>_<scenario>_<expected_result>`
- Group related tests using descriptive module-level comments or separators

### When to Use Classes

Classes should only be used for testing when:
- You need to share complex setup/teardown logic across multiple tests
- Testing class-based code that requires state management
- You have a large suite of tests that benefit from logical grouping with shared fixtures

### Test Organization

```python
# Preferred: Function-based tests
def test_process_data_with_valid_string():
    """Test processing with valid string input."""
    result = process_data("hello")

    assert result["status"] == "success"
    assert result["input"] == "hello"
    assert result["processed"] == "HELLO"

def test_process_data_with_empty_string():
    """Test processing with empty string input."""
    result = process_data("")

    assert result["status"] == "success"
    assert result["input"] == ""
    assert result["processed"] == ""

# Use separators for logical grouping
# ============================================================================
# validate_input() tests
# ============================================================================

def test_validate_input_with_valid_string():
    """Test validation with valid string."""
    assert validate_input("valid_input") is True

def test_validate_input_with_empty_string():
    """Test validation with empty string."""
    assert validate_input("") is False
```

## Test Naming Conventions

### Test Functions
- Start with `test_`
- Use descriptive names that explain what is being tested
- Format: `test_<function_name>_<condition>_<expected_outcome>`

Examples:
- `test_process_data_with_valid_input_returns_success()`
- `test_validate_input_with_empty_string_returns_false()`
- `test_setup_logging_with_invalid_level_defaults_to_info()`

### Test Files
- Name test files as `test_<module_name>.py`
- Place in `tests/` directory
- Mirror the source code structure

## Test Categories

### Unit Tests
- Test individual functions in isolation
- Mock external dependencies
- Focus on single responsibility

### Integration Tests
- Test complete workflows
- Test function interactions
- Use minimal mocking

### Parametrized Tests
- Use `@pytest.mark.parametrize` for testing multiple inputs
- Reduces code duplication
- Improves test coverage

Example:
```python
@pytest.mark.parametrize("input_value,expected", [
    ("valid", True),
    ("", False),
    ("   ", False),
    ("test with spaces", True),
])
def test_validate_input_parametrized(input_value, expected):
    """Test validation with multiple inputs using parametrize."""
    assert validate_input(input_value) is expected
```

## Fixtures and Setup

### Use Fixtures for Common Setup
```python
@pytest.fixture
def sample_data():
    """Provide sample data for tests."""
    return {
        "valid_string": "test_data",
        "empty_string": "",
        "numeric": 123,
    }

@pytest.fixture
def cli_runner():
    """Provide CLI runner for tests."""
    return CliRunner()
```

### Function-Level Setup
For simple setup, use function-level variables:
```python
def test_process_data_with_valid_input():
    """Test processing with valid input."""
    # Setup
    test_input = "hello_world"

    # Execute
    result = process_data(test_input)

    # Assert
    assert result["status"] == "success"
```

## Mocking Guidelines

### Mock External Dependencies
- Mock external APIs, databases, file systems
- Use `@patch` decorator for single mocks
- Use `patch.object()` for specific method mocking

```python
@patch("python_template.main.logging.getLogger")
def test_process_data_logs_correctly(mock_get_logger):
    """Test that processing data logs correctly."""
    mock_logger = MagicMock()
    mock_get_logger.return_value = mock_logger

    process_data("test")

    mock_logger.info.assert_called_with("Processing data: test")
```

### Environment Variable Mocking
```python
@patch.dict("os.environ", {"PYTHON_TEMPLATE_LOG_LEVEL": "DEBUG"})
def test_settings_with_environment_variables():
    """Test settings with environment variables."""
    settings = Settings()
    assert settings.log_level == "DEBUG"
```

## Assertion Guidelines

### Use Descriptive Assertions
- Prefer explicit assertions over generic ones
- Include custom error messages when helpful
- Test multiple aspects of the result

```python
def test_process_data_returns_complete_result():
    """Test that process_data returns all expected fields."""
    result = process_data("test")

    # Test multiple aspects
    assert result["status"] == "success"
    assert result["input"] == "test"
    assert result["processed"] == "TEST"
    assert "timestamp" in result
```

### Boolean Assertions
```python
# Preferred
assert validate_input("test") is True
assert validate_input("") is False

# Avoid
assert validate_input("test")
assert not validate_input("")
```

## Test Coverage Requirements

- Maintain >85% test coverage
- Focus on business logic coverage
- Test edge cases and error conditions
- Include both positive and negative test cases

## Test File Structure

```python
"""Tests for the main module functionality.

This module contains comprehensive tests for the main application logic,
following functional programming and TDD principles.
"""

import logging
from unittest.mock import MagicMock, patch

import pytest
from typer.testing import CliRunner

from python_template.main import (
    Settings,
    app,
    cli,
    main,
    process_data,
    setup_logging,
    validate_input,
)

# ============================================================================
# process_data() tests
# ============================================================================

def test_process_data_with_valid_string():
    """Test processing with valid string input."""
    # Test implementation here

# ============================================================================
# validate_input() tests
# ============================================================================

def test_validate_input_with_valid_string():
    """Test validation with valid string."""
    # Test implementation here

# ============================================================================
# Fixtures
# ============================================================================

@pytest.fixture
def sample_data():
    """Provide sample data for tests."""
    return {"test": "data"}
```

## Running Tests

### Development Testing
```bash
# Run all tests
make test

# Run with coverage
make test-cov

# Run specific test
pytest tests/test_main.py::test_process_data_with_valid_string

# Run tests matching pattern
pytest -k "process_data"
```

### Test-Driven Development (TDD)
1. **Red**: Write a failing test first
2. **Green**: Write minimal code to make the test pass
3. **Refactor**: Improve code while keeping tests green

## Common Patterns

### Testing CLI Applications
```python
def test_cli_with_valid_data():
    """Test CLI with valid data parameter."""
    runner = CliRunner()
    result = runner.invoke(app, ["--data", "test_data"])

    assert result.exit_code == 0
    assert "test_data" in result.output
```

### Testing Functions with Side Effects
```python
@patch("python_template.main.logging.basicConfig")
def test_setup_logging_calls_basic_config(mock_basic_config):
    """Test logging setup calls basicConfig."""
    setup_logging("INFO")

    mock_basic_config.assert_called_once()
    call_args = mock_basic_config.call_args
    assert call_args[1]["level"] == logging.INFO
```

### Testing Error Conditions
```python
def test_process_data_handles_none_input():
    """Test processing with None input uses default."""
    result = process_data(None)

    assert result["status"] == "success"
    assert result["input"] == "default"
    assert result["processed"] == "DEFAULT"
```

## Migration from Class-Based Tests

When converting class-based tests to function-based tests:

1. **Remove class definitions** and convert methods to functions
2. **Flatten test structure** - move tests to module level
3. **Add descriptive comments** to group related tests
4. **Preserve test logic** - keep assertions and mocking the same
5. **Update test names** to follow function naming conventions
6. **Convert class fixtures** to module-level fixtures if needed

This approach aligns with the project's functional programming philosophy and makes tests more straightforward and easier to maintain.
