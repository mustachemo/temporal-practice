"""Logging configuration and utilities."""

# ================================== Imports ================================== #
# Standard Library
import sys
from pathlib import Path
from typing import Optional

# Third-party
from loguru import logger
from rich.logging import RichHandler


# ================================== Functions ================================ #
def setup_logger(
    log_file: Optional[Path] = None,
    log_level: str = "INFO",
    enable_rich: bool = True,
    enable_json: bool = False,
) -> None:
    """Configure Loguru logger with rich console output and file logging.

    Args:
        log_file: Path to log file. If None, only console logging is enabled.
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL).
        enable_rich: Whether to use Rich for console formatting.
        enable_json: Whether to use JSON formatting for file logs.
    """
    # Remove default handler
    logger.remove()

    # Console handler with Rich formatting
    if enable_rich:
        logger.add(
            sys.stderr,
            level=log_level,
            format="{message}",
            enqueue=True,
            backtrace=True,
            colorize=True,
            handler=RichHandler(
                rich_tracebacks=True,
                show_path=False,
                markup=True,
            ),
        )
    else:
        logger.add(
            sys.stderr,
            level=log_level,
            format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} - {message}",
            enqueue=True,
            backtrace=True,
            colorize=True,
        )

    # File handler
    if log_file:
        log_file.parent.mkdir(parents=True, exist_ok=True)

        if enable_json:
            logger.add(
                log_file,
                level="DEBUG",
                rotation="10 MB",
                retention="30 days",
                enqueue=True,
                backtrace=True,
                serialize=True,  # JSON serialization
                format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level} | {name}:{function}:{line} | {message}",
            )
        else:
            logger.add(
                log_file,
                level="DEBUG",
                rotation="10 MB",
                retention="30 days",
                enqueue=True,
                backtrace=True,
                format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} - {message}",
            )

    logger.info("[bold green]Logger configured successfully[/bold green]")


def get_workflow_logger(workflow_id: str, workflow_type: str) -> logger:
    """Get a logger instance with workflow context.

    Args:
        workflow_id: Unique identifier for the workflow.
        workflow_type: Type of workflow being executed.

    Returns:
        Logger instance with workflow context.
    """
    return logger.bind(
        workflow_id=workflow_id, workflow_type=workflow_type, component="workflow"
    )


def get_activity_logger(activity_name: str, workflow_id: str) -> logger:
    """Get a logger instance with activity context.

    Args:
        activity_name: Name of the activity.
        workflow_id: ID of the parent workflow.

    Returns:
        Logger instance with activity context.
    """
    return logger.bind(
        activity_name=activity_name, workflow_id=workflow_id, component="activity"
    )
