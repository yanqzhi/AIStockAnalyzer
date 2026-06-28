"""Broker interface tests."""

from datetime import UTC, datetime

import pytest

from ai_stock_analyzer.broker import BrokerInterface, BrokerType


def test_broker_interface_imports() -> None:
    """Verify broker interface package exports are importable."""
    assert BrokerInterface
    assert BrokerType.IBKR == "ibkr"
    assert BrokerType.MOOMOO == "moomoo"
    assert BrokerType.POLYGON == "polygon"


def test_broker_interface_cannot_be_instantiated_directly() -> None:
    """Verify broker interface remains abstract."""
    with pytest.raises(TypeError):
        BrokerInterface()


def test_broker_interface_requires_all_abstract_methods() -> None:
    """Verify incomplete broker implementations remain abstract."""

    class IncompleteBroker(BrokerInterface):
        """Incomplete test broker implementation."""

        def connect(self) -> None:
            """Connect to the broker service."""

    with pytest.raises(TypeError):
        IncompleteBroker()


def test_complete_broker_implementation_can_be_instantiated() -> None:
    """Verify complete broker implementations satisfy the interface."""

    class CompleteBroker(BrokerInterface):
        """Complete test broker implementation."""

        def connect(self) -> None:
            """Connect to the broker service."""

        def disconnect(self) -> None:
            """Disconnect from the broker service."""

        def is_connected(self) -> bool:
            """Return whether the broker service is connected."""
            return True

        def get_historical_data(
            self,
            symbol: str,
            start: datetime,
            end: datetime,
            interval: str,
        ) -> list[dict[str, object]]:
            """Return historical market data for a symbol."""
            return [
                {
                    "symbol": symbol,
                    "start": start,
                    "end": end,
                    "interval": interval,
                }
            ]

        def get_market_data(self, symbol: str) -> dict[str, object]:
            """Return current market data for a symbol."""
            return {"symbol": symbol}

    broker = CompleteBroker()

    assert broker.is_connected()
    assert broker.get_market_data("AAPL") == {"symbol": "AAPL"}
    assert broker.get_historical_data(
        "AAPL",
        datetime(2026, 1, 1, tzinfo=UTC),
        datetime(2026, 1, 2, tzinfo=UTC),
        "1d",
    )
