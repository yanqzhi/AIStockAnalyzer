"""Stock SQLite repository."""

from collections.abc import Sequence
from sqlite3 import Row

from ai_stock_analyzer.database.repositories.repository import (
    BaseRepository,
    DatabaseSource,
)
from ai_stock_analyzer.models import Stock


class StockRepository(BaseRepository[Stock, str]):
    """SQLite repository for stock records."""

    def __init__(self, database: DatabaseSource) -> None:
        """Initialize the stock repository.

        Args:
            database: SQLite connection or database manager.
        """
        super().__init__(database)

    @property
    def _insert_sql(self) -> str:
        """Return INSERT SQL for stock records."""
        return """
            INSERT INTO stocks (symbol, name, exchange, currency)
            VALUES (?, ?, ?, ?)
        """

    @property
    def _select_by_id_sql(self) -> str:
        """Return SELECT-by-id SQL for stock records."""
        return """
            SELECT symbol, name, exchange, currency
            FROM stocks
            WHERE symbol = ?
        """

    @property
    def _select_all_sql(self) -> str:
        """Return SELECT-all SQL for stock records."""
        return """
            SELECT symbol, name, exchange, currency
            FROM stocks
            ORDER BY symbol
        """

    @property
    def _update_sql(self) -> str:
        """Return UPDATE SQL for stock records."""
        return """
            UPDATE stocks
            SET symbol = ?, name = ?, exchange = ?, currency = ?
            WHERE symbol = ?
        """

    @property
    def _delete_sql(self) -> str:
        """Return DELETE SQL for stock records."""
        return """
            DELETE FROM stocks
            WHERE symbol = ?
        """

    def _create_schema(self) -> None:
        """Create stock storage when missing."""
        self._connection.execute(
            """
            CREATE TABLE IF NOT EXISTS stocks (
                symbol TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                exchange TEXT NOT NULL,
                currency TEXT NOT NULL
            )
            """,
        )
        self._connection.commit()

    def _to_record(self, entity: Stock) -> tuple[object, ...]:
        """Convert a stock to SQLite parameters.

        Args:
            entity: Stock to convert.

        Returns:
            SQLite parameter tuple.
        """
        return (
            entity.symbol,
            entity.name,
            entity.exchange,
            entity.currency,
        )

    def _from_row(self, row: Row) -> Stock:
        """Convert a SQLite row to a stock.

        Args:
            row: SQLite row.

        Returns:
            Stock data model.
        """
        return Stock(
            symbol=str(row["symbol"]),
            name=str(row["name"]),
            exchange=str(row["exchange"]),
            currency=str(row["currency"]),
        )

    def _id_parameters(self, entity_id: str) -> Sequence[object]:
        """Convert a stock symbol to SQLite parameters.

        Args:
            entity_id: Stock symbol.

        Returns:
            SQLite identifier parameters.
        """
        return (entity_id,)

    def _created_id(self, entity: Stock, row_id: int) -> str:
        """Return the identifier for a created stock.

        Args:
            entity: Persisted stock.
            row_id: SQLite row id.

        Returns:
            Stock symbol.
        """
        return entity.symbol
