"""Position data model."""

from dataclasses import dataclass

from ai_stock_analyzer.models.stock import Stock


@dataclass(frozen=True, slots=True)
class Position:
    """Portfolio position data.

    Attributes:
        stock: Stock instrument for the position.
        quantity: Position quantity.
        average_cost: Average acquisition cost.
    """

    stock: Stock
    quantity: float
    average_cost: float
