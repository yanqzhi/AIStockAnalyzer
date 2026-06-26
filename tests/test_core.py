"""Core package tests."""

import ai_stock_analyzer.core as core
from ai_stock_analyzer.core import (
    AIStockAnalyzerError,
    ConfigurationError,
    InfrastructureError,
    ValidationError,
)


def test_core_package_exports_public_members() -> None:
    """Verify core package public members are importable."""
    assert core.APPLICATION_NAME
    assert core.DEFAULT_CONFIG_PATH
    assert core.DEFAULT_ENVIRONMENT
    assert core.Environment
    assert core.LogLevel
    assert core.AIStockAnalyzerError
    assert core.ConfigurationError
    assert core.InfrastructureError
    assert core.ValidationError


def test_common_exceptions_inherit_from_project_base_exception() -> None:
    """Verify common custom exceptions share the project base exception."""
    exception_types: tuple[type[AIStockAnalyzerError], ...] = (
        ConfigurationError,
        InfrastructureError,
        ValidationError,
    )

    for exception_type in exception_types:
        assert issubclass(exception_type, AIStockAnalyzerError)


def test_custom_exceptions_preserve_messages() -> None:
    """Verify custom exceptions preserve provided messages."""
    message = "test message"

    assert str(ConfigurationError(message)) == message
    assert str(InfrastructureError(message)) == message
    assert str(ValidationError(message)) == message
