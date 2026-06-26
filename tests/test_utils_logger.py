"""Logger utility tests."""

from logging import DEBUG, Logger
from logging.handlers import RotatingFileHandler
from pathlib import Path

import pytest
from _pytest.capture import CaptureFixture

from ai_stock_analyzer.config import LoggingSettings
from ai_stock_analyzer.utils import configure_logger


def test_configure_logger_creates_console_and_file_handlers(
    tmp_path: Path,
) -> None:
    """Verify logger configuration creates console and file handlers."""
    settings = _create_logging_settings(file_path=tmp_path / "application.log")

    logger = configure_logger(
        name="tests.logger.full",
        settings=settings,
    )

    assert isinstance(logger, Logger)
    assert logger.level == DEBUG
    assert len(logger.handlers) == 2


def test_configure_logger_writes_to_configured_log_directory(
    tmp_path: Path,
) -> None:
    """Verify file logging writes to the configured directory."""
    log_file = tmp_path / "nested" / "test.log"
    settings = _create_logging_settings(
        file_path=log_file,
        enable_console=False,
    )

    logger = configure_logger(
        name="tests.logger.file",
        settings=settings,
    )

    logger.info("hello")

    assert log_file.exists()
    assert "hello" in log_file.read_text(encoding="utf-8")


def test_configure_logger_writes_to_console(
    tmp_path: Path,
    capsys: CaptureFixture[str],
) -> None:
    """Verify console logging writes output."""
    settings = _create_logging_settings(
        file_path=tmp_path / "application.log",
        enable_file=False,
    )

    logger = configure_logger(
        name="tests.logger.console",
        settings=settings,
    )

    logger.info("console message")
    captured = capsys.readouterr()

    assert "console message" in captured.err


def test_configure_logger_uses_rotation_settings(tmp_path: Path) -> None:
    """Verify rotating file handler receives configured rotation settings."""
    settings = _create_logging_settings(
        file_path=tmp_path / "application.log",
        max_bytes=128,
        backup_count=3,
        enable_console=False,
    )

    logger = configure_logger(
        name="tests.logger.rotation",
        settings=settings,
    )

    file_handler = next(
        handler
        for handler in logger.handlers
        if isinstance(handler, RotatingFileHandler)
    )

    assert file_handler.maxBytes == 128
    assert file_handler.backupCount == 3


def test_configure_logger_rejects_unsupported_log_level(tmp_path: Path) -> None:
    """Verify unsupported string log levels raise ValueError."""
    settings = _create_logging_settings(
        file_path=tmp_path / "application.log",
        level="INVALID",
    )

    with pytest.raises(ValueError, match="Unsupported log level"):
        configure_logger(
            name="tests.logger.invalid",
            settings=settings,
        )


def _create_logging_settings(
    file_path: Path,
    *,
    level: str = "DEBUG",
    log_format: str = "%(levelname)s:%(name)s:%(message)s",
    max_bytes: int = 1_024,
    backup_count: int = 2,
    enable_console: bool = True,
    enable_file: bool = True,
) -> LoggingSettings:
    """Create logging settings for tests.

    Args:
        file_path: Log file path.
        level: Logging level name.
        log_format: Logging formatter pattern.
        max_bytes: Maximum bytes per log file before rotation.
        backup_count: Number of rotated log files to retain.
        enable_console: Whether console logging is enabled.
        enable_file: Whether rotating file logging is enabled.

    Returns:
        Logging settings instance.
    """
    return LoggingSettings(
        level=level,
        format=log_format,
        file_path=file_path,
        max_bytes=max_bytes,
        backup_count=backup_count,
        enable_console=enable_console,
        enable_file=enable_file,
    )
