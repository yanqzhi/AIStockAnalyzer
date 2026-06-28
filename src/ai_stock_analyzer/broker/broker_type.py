"""Broker type definitions."""

from enum import StrEnum


class BrokerType(StrEnum):
    """Supported broker integration types."""

    IBKR = "ibkr"
    MOOMOO = "moomoo"
    POLYGON = "polygon"
