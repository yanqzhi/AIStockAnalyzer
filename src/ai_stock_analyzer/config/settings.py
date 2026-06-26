"""Application settings definitions."""

from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    """Application settings loaded from environment or .env.

    Attributes:
        name: Application display name.
        environment: Runtime environment name.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="APP_",
        frozen=True,
    )

    name: str = Field(default="AI Stock Analyzer", min_length=1)
    environment: str = Field(default="development", min_length=1)


class DatabaseSettings(BaseSettings):
    """Database settings loaded from environment or .env.

    Attributes:
        path: SQLite database file path.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="DATABASE_",
        frozen=True,
    )

    path: Path = Path("data/ai_stock_analyzer.db")


class LoggingSettings(BaseSettings):
    """Logging settings loaded from environment or .env.

    Attributes:
        level: Logging level name.
        format: Logging formatter pattern.
        file_path: Log file path.
        max_bytes: Maximum bytes per log file before rotation.
        backup_count: Number of rotated log files to retain.
        enable_console: Whether console logging is enabled.
        enable_file: Whether rotating file logging is enabled.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="LOGGING_",
        frozen=True,
    )

    level: str = Field(default="INFO", min_length=1)
    format: str = Field(
        default="%(asctime)s %(levelname)s [%(name)s] %(message)s",
        min_length=1,
    )
    file_path: Path = Path("logs/application.log")
    max_bytes: int = Field(default=1_048_576, gt=0)
    backup_count: int = Field(default=5, ge=0)
    enable_console: bool = True
    enable_file: bool = True


class BrokerSettings(BaseSettings):
    """Broker settings loaded from environment or .env.

    Attributes:
        provider: Broker provider name.
        host: Broker API host.
        port: Broker API port.
        client_id: Broker API client id.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="BROKER_",
        frozen=True,
    )

    provider: str = Field(default="ibkr", min_length=1)
    host: str = Field(default="127.0.0.1", min_length=1)
    port: int = Field(default=7497, gt=0)
    client_id: int = Field(default=1, ge=0)


class OpenAISettings(BaseSettings):
    """OpenAI settings loaded from environment or .env.

    Attributes:
        api_key: OpenAI API key.
        model: OpenAI model name.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="OPENAI_",
        frozen=True,
    )

    api_key: str = ""
    model: str = Field(default="gpt-4.1-mini", min_length=1)


class Settings(BaseSettings):
    """Aggregate immutable application settings."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_nested_delimiter="__",
        frozen=True,
    )

    app: AppSettings = Field(default_factory=AppSettings)
    database: DatabaseSettings = Field(default_factory=DatabaseSettings)
    logging: LoggingSettings = Field(default_factory=LoggingSettings)
    broker: BrokerSettings = Field(default_factory=BrokerSettings)
    openai: OpenAISettings = Field(default_factory=OpenAISettings)
