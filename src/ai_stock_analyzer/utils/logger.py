"""Project logging utilities."""

from logging import (
    CRITICAL,
    DEBUG,
    ERROR,
    INFO,
    WARNING,
    Formatter,
    Logger,
    StreamHandler,
    getLogger,
)
from logging.handlers import RotatingFileHandler

from ai_stock_analyzer.config import LoggingSettings

LOG_LEVELS: dict[str, int] = {
    "CRITICAL": CRITICAL,
    "DEBUG": DEBUG,
    "ERROR": ERROR,
    "INFO": INFO,
    "WARNING": WARNING,
}


def configure_logger(
    name: str,
    settings: LoggingSettings,
) -> Logger:
    """Configure and return a project logger.

    Args:
        name: Logger name.
        settings: Logging configuration loaded from application config.

    Returns:
        The configured logger instance.
    """
    resolved_level = _resolve_log_level(settings.level)
    logger = getLogger(name)
    logger.setLevel(resolved_level)
    logger.propagate = False
    logger.handlers.clear()

    formatter = Formatter(settings.format)

    if settings.enable_console:
        console_handler = StreamHandler()
        console_handler.setLevel(resolved_level)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    if settings.enable_file:
        settings.file_path.parent.mkdir(parents=True, exist_ok=True)
        file_handler = RotatingFileHandler(
            filename=settings.file_path,
            maxBytes=settings.max_bytes,
            backupCount=settings.backup_count,
            encoding="utf-8",
        )
        file_handler.setLevel(resolved_level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


def _resolve_log_level(level: int | str) -> int:
    """Resolve a logging level value.

    Args:
        level: Logging level as an integer or level name.

    Returns:
        The integer logging level.

    Raises:
        ValueError: If a string logging level is unsupported.
    """
    if isinstance(level, int):
        return level

    normalized_level = level.upper()
    if normalized_level not in LOG_LEVELS:
        msg = f"Unsupported log level: {level}"
        raise ValueError(msg)

    return LOG_LEVELS[normalized_level]
