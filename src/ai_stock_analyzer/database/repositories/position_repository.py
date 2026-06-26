"""Position SQLite repository."""

from collections.abc import Sequence
from sqlite3 import Row

from ai_stock_analyzer.database.repositories.repository import (
    BaseRepository,
    DatabaseSource,
)
from ai_stock_analyzer.models import Position, Stock


class PositionRepository(BaseRepository[Position, int]):
    """SQLite repository for position records."""

    def __init__(self, database: DatabaseSource) -> None:
        """Initialize the position repository.

        Args:
            database: SQLite connection or database manager.
        """
        super().__init__(database)

    @property
    def _insert_sql(self) -> str:
        """Return INSERT SQL for position records."""
        return """
            INSERT INTO positions (
                stock_symbol,
                stock_name,
                stock_exchange,
                stock_currency,
                quantity,
                average_cost
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """

    @property
    def _select_by_id_sql(self) -> str:
        """Return SELECT-by-id SQL for position records."""
        return """
            SELECT
                stock_symbol,
                stock_name,
                stock_exchange,
                stock_currency,
                quantity,
                average_cost
            FROM positions
            WHERE id = ?
        """

    @property
    def _select_all_sql(self) -> str:
        """Return SELECT-all SQL for position records."""
        return """
            SELECT
                stock_symbol,
                stock_name,
                stock_exchange,
                stock_currency,
                quantity,
                average_cost
            FROM positions
            ORDER BY id
        """

    @property
    def _update_sql(self) -> str:
        """Return UPDATE SQL for position records."""
        return """
            UPDATE positions
            SET
                stock_symbol = ?,
                stock_name = ?,
                stock_exchange = ?,
                stock_currency = ?,
                quantity = ?,
                average_cost = ?
            WHERE id = ?
        """

    @property
    def _delete_sql(self) -> str:
        """Return DELETE SQL for position records."""
        return """
            DELETE FROM positions
            WHERE id = ?
        """

    def _create_schema(self) -> None:
        """Create position storage when missing."""
        self._connection.execute(
            """
            CREATE TABLE IF NOT EXISTS positions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                stock_symbol TEXT NOT NULL,
                stock_name TEXT NOT NULL,
                stock_exchange TEXT NOT NULL,
                stock_currency TEXT NOT NULL,
                quantity REAL NOT NULL,
                average_cost REAL NOT NULL
            )
            """,
        )
        self._connection.commit()

    def _to_record(self, entity: Position) -> tuple[object, ...]:
        """Convert a position to SQLite parameters.

        Args:
            entity: Position to convert.

        Returns:
            SQLite parameter tuple.
        """
        return (
            entity.stock.symbol,
            entity.stock.name,
            entity.stock.exchange,
            entity.stock.currency,
            entity.quantity,
            entity.average_cost,
        )

    def _from_row(self, row: Row) -> Position:
        """Convert a SQLite row to a position.

        Args:
            row: SQLite row.

        Returns:
            Position data model.
        """
        return Position(
            stock=Stock(
                symbol=str(row["stock_symbol"]),
                name=str(row["stock_name"]),
                exchange=str(row["stock_exchange"]),
                currency=str(row["stock_currency"]),
            ),
            quantity=float(row["quantity"]),
            average_cost=float(row["average_cost"]),
        )

    def _id_parameters(self, entity_id: int) -> Sequence[object]:
        """Convert a position id to SQLite parameters.

        Args:
            entity_id: Position id.

        Returns:
            SQLite identifier parameters.
        """
        return (entity_id,)

    def _created_id(self, entity: Position, row_id: int) -> int:
        """Return the identifier for a created position.

        Args:
            entity: Persisted position.
            row_id: SQLite row id.

        Returns:
            Position id.
        """
        return row_id
