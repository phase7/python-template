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


def test_process_data_with_string_input():
    """Test processing with valid string input."""
    result = process_data("hello")

    assert result["status"] == "success"
    assert result["input"] == "hello"
    assert result["processed"] == "HELLO"
    assert "timestamp" in result


def test_process_data_with_none_input():
    """Test processing with None input uses default."""
    result = process_data(None)

    assert result["status"] == "success"
    assert result["input"] == "default"
    assert result["processed"] == "DEFAULT"


def test_process_data_with_empty_string():
    """Test processing with empty string."""
    result = process_data("")

    assert result["status"] == "success"
    assert result["input"] == ""
    assert result["processed"] == ""


def test_process_data_with_numeric_input():
    """Test processing with numeric input."""
    result = process_data(123)

    assert result["status"] == "success"
    assert result["input"] == 123
    assert result["processed"] == "123"


@patch("python_template.main.logging.getLogger")
def test_process_data_logs_correctly(mock_get_logger):
    """Test that processing data logs correctly."""
    mock_logger = MagicMock()
    mock_get_logger.return_value = mock_logger

    process_data("test")

    mock_logger.info.assert_called_with("Processing data: test")


# ============================================================================
# validate_input() tests
# ============================================================================


def test_validate_input_with_valid_string():
    """Test validation with valid string."""
    assert validate_input("valid_input") is True


def test_validate_input_with_empty_string():
    """Test validation with empty string."""
    assert validate_input("") is False


def test_validate_input_with_whitespace_only():
    """Test validation with whitespace-only string."""
    assert validate_input("   ") is False


def test_validate_input_with_valid_string_with_spaces():
    """Test validation with valid string containing spaces."""
    assert validate_input("valid input with spaces") is True


@pytest.mark.parametrize(
    "input_value,expected",
    [
        ("test", True),
        ("", False),
        ("   ", False),
        ("a", True),
        ("test with spaces", True),
        ("\t\n", False),
    ],
)
def test_validate_input_parametrized(input_value, expected):
    """Test validation with multiple inputs using parametrize."""
    assert validate_input(input_value) is expected


# ============================================================================
# setup_logging() tests
# ============================================================================


@patch("python_template.main.logging.basicConfig")
def test_setup_logging_with_default_level(mock_basic_config):
    """Test logging setup with default level."""
    setup_logging()

    mock_basic_config.assert_called_once()
    call_args = mock_basic_config.call_args
    assert call_args[1]["level"] == logging.INFO


@patch("python_template.main.logging.basicConfig")
def test_setup_logging_with_custom_level(mock_basic_config):
    """Test logging setup with custom level."""
    setup_logging("DEBUG")

    mock_basic_config.assert_called_once()
    call_args = mock_basic_config.call_args
    assert call_args[1]["level"] == logging.DEBUG


@patch("python_template.main.logging.basicConfig")
def test_setup_logging_with_invalid_level_defaults_to_info(mock_basic_config):
    """Test logging setup with invalid level defaults to INFO."""
    setup_logging("INVALID")

    mock_basic_config.assert_called_once()
    call_args = mock_basic_config.call_args
    # Should default to INFO level for invalid levels
    assert call_args[1]["level"] == logging.INFO


# ============================================================================
# Settings class tests
# ============================================================================


def test_settings_with_default_values():
    """Test settings with default values."""
    settings = Settings()

    assert settings.log_level == "INFO"
    assert settings.debug is False


@patch.dict("os.environ", {"PYTHON_TEMPLATE_LOG_LEVEL": "DEBUG"})
def test_settings_with_environment_variables():
    """Test settings with environment variables."""
    settings = Settings()

    assert settings.log_level == "DEBUG"


@patch.dict("os.environ", {"PYTHON_TEMPLATE_DEBUG": "true"})
def test_settings_debug_from_environment():
    """Test debug setting from environment variable."""
    settings = Settings()

    assert settings.debug is True


# ============================================================================
# CLI interface tests
# ============================================================================


def test_cli_with_default_execution():
    """Test CLI with default parameters."""
    runner = CliRunner()
    result = runner.invoke(app, [])

    assert result.exit_code == 0
    assert "Python Template Application" in result.output
    assert "Status: success" in result.output


def test_cli_with_data_parameter():
    """Test CLI with data parameter."""
    runner = CliRunner()
    result = runner.invoke(app, ["--data", "test_data"])

    assert result.exit_code == 0
    assert "Input: test_data" in result.output
    assert "Processed: TEST_DATA" in result.output


def test_cli_with_debug_flag():
    """Test CLI with debug flag."""
    runner = CliRunner()
    result = runner.invoke(app, ["--debug"])

    assert result.exit_code == 0
    assert "Status: success" in result.output


def test_cli_with_empty_data():
    """Test CLI with empty data parameter."""
    runner = CliRunner()
    result = runner.invoke(app, ["--data", ""])

    assert result.exit_code == 0
    assert "Error: Invalid input provided" in result.output


def test_cli_with_whitespace_data():
    """Test CLI with whitespace-only data."""
    runner = CliRunner()
    result = runner.invoke(app, ["--data", "   "])

    assert result.exit_code == 0
    assert "Error: Invalid input provided" in result.output


# ============================================================================
# main() function tests
# ============================================================================


@patch("python_template.main.app")
def test_main_calls_app(mock_app):
    """Test that main function calls Typer app."""
    main()

    mock_app.assert_called_once()


# ============================================================================
# Integration tests
# ============================================================================


def test_full_workflow_success():
    """Test complete workflow from input to output."""
    # Test the full pipeline
    data = "integration_test"

    # Validate input
    assert validate_input(data) is True

    # Process data
    result = process_data(data)

    # Verify result
    assert result["status"] == "success"
    assert result["input"] == data
    assert result["processed"] == data.upper()


def test_full_workflow_with_invalid_input():
    """Test complete workflow with invalid input."""
    data = ""

    # Validate input
    assert validate_input(data) is False

    # Even invalid input can be processed (validation is separate)
    result = process_data(data)
    assert result["status"] == "success"  # Processing doesn't fail


@patch("python_template.main.logging.getLogger")
def test_error_handling_and_logging_integration(mock_get_logger):
    """Test error handling and logging integration."""
    mock_logger = MagicMock()
    mock_get_logger.return_value = mock_logger

    # Test with valid data
    process_data("test")

    # Verify logging was called
    mock_logger.info.assert_called_with("Processing data: test")


# ============================================================================
# Fixtures
# ============================================================================


@pytest.fixture
def sample_data():
    """Provide sample data for tests."""
    return {
        "valid_string": "test_data",
        "empty_string": "",
        "whitespace": "   ",
        "numeric": 123,
        "none_value": None,
    }


@pytest.fixture
def cli_runner():
    """Provide CLI runner for tests."""
    return CliRunner()


# ============================================================================
# Module import tests
# ============================================================================


def test_module_imports():
    """Test that all required modules can be imported."""
    from python_template.main import (
        Settings,
        main,
        process_data,
        setup_logging,
        validate_input,
    )

    # Verify functions are callable
    assert callable(process_data)
    assert callable(validate_input)
    assert callable(setup_logging)
    assert callable(cli)
    assert callable(main)
    assert callable(Settings)
