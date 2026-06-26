"""Trade SQLite repository."""

from collections.abc import Sequence
from datetime import datetime
from sqlite3 import Row

from ai_stock_analyzer.database.repositories.repository import (
    BaseRepository,
    DatabaseSource,
)
from ai_stock_analyzer.models import Stock, Trade


class TradeRepository(BaseRepository[Trade, int]):
    """SQLite repository for trade records."""

    def __init__(self, database: DatabaseSource) -> None:
        """Initialize the trade repository.

        Args:
            database: SQLite connection or database manager.
        """
        super().__init__(database)

    @property
    def _insert_sql(self) -> str:
        """Return INSERT SQL for trade records."""
        return """
            INSERT INTO trades (
                stock_symbol,
                stock_name,
                stock_exchange,
                stock_currency,
                quantity,
                price,
                side,
                executed_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """

    @property
    def _select_by_id_sql(self) -> str:
        """Return SELECT-by-id SQL for trade records."""
        return """
            SELECT
                stock_symbol,
                stock_name,
                stock_exchange,
                stock_currency,
                quantity,
                price,
                side,
                executed_at
            FROM trades
            WHERE id = ?
        """

    @property
    def _select_all_sql(self) -> str:
        """Return SELECT-all SQL for trade records."""
        return """
            SELECT
                stock_symbol,
                stock_name,
                stock_exchange,
                stock_currency,
                quantity,
                price,
                side,
                executed_at
            FROM trades
            ORDER BY id
        """

    @property
    def _update_sql(self) -> str:
        """Return UPDATE SQL for trade records."""
        return """
            UPDATE trades
            SET
                stock_symbol = ?,
                stock_name = ?,
                stock_exchange = ?,
                stock_currency = ?,
                quantity = ?,
                price = ?,
                side = ?,
                executed_at = ?
            WHERE id = ?
        """

    @property
    def _delete_sql(self) -> str:
        """Return DELETE SQL for trade records."""
        return """
            DELETE FROM trades
            WHERE id = ?
        """

    def _create_schema(self) -> None:
        """Create trade storage when missing."""
        self._connection.execute(
            """
            CREATE TABLE IF NOT EXISTS trades (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                stock_symbol TEXT NOT NULL,
                stock_name TEXT NOT NULL,
                stock_exchange TEXT NOT NULL,
                stock_currency TEXT NOT NULL,
                quantity REAL NOT NULL,
                price REAL NOT NULL,
                side TEXT NOT NULL,
                executed_at TEXT NOT NULL
            )
            """,
        )
        self._connection.commit()

    def _to_record(self, entity: Trade) -> tuple[object, ...]:
        """Convert a trade to SQLite parameters.

        Args:
            entity: Trade to convert.

        Returns:
            SQLite parameter tuple.
        """
        return (
            entity.stock.symbol,
            entity.stock.name,
            entity.stock.exchange,
            entity.stock.currency,
            entity.quantity,
            entity.price,
            entity.side,
            entity.executed_at.isoformat(),
        )

    def _from_row(self, row: Row) -> Trade:
        """Convert a SQLite row to a trade.

        Args:
            row: SQLite row.

        Returns:
            Trade data model.
        """
        return Trade(
            stock=Stock(
                symbol=str(row["stock_symbol"]),
                name=str(row["stock_name"]),
                exchange=str(row["stock_exchange"]),
                currency=str(row["stock_currency"]),
            ),
            quantity=float(row["quantity"]),
            price=float(row["price"]),
            side=str(row["side"]),
            executed_at=datetime.fromisoformat(str(row["executed_at"])),
        )

    def _id_parameters(self, entity_id: int) -> Sequence[object]:
        """Convert a trade id to SQLite parameters.

        Args:
            entity_id: Trade id.

        Returns:
            SQLite identifier parameters.
        """
        return (entity_id,)

    def _created_id(self, entity: Trade, row_id: int) -> int:
        """Return the identifier for a created trade.

        Args:
            entity: Persisted trade.
            row_id: SQLite row id.

        Returns:
            Trade id.
        """
        return row_id
