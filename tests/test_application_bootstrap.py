"""Application bootstrap tests."""

from pathlib import Path
from types import ModuleType

from pytest import MonkeyPatch

import ai_stock_analyzer.__main__ as entrypoint


class FakeApplication:
    """Test double for QApplication."""

    created_arguments: list[str] | None = None

    def __init__(self, arguments: list[str]) -> None:
        """Initialize the fake application.

        Args:
            arguments: Command-line arguments.
        """
        self.created_arguments = arguments
        FakeApplication.created_arguments = arguments

    @staticmethod
    def instance() -> None:
        """Return no existing application for tests."""
        return None

    def exec(self) -> int:
        """Return a successful exit code."""
        return 0


class FakeMainWindow:
    """Test double for MainWindow."""

    shown: bool = False

    def show(self) -> None:
        """Record that the window was shown."""
        FakeMainWindow.shown = True


class FakeDatabaseManager:
    """Test double for DatabaseManager."""

    initialized_path: Path | None = None
    closed: bool = False

    def __init__(self, database_path: Path) -> None:
        """Initialize the fake database manager.

        Args:
            database_path: Database path from configuration.
        """
        FakeDatabaseManager.initialized_path = database_path

    def close(self) -> None:
        """Record that the database manager was closed."""
        FakeDatabaseManager.closed = True


def test_entrypoint_module_is_importable() -> None:
    """Verify the application entrypoint module is importable."""
    assert isinstance(entrypoint, ModuleType)


def test_main_starts_application(monkeypatch: MonkeyPatch, tmp_path: Path) -> None:
    """Verify main initializes dependencies and starts the application."""
    database_path = tmp_path / "app.db"
    log_file_path = tmp_path / "application.log"
    monkeypatch.setenv("DATABASE_PATH", str(database_path))
    monkeypatch.setenv("LOGGING_FILE_PATH", str(log_file_path))
    monkeypatch.setattr(entrypoint, "QApplication", FakeApplication)
    monkeypatch.setattr(entrypoint, "MainWindow", FakeMainWindow)
    monkeypatch.setattr(entrypoint, "DatabaseManager", FakeDatabaseManager)
    FakeMainWindow.shown = False
    FakeDatabaseManager.closed = False
    FakeDatabaseManager.initialized_path = None

    exit_code = entrypoint.main(["ai-stock-analyzer"])

    assert exit_code == 0
    assert FakeApplication.created_arguments == ["ai-stock-analyzer"]
    assert FakeDatabaseManager.initialized_path == database_path
    assert FakeMainWindow.shown is True
    assert FakeDatabaseManager.closed is True


def test_main_returns_error_code_on_startup_failure(
    monkeypatch: MonkeyPatch,
    tmp_path: Path,
) -> None:
    """Verify main handles startup exceptions gracefully."""
    monkeypatch.setenv("DATABASE_PATH", str(tmp_path / "app.db"))
    monkeypatch.setenv("LOGGING_FILE_PATH", str(tmp_path / "application.log"))
    monkeypatch.setattr(entrypoint, "QApplication", FakeApplication)
    monkeypatch.setattr(entrypoint, "MainWindow", _raise_startup_error)
    monkeypatch.setattr(entrypoint, "DatabaseManager", FakeDatabaseManager)

    exit_code = entrypoint.main(["ai-stock-analyzer"])

    assert exit_code == 1


def _raise_startup_error() -> FakeMainWindow:
    """Raise a startup error for bootstrap tests.

    Raises:
        RuntimeError: Always raised for startup failure testing.
    """
    raise RuntimeError("startup failed")
