"""Abstract broker interface definitions."""

from abc import ABC, abstractmethod
from collections.abc import Mapping, Sequence
from datetime import datetime


class BrokerInterface(ABC):
    """Abstract interface that all broker implementations must follow."""

    @abstractmethod
    def connect(self) -> None:
        """Connect to the broker service."""
        ...

    @abstractmethod
    def disconnect(self) -> None:
        """Disconnect from the broker service."""
        ...

    @abstractmethod
    def is_connected(self) -> bool:
        """Return whether the broker service is connected.

        Returns:
            True when connected, otherwise False.
        """
        ...

    @abstractmethod
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

        Returns:
            A sequence of provider-normalized market data records.
        """
        ...

    @abstractmethod
    def get_market_data(self, symbol: str) -> Mapping[str, object]:
        """Return current market data for a symbol.

        Args:
            symbol: Instrument symbol to request.

        Returns:
            Provider-normalized market data record.
        """
        ...
