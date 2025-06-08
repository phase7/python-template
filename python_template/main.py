"""Main application logic for python_template package.

This module contains the core functionality and serves as the main entry point
for the application. It follows functional programming principles with simple,
testable functions.
"""

import logging

import click
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings with environment variable support."""

    log_level: str = "INFO"
    debug: bool = False

    model_config = {"env_prefix": "PYTHON_TEMPLATE_"}


def setup_logging(level: str = "INFO") -> None:
    """Set up structured logging for the application.

    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    """
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def process_data(data: str | None = None) -> dict:
    """Process input data and return structured result.

    This is an example function demonstrating the functional programming
    approach preferred in this template.

    Args:
        data: Optional input data to process

    Returns:
        Dictionary containing processed result

    Examples:
        >>> result = process_data("test")
        >>> result["status"]
        "success"
    """
    logger = logging.getLogger(__name__)

    if data is None:
        logger.info("No data provided, using default")
        data = "default"

    logger.info(f"Processing data: {data}")

    return {
        "status": "success",
        "input": data,
        "processed": data.upper() if isinstance(data, str) else str(data),
        "timestamp": "2025-06-08T00:00:00Z",  # In real app, use datetime.utcnow()
    }


def validate_input(input_value: str) -> bool:
    """Validate input according to business rules.

    Args:
        input_value: The input string to validate

    Returns:
        True if valid, False otherwise

    Examples:
        >>> validate_input("valid_input")
        True
        >>> validate_input("")
        False
    """
    return bool(input_value and len(input_value.strip()) > 0)


@click.command()
@click.option("--data", default=None, help="Data to process")
@click.option("--debug", is_flag=True, help="Enable debug logging")
def cli(data: str | None, debug: bool) -> None:
    """Python Template CLI - A template for Python CLI applications.

    This command demonstrates the basic structure and patterns used
    in this Python template project.
    """
    settings = Settings(debug=debug)
    log_level = "DEBUG" if settings.debug else settings.log_level
    setup_logging(log_level)

    logger = logging.getLogger(__name__)
    logger.info("Starting python_template application")

    if data is not None and not validate_input(data):
        logger.error("Invalid input provided")
        click.echo("Error: Invalid input provided", err=True)
        return

    try:
        result = process_data(data)
        logger.info("Processing completed successfully")

        click.echo("Python Template Application")
        click.echo(f"Status: {result['status']}")
        click.echo(f"Input: {result['input']}")
        click.echo(f"Processed: {result['processed']}")
        click.echo(f"Timestamp: {result['timestamp']}")

    except Exception as e:
        logger.error(f"Processing failed: {e}")
        click.echo(f"Error: {e}", err=True)


def main() -> None:
    """Main entry point for the application.

    This function serves as the primary entry point and can be called
    directly or through the CLI interface.
    """
    cli()


if __name__ == "__main__":
    main()
