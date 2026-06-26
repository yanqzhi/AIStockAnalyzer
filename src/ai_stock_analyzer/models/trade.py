"""Trade data model."""

from dataclasses import dataclass
from datetime import datetime

from ai_stock_analyzer.models.stock import Stock


@dataclass(frozen=True, slots=True)
class Trade:
    """Trade execution data.

    Attributes:
        stock: Stock instrument for the trade.
        quantity: Trade quantity.
        price: Trade execution price.
        side: Trade side.
        executed_at: Trade execution timestamp.
    """

    stock: Stock
    quantity: float
    price: float
    side: str
    executed_at: datetime
