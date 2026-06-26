"""Database manager tests."""

from pathlib import Path

import pytest

from ai_stock_analyzer.database import DatabaseManager
from ai_stock_analyzer.database.repositories import StockRepository
from ai_stock_analyzer.models import Stock


def test_database_manager_is_singleton(tmp_path: Path) -> None:
    """Verify DatabaseManager returns one shared instance."""
    first_manager = DatabaseManager(tmp_path / "first.db")
    second_manager = DatabaseManager(tmp_path / "second.db")

    try:
        assert first_manager is second_manager
    finally:
        first_manager.close()


def test_database_manager_creates_database_file(tmp_path: Path) -> None:
    """Verify manager creates the database file and parent directory."""
    database_path = tmp_path / "nested" / "test.db"
    manager = DatabaseManager(database_path)

    try:
        assert database_path.exists()
    finally:
        manager.close()


def test_database_manager_commits_transaction(tmp_path: Path) -> None:
    """Verify context manager commits successful transactions."""
    database_path = tmp_path / "commit.db"
    manager = DatabaseManager(database_path)
    repository = StockRepository(manager)
    stock = Stock(
        symbol="AAPL",
        name="Apple Inc.",
        exchange="NASDAQ",
        currency="USD",
    )

    with manager:
        repository.create(stock)

    try:
        assert repository.get("AAPL") == stock
    finally:
        manager.close()


def test_database_manager_rolls_back_transaction(tmp_path: Path) -> None:
    """Verify context manager rolls back failed transactions."""
    database_path = tmp_path / "rollback.db"
    manager = DatabaseManager(database_path)
    repository = StockRepository(manager)
    stock = Stock(
        symbol="MSFT",
        name="Microsoft Corporation",
        exchange="NASDAQ",
        currency="USD",
    )

    with pytest.raises(RuntimeError, match="rollback"):
        with manager:
            repository.create(stock)
            raise RuntimeError("rollback")

    try:
        assert repository.get("MSFT") is None
    finally:
        manager.close()


def test_repository_uses_database_manager(tmp_path: Path) -> None:
    """Verify repositories can use DatabaseManager as their database source."""
    manager = DatabaseManager(tmp_path / "repository.db")
    repository = StockRepository(manager)
    stock = Stock(
        symbol="TSLA",
        name="Tesla Inc.",
        exchange="NASDAQ",
        currency="USD",
    )

    try:
        stock_id = repository.create(stock)

        assert stock_id == "TSLA"
        assert repository.get(stock_id) == stock
    finally:
        manager.close()
