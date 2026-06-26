"""Reusable datetime helper functions."""

from datetime import UTC, datetime

DEFAULT_DATETIME_FORMAT: str = "%Y-%m-%dT%H:%M:%S%z"


def utc_now() -> datetime:
    """Return the current UTC datetime.

    Returns:
        Timezone-aware current UTC datetime.
    """
    return datetime.now(UTC)


def ensure_utc(value: datetime) -> datetime:
    """Return a datetime normalized to UTC.

    Args:
        value: Datetime to normalize.

    Returns:
        Timezone-aware UTC datetime.
    """
    if value.tzinfo is None:
        return value.replace(tzinfo=UTC)

    return value.astimezone(UTC)


def format_datetime(
    value: datetime,
    datetime_format: str = DEFAULT_DATETIME_FORMAT,
) -> str:
    """Format a datetime after normalizing it to UTC.

    Args:
        value: Datetime to format.
        datetime_format: Format string used by datetime.strftime.

    Returns:
        Formatted UTC datetime string.
    """
    return ensure_utc(value).strftime(datetime_format)
