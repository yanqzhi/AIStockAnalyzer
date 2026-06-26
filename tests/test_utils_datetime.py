"""Datetime utility tests."""

from datetime import UTC, datetime, timedelta, timezone

from ai_stock_analyzer.utils import ensure_utc, format_datetime, utc_now


def test_utc_now_returns_timezone_aware_utc_datetime() -> None:
    """Verify utc_now returns a timezone-aware UTC datetime."""
    current_datetime = utc_now()

    assert current_datetime.tzinfo is UTC


def test_ensure_utc_adds_utc_timezone_to_naive_datetime() -> None:
    """Verify naive datetimes are treated as UTC."""
    naive_datetime = datetime(2026, 1, 2, 3, 4, 5)

    utc_datetime = ensure_utc(naive_datetime)

    assert utc_datetime.tzinfo is UTC
    assert utc_datetime.hour == naive_datetime.hour


def test_ensure_utc_converts_timezone_aware_datetime() -> None:
    """Verify aware datetimes are converted to UTC."""
    source_timezone = timezone(timedelta(hours=9))
    source_datetime = datetime(2026, 1, 2, 12, 0, 0, tzinfo=source_timezone)

    utc_datetime = ensure_utc(source_datetime)

    assert utc_datetime.tzinfo is UTC
    assert utc_datetime.hour == 3


def test_format_datetime_returns_formatted_utc_datetime() -> None:
    """Verify datetimes are formatted after UTC normalization."""
    source_datetime = datetime(2026, 1, 2, 3, 4, 5)

    formatted_datetime = format_datetime(source_datetime)

    assert formatted_datetime == "2026-01-02T03:04:05+0000"
