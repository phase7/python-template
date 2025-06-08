"""Tests for the main module functionality.

This module contains comprehensive tests for the main application logic,
following TDD principles and ensuring high test coverage.
"""

import logging
from unittest.mock import MagicMock, patch

import pytest
from click.testing import CliRunner

from python_template.main import (
    Settings,
    cli,
    main,
    process_data,
    setup_logging,
    validate_input,
)


class TestProcessData:
    """Test cases for the process_data function."""

    def test_process_data_with_string_input(self):
        """Test processing with valid string input."""
        result = process_data("hello")

        assert result["status"] == "success"
        assert result["input"] == "hello"
        assert result["processed"] == "HELLO"
        assert "timestamp" in result

    def test_process_data_with_none_input(self):
        """Test processing with None input uses default."""
        result = process_data(None)

        assert result["status"] == "success"
        assert result["input"] == "default"
        assert result["processed"] == "DEFAULT"

    def test_process_data_with_empty_string(self):
        """Test processing with empty string."""
        result = process_data("")

        assert result["status"] == "success"
        assert result["input"] == ""
        assert result["processed"] == ""

    def test_process_data_with_numeric_input(self):
        """Test processing with numeric input."""
        result = process_data(123)

        assert result["status"] == "success"
        assert result["input"] == 123
        assert result["processed"] == "123"

    @patch("python_template.main.logging.getLogger")
    def test_process_data_logging(self, mock_get_logger):
        """Test that processing data logs correctly."""
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger

        process_data("test")

        mock_logger.info.assert_called_with("Processing data: test")


class TestValidateInput:
    """Test cases for the validate_input function."""

    def test_validate_input_with_valid_string(self):
        """Test validation with valid string."""
        assert validate_input("valid_input") is True

    def test_validate_input_with_empty_string(self):
        """Test validation with empty string."""
        assert validate_input("") is False

    def test_validate_input_with_whitespace_only(self):
        """Test validation with whitespace-only string."""
        assert validate_input("   ") is False

    def test_validate_input_with_valid_string_with_spaces(self):
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
    def test_validate_input_parametrized(self, input_value, expected):
        """Test validation with multiple inputs using parametrize."""
        assert validate_input(input_value) is expected


class TestSetupLogging:
    """Test cases for the setup_logging function."""

    @patch("python_template.main.logging.basicConfig")
    def test_setup_logging_default_level(self, mock_basic_config):
        """Test logging setup with default level."""
        setup_logging()

        mock_basic_config.assert_called_once()
        call_args = mock_basic_config.call_args
        assert call_args[1]["level"] == logging.INFO

    @patch("python_template.main.logging.basicConfig")
    def test_setup_logging_custom_level(self, mock_basic_config):
        """Test logging setup with custom level."""
        setup_logging("DEBUG")

        mock_basic_config.assert_called_once()
        call_args = mock_basic_config.call_args
        assert call_args[1]["level"] == logging.DEBUG

    @patch("python_template.main.logging.basicConfig")
    def test_setup_logging_invalid_level(self, mock_basic_config):
        """Test logging setup with invalid level defaults to INFO."""
        setup_logging("INVALID")

        mock_basic_config.assert_called_once()
        call_args = mock_basic_config.call_args
        # Should default to INFO level for invalid levels
        assert call_args[1]["level"] == logging.INFO


class TestSettings:
    """Test cases for the Settings class."""

    def test_settings_default_values(self):
        """Test settings with default values."""
        settings = Settings()

        assert settings.log_level == "INFO"
        assert settings.debug is False

    @patch.dict("os.environ", {"PYTHON_TEMPLATE_LOG_LEVEL": "DEBUG"})
    def test_settings_environment_variables(self):
        """Test settings with environment variables."""
        settings = Settings()

        assert settings.log_level == "DEBUG"

    @patch.dict("os.environ", {"PYTHON_TEMPLATE_DEBUG": "true"})
    def test_settings_debug_from_env(self):
        """Test debug setting from environment variable."""
        settings = Settings()

        assert settings.debug is True


class TestCLI:
    """Test cases for the CLI interface."""

    def test_cli_default_execution(self):
        """Test CLI with default parameters."""
        runner = CliRunner()
        result = runner.invoke(cli, [])

        assert result.exit_code == 0
        assert "Python Template Application" in result.output
        assert "Status: success" in result.output

    def test_cli_with_data_parameter(self):
        """Test CLI with data parameter."""
        runner = CliRunner()
        result = runner.invoke(cli, ["--data", "test_data"])

        assert result.exit_code == 0
        assert "Input: test_data" in result.output
        assert "Processed: TEST_DATA" in result.output

    def test_cli_with_debug_flag(self):
        """Test CLI with debug flag."""
        runner = CliRunner()
        result = runner.invoke(cli, ["--debug"])

        assert result.exit_code == 0
        assert "Status: success" in result.output

    def test_cli_with_empty_data(self):
        """Test CLI with empty data parameter."""
        runner = CliRunner()
        result = runner.invoke(cli, ["--data", ""])

        assert result.exit_code == 0
        assert "Error: Invalid input provided" in result.output

    def test_cli_with_whitespace_data(self):
        """Test CLI with whitespace-only data."""
        runner = CliRunner()
        result = runner.invoke(cli, ["--data", "   "])

        assert result.exit_code == 0
        assert "Error: Invalid input provided" in result.output


class TestMainFunction:
    """Test cases for the main function."""

    @patch("python_template.main.cli")
    def test_main_calls_cli(self, mock_cli):
        """Test that main function calls CLI."""
        main()

        mock_cli.assert_called_once()


class TestIntegration:
    """Integration tests for the complete workflow."""

    def test_full_workflow_success(self):
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

    def test_full_workflow_failure(self):
        """Test complete workflow with invalid input."""
        data = ""

        # Validate input
        assert validate_input(data) is False

        # Even invalid input can be processed (validation is separate)
        result = process_data(data)
        assert result["status"] == "success"  # Processing doesn't fail

    @patch("python_template.main.logging.getLogger")
    def test_error_handling_and_logging(self, mock_get_logger):
        """Test error handling and logging integration."""
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger

        # Test with valid data
        process_data("test")

        # Verify logging was called
        mock_logger.info.assert_called_with("Processing data: test")


# Fixtures for test setup
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


# Test coverage helpers
def test_module_imports():
    """Test that all required modules can be imported."""
    from python_template.main import (
        Settings,
        cli,
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
