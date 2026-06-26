"""Model dataclass tests."""

from dataclasses import asdict, is_dataclass
from datetime import UTC, datetime

from ai_stock_analyzer.models import Position, Stock, Trade


def test_stock_initialization() -> None:
    """Verify Stock can be initialized as a dataclass."""
    stock = Stock(
        symbol="AAPL",
        name="Apple Inc.",
        exchange="NASDAQ",
        currency="USD",
    )

    assert is_dataclass(stock)
    assert stock.symbol == "AAPL"
    assert stock.name == "Apple Inc."
    assert stock.exchange == "NASDAQ"
    assert stock.currency == "USD"


def test_position_initialization() -> None:
    """Verify Position can be initialized as a dataclass."""
    stock = Stock(
        symbol="MSFT",
        name="Microsoft Corporation",
        exchange="NASDAQ",
        currency="USD",
    )
    position = Position(stock=stock, quantity=10.0, average_cost=100.0)

    assert is_dataclass(position)
    assert position.stock == stock
    assert position.quantity == 10.0
    assert position.average_cost == 100.0


def test_trade_initialization() -> None:
    """Verify Trade can be initialized as a dataclass."""
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

    assert is_dataclass(trade)
    assert trade.stock == stock
    assert trade.quantity == 5.0
    assert trade.price == 200.0
    assert trade.side == "BUY"
    assert trade.executed_at == executed_at


def test_stock_serialization() -> None:
    """Verify Stock serializes with dataclasses.asdict."""
    stock = Stock(
        symbol="AAPL",
        name="Apple Inc.",
        exchange="NASDAQ",
        currency="USD",
    )

    assert asdict(stock) == {
        "symbol": "AAPL",
        "name": "Apple Inc.",
        "exchange": "NASDAQ",
        "currency": "USD",
    }


def test_position_serialization() -> None:
    """Verify Position serializes with dataclasses.asdict."""
    stock = Stock(
        symbol="MSFT",
        name="Microsoft Corporation",
        exchange="NASDAQ",
        currency="USD",
    )
    position = Position(stock=stock, quantity=10.0, average_cost=100.0)

    assert asdict(position) == {
        "stock": {
            "symbol": "MSFT",
            "name": "Microsoft Corporation",
            "exchange": "NASDAQ",
            "currency": "USD",
        },
        "quantity": 10.0,
        "average_cost": 100.0,
    }


def test_trade_serialization() -> None:
    """Verify Trade serializes with dataclasses.asdict."""
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

    assert asdict(trade) == {
        "stock": {
            "symbol": "TSLA",
            "name": "Tesla Inc.",
            "exchange": "NASDAQ",
            "currency": "USD",
        },
        "quantity": 5.0,
        "price": 200.0,
        "side": "BUY",
        "executed_at": executed_at,
    }
