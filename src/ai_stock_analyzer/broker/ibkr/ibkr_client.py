"""IBKR broker client implementation."""

from collections.abc import Callable, Mapping, Sequence
from datetime import datetime
from typing import Protocol

from ai_stock_analyzer.broker import BrokerInterface
from ai_stock_analyzer.config import BrokerSettings


class _IBKRApiClient(Protocol):
    def connect(self, host: str, port: int, client_id: int) -> None: ...

    def disconnect(self) -> None: ...

    def isConnected(self) -> bool: ...


def _create_ibkr_api_client() -> _IBKRApiClient:
    from ibapi.client import EClient
    from ibapi.wrapper import EWrapper

    class _DefaultIBKRApiClient(EWrapper, EClient):
        def __init__(self) -> None:
            EClient.__init__(self, self)

    return _DefaultIBKRApiClient()


class IBKRClient(BrokerInterface):
    """IBKR broker client for connection lifecycle operations."""

    def __init__(
        self,
        settings: BrokerSettings,
        api_client_factory: Callable[[], _IBKRApiClient] = _create_ibkr_api_client,
    ) -> None:
        """Initialize an IBKR broker client.

        Args:
            settings: Broker settings containing host, port, and client id.
            api_client_factory: Factory that creates the underlying IBKR API client.
        """
        self._settings = settings
        self._api_client_factory = api_client_factory
        self._api_client: _IBKRApiClient | None = None

    def connect(self) -> None:
        """Connect to TWS or IB Gateway."""
        if self.is_connected():
            return

        if self._api_client is None:
            self._api_client = self._api_client_factory()

        self._api_client.connect(
            self._settings.host,
            self._settings.port,
            self._settings.client_id,
        )

    def disconnect(self) -> None:
        """Disconnect from TWS or IB Gateway."""
        if self._api_client is None:
            return

        self._api_client.disconnect()

    def is_connected(self) -> bool:
        """Return whether the IBKR API client is connected.

        Returns:
            True when connected to TWS or IB Gateway, otherwise False.
        """
        if self._api_client is None:
            return False

        return self._api_client.isConnected()

    def get_historical_data(
        self,
        symbol: str,
        start: datetime,
        end: datetime,
        interval: str,
    ) -> Sequence[Mapping[str, object]]:
        """Return historical market data for a symbol.

        Args:
            symbol: Instrument symbol to request.
            start: Inclusive start datetime for the requested period.
            end: Inclusive end datetime for the requested period.
            interval: Time interval for each returned data point.

        Raises:
            NotImplementedError: Historical data is not implemented yet.
        """
        raise NotImplementedError("IBKR historical data is not implemented yet.")

    def get_market_data(self, symbol: str) -> Mapping[str, object]:
        """Return current market data for a symbol.

        Args:
            symbol: Instrument symbol to request.

        Raises:
            NotImplementedError: Market data is not implemented yet.
        """
        raise NotImplementedError("IBKR market data is not implemented yet.")
