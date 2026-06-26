"""Stock data model."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Stock:
    """Stock instrument data.

    Attributes:
        symbol: Stock ticker symbol.
        name: Stock display name.
        exchange: Exchange identifier.
        currency: Trading currency code.
    """

    symbol: str
    name: str
    exchange: str
    currency: str
