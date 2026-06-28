"""IBKR broker client tests."""

from datetime import UTC, datetime

import pytest

from ai_stock_analyzer.broker import BrokerInterface
from ai_stock_analyzer.broker.ibkr import IBKRClient
from ai_stock_analyzer.config import BrokerSettings


class MockIBKRApiClient:
    """Mock IBKR API client for connection tests."""

    def __init__(self) -> None:
        """Initialize mock connection state."""
        self.connected = False
        self.connected_host: str | None = None
        self.connected_port: int | None = None
        self.connected_client_id: int | None = None
        self.disconnect_count = 0

    def connect(self, host: str, port: int, client_id: int) -> None:
        """Record connection details and mark the mock connected."""
        self.connected = True
        self.connected_host = host
        self.connected_port = port
        self.connected_client_id = client_id

    def disconnect(self) -> None:
        """Mark the mock disconnected."""
        self.connected = False
        self.disconnect_count += 1

    def isConnected(self) -> bool:
        """Return the mock connection status."""
        return self.connected


def test_ibkr_client_implements_broker_interface() -> None:
    """Verify IBKR client implements the broker interface."""
    client = IBKRClient(
        BrokerSettings(host="test-host", port=4002, client_id=7),
        api_client_factory=MockIBKRApiClient,
    )

    assert isinstance(client, BrokerInterface)


def test_ibkr_client_connects_using_configured_settings() -> None:
    """Verify IBKR client connects using injected settings."""
    mock_api_client = MockIBKRApiClient()
    client = IBKRClient(
        BrokerSettings(host="test-host", port=4002, client_id=7),
        api_client_factory=lambda: mock_api_client,
    )

    client.connect()

    assert client.is_connected()
    assert mock_api_client.connected_host == "test-host"
    assert mock_api_client.connected_port == 4002
    assert mock_api_client.connected_client_id == 7


def test_ibkr_client_disconnect_updates_connection_state() -> None:
    """Verify IBKR client disconnects from the injected API client."""
    mock_api_client = MockIBKRApiClient()
    client = IBKRClient(
        BrokerSettings(host="test-host", port=4002, client_id=7),
        api_client_factory=lambda: mock_api_client,
    )

    client.connect()
    client.disconnect()

    assert not client.is_connected()
    assert mock_api_client.disconnect_count == 1


def test_ibkr_client_data_methods_are_not_implemented_yet() -> None:
    """Verify data methods are intentionally deferred."""
    client = IBKRClient(
        BrokerSettings(host="test-host", port=4002, client_id=7),
        api_client_factory=MockIBKRApiClient,
    )

    with pytest.raises(NotImplementedError):
        client.get_market_data("AAPL")

    with pytest.raises(NotImplementedError):
        client.get_historical_data(
            "AAPL",
            datetime(2026, 1, 1, tzinfo=UTC),
            datetime(2026, 1, 2, tzinfo=UTC),
            "1d",
        )
