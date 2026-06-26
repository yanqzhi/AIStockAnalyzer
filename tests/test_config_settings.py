"""Configuration settings tests."""

from pathlib import Path

import pytest
from pydantic import ValidationError
from pytest import MonkeyPatch

from ai_stock_analyzer.config import (
    AppSettings,
    BrokerSettings,
    DatabaseSettings,
    LoggingSettings,
    OpenAISettings,
    Settings,
)

ENVIRONMENT_VARIABLES: tuple[str, ...] = (
    "APP_NAME",
    "APP_ENVIRONMENT",
    "DATABASE_PATH",
    "LOGGING_LEVEL",
    "LOGGING_FORMAT",
    "LOGGING_FILE_PATH",
    "LOGGING_MAX_BYTES",
    "LOGGING_BACKUP_COUNT",
    "LOGGING_ENABLE_CONSOLE",
    "LOGGING_ENABLE_FILE",
    "BROKER_PROVIDER",
    "BROKER_HOST",
    "BROKER_PORT",
    "BROKER_CLIENT_ID",
    "OPENAI_API_KEY",
    "OPENAI_MODEL",
)


def test_settings_load_environment_variables(monkeypatch: MonkeyPatch) -> None:
    """Verify settings load values from environment variables."""
    _clear_environment(monkeypatch)
    monkeypatch.setenv("APP_NAME", "Test Analyzer")
    monkeypatch.setenv("DATABASE_PATH", "test-data/app.db")
    monkeypatch.setenv("LOGGING_LEVEL", "DEBUG")
    monkeypatch.setenv("BROKER_PORT", "4002")
    monkeypatch.setenv("OPENAI_MODEL", "test-model")

    settings = Settings()

    assert settings.app.name == "Test Analyzer"
    assert settings.database.path == Path("test-data/app.db")
    assert settings.logging.level == "DEBUG"
    assert settings.broker.port == 4002
    assert settings.openai.model == "test-model"


def test_settings_load_dotenv_file(tmp_path: Path) -> None:
    """Verify settings can load values from a .env file."""
    env_file = tmp_path / ".env"
    env_file.write_text(
        "APP_NAME=Dotenv Analyzer\nAPP_ENVIRONMENT=testing\n",
        encoding="utf-8",
    )

    settings = AppSettings(_env_file=env_file)

    assert settings.name == "Dotenv Analyzer"
    assert settings.environment == "testing"


def test_settings_defaults(monkeypatch: MonkeyPatch) -> None:
    """Verify settings provide default values."""
    _clear_environment(monkeypatch)
    settings = Settings()

    assert settings.app.name == "AI Stock Analyzer"
    assert settings.app.environment == "development"
    assert settings.database.path == Path("data/ai_stock_analyzer.db")
    assert settings.logging.file_path == Path("logs/application.log")
    assert settings.broker.provider == "ibkr"
    assert settings.openai.model == "gpt-4.1-mini"


def test_settings_validation() -> None:
    """Verify invalid settings raise validation errors."""
    with pytest.raises(ValidationError):
        BrokerSettings(port=0)

    with pytest.raises(ValidationError):
        LoggingSettings(max_bytes=0)


def test_settings_are_immutable() -> None:
    """Verify settings cannot be modified after initialization."""
    settings = DatabaseSettings()

    with pytest.raises(ValidationError):
        settings.path = Path("other.db")


def test_separate_settings_classes_are_importable() -> None:
    """Verify separate settings classes are available."""
    assert AppSettings
    assert BrokerSettings
    assert DatabaseSettings
    assert LoggingSettings
    assert OpenAISettings


def _clear_environment(monkeypatch: MonkeyPatch) -> None:
    """Clear settings environment variables for deterministic tests.

    Args:
        monkeypatch: Pytest monkeypatch fixture.
    """
    for variable_name in ENVIRONMENT_VARIABLES:
        monkeypatch.delenv(variable_name, raising=False)
