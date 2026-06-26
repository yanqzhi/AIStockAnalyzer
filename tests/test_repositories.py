"""SQLite repository tests."""

from collections.abc import Iterator
from datetime import UTC, datetime
from sqlite3 import Connection, connect

import pytest

from ai_stock_analyzer.database.repositories import (
    PositionRepository,
    StockRepository,
    TradeRepository,
)
from ai_stock_analyzer.models import Position, Stock, Trade


@pytest.fixture
def connection() -> Iterator[Connection]:
    """Create an in-memory SQLite connection for repository tests.

    Yields:
        SQLite connection.
    """
    sqlite_connection = connect(":memory:")

    try:
        yield sqlite_connection
    finally:
        sqlite_connection.close()


def test_stock_repository_crud(connection: Connection) -> None:
    """Verify stock repository CRUD operations."""
    repository = StockRepository(connection)
    stock = Stock(
        symbol="AAPL",
        name="Apple Inc.",
        exchange="NASDAQ",
        currency="USD",
    )
    updated_stock = Stock(
        symbol="AAPL",
        name="Apple",
        exchange="NASDAQ",
        currency="USD",
    )

    stock_id = repository.create(stock)
    repository.update(stock_id, updated_stock)

    assert stock_id == "AAPL"
    assert repository.get(stock_id) == updated_stock
    assert repository.list_all() == [updated_stock]

    repository.delete(stock_id)

    assert repository.get(stock_id) is None
    assert repository.list_all() == []


def test_position_repository_crud(connection: Connection) -> None:
    """Verify position repository CRUD operations."""
    repository = PositionRepository(connection)
    stock = Stock(
        symbol="MSFT",
        name="Microsoft Corporation",
        exchange="NASDAQ",
        currency="USD",
    )
    position = Position(stock=stock, quantity=10.0, average_cost=100.0)
    updated_position = Position(stock=stock, quantity=12.0, average_cost=105.0)

    position_id = repository.create(position)
    repository.update(position_id, updated_position)

    assert repository.get(position_id) == updated_position
    assert repository.list_all() == [updated_position]

    repository.delete(position_id)

    assert repository.get(position_id) is None
    assert repository.list_all() == []


def test_trade_repository_crud(connection: Connection) -> None:
    """Verify trade repository CRUD operations."""
    repository = TradeRepository(connection)
    stock = Stock(
        symbol="TSLA",
        name="Tesla Inc.",
        exchange="NASDAQ",
        currency="USD",
    )
    executed_at = datetime(2026, 1, 2, 3, 4, 5, tzinfo=UTC)
    trade = Trade(
        stock=stock,
        quantity=5.0,
        price=200.0,
        side="BUY",
        executed_at=executed_at,
    )
    updated_trade = Trade(
        stock=stock,
        quantity=5.0,
        price=205.0,
        side="BUY",
        executed_at=executed_at,
    )

    trade_id = repository.create(trade)
    repository.update(trade_id, updated_trade)

    assert repository.get(trade_id) == updated_trade
    assert repository.list_all() == [updated_trade]

    repository.delete(trade_id)

    assert repository.get(trade_id) is None
    assert repository.list_all() == []
