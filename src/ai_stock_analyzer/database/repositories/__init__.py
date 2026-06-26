"""Repository pattern contracts."""

from ai_stock_analyzer.database.repositories.base import Repository
from ai_stock_analyzer.database.repositories.position_repository import (
    PositionRepository,
)
from ai_stock_analyzer.database.repositories.repository import BaseRepository
from ai_stock_analyzer.database.repositories.stock_repository import StockRepository
from ai_stock_analyzer.database.repositories.trade_repository import TradeRepository

__all__ = [
    "BaseRepository",
    "PositionRepository",
    "Repository",
    "StockRepository",
    "TradeRepository",
]
