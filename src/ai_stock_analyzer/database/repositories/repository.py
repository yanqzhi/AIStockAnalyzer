"""Reusable SQLite repository implementation."""

from abc import ABC, abstractmethod
from collections.abc import Sequence
from sqlite3 import Connection, Row

from ai_stock_analyzer.database.database_manager import DatabaseManager

DatabaseSource = Connection | DatabaseManager


class BaseRepository[Entity, EntityId](ABC):
    """Generic SQLite repository with shared CRUD behavior."""

    def __init__(self, database: DatabaseSource) -> None:
        """Initialize the repository with an injected database source.

        Args:
            database: SQLite connection or database manager.
        """
        self._database_manager = (
            database if isinstance(database, DatabaseManager) else None
        )
        self._connection = (
            database.connection
            if isinstance(database, DatabaseManager)
            else database
        )
        self._connection.row_factory = Row
        self._create_schema()

    def create(self, entity: Entity) -> EntityId:
        """Persist an entity.

        Args:
            entity: Entity to persist.

        Returns:
            Identifier for the persisted entity.
        """
        cursor = self._connection.execute(
            self._insert_sql,
            self._to_record(entity),
        )
        self._commit()
        return self._created_id(entity, cursor.lastrowid)

    def get(self, entity_id: EntityId) -> Entity | None:
        """Fetch an entity by identifier.

        Args:
            entity_id: Entity identifier.

        Returns:
            The entity when found, otherwise None.
        """
        row = self._connection.execute(
            self._select_by_id_sql,
            self._id_parameters(entity_id),
        ).fetchone()

        if row is None:
            return None

        return self._from_row(row)

    def list_all(self) -> list[Entity]:
        """Fetch all entities.

        Returns:
            List of persisted entities.
        """
        rows = self._connection.execute(self._select_all_sql).fetchall()
        return [self._from_row(row) for row in rows]

    def update(self, entity_id: EntityId, entity: Entity) -> None:
        """Update an existing entity.

        Args:
            entity_id: Entity identifier.
            entity: Replacement entity data.
        """
        self._connection.execute(
            self._update_sql,
            (*self._to_record(entity), *self._id_parameters(entity_id)),
        )
        self._commit()

    def delete(self, entity_id: EntityId) -> None:
        """Delete an entity by identifier.

        Args:
            entity_id: Entity identifier.
        """
        self._connection.execute(
            self._delete_sql,
            self._id_parameters(entity_id),
        )
        self._commit()

    def _commit(self) -> None:
        """Commit repository changes through the configured database source."""
        if self._database_manager is None:
            self._connection.commit()
            return

        self._database_manager.commit()

    @property
    @abstractmethod
    def _insert_sql(self) -> str:
        """Return INSERT SQL for the repository."""

    @property
    @abstractmethod
    def _select_by_id_sql(self) -> str:
        """Return SELECT-by-id SQL for the repository."""

    @property
    @abstractmethod
    def _select_all_sql(self) -> str:
        """Return SELECT-all SQL for the repository."""

    @property
    @abstractmethod
    def _update_sql(self) -> str:
        """Return UPDATE SQL for the repository."""

    @property
    @abstractmethod
    def _delete_sql(self) -> str:
        """Return DELETE SQL for the repository."""

    @abstractmethod
    def _create_schema(self) -> None:
        """Create repository storage when missing."""

    @abstractmethod
    def _to_record(self, entity: Entity) -> tuple[object, ...]:
        """Convert an entity to SQLite parameters.

        Args:
            entity: Entity to convert.

        Returns:
            SQLite parameter tuple.
        """

    @abstractmethod
    def _from_row(self, row: Row) -> Entity:
        """Convert a SQLite row to an entity.

        Args:
            row: SQLite row.

        Returns:
            Converted entity.
        """

    @abstractmethod
    def _id_parameters(self, entity_id: EntityId) -> Sequence[object]:
        """Convert an entity identifier to SQLite parameters.

        Args:
            entity_id: Entity identifier.

        Returns:
            SQLite identifier parameters.
        """

    @abstractmethod
    def _created_id(self, entity: Entity, row_id: int) -> EntityId:
        """Return the identifier for a created entity.

        Args:
            entity: Persisted entity.
            row_id: SQLite row id.

        Returns:
            Entity identifier.
        """
