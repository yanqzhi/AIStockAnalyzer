"""SQLite database manager."""

from __future__ import annotations

from pathlib import Path
from sqlite3 import Connection, Row, connect
from threading import RLock, local
from types import TracebackType
from typing import ClassVar, Self


class DatabaseManager:
    """Manage SQLite connection lifecycle and transactions."""

    _instance: ClassVar[Self | None] = None
    _instance_lock: ClassVar[RLock] = RLock()

    def __new__(cls, database_path: Path) -> Self:
        """Create or return the shared database manager instance.

        Args:
            database_path: SQLite database file path.

        Returns:
            Shared database manager instance.
        """
        with cls._instance_lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)

        return cls._instance

    def __init__(self, database_path: Path) -> None:
        """Initialize the database manager.

        Args:
            database_path: SQLite database file path.
        """
        self._lock = RLock()
        self._local = local()
        self._database_path = database_path
        self._initialize_database()

    def __enter__(self) -> Self:
        """Begin a managed transaction.

        Returns:
            The database manager.
        """
        self._lock.acquire()
        self.connection.execute("BEGIN")
        self._transaction_depth = self._transaction_depth + 1
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        """Commit or roll back the managed transaction.

        Args:
            exc_type: Exception type when the context exits with an error.
            exc_value: Exception value when the context exits with an error.
            traceback: Exception traceback when the context exits with an error.
        """
        try:
            if exc_type is None:
                self.connection.commit()
            else:
                self.connection.rollback()
        finally:
            self._transaction_depth = max(0, self._transaction_depth - 1)
            self._lock.release()

    @property
    def connection(self) -> Connection:
        """Return the thread-local SQLite connection.

        Returns:
            SQLite connection for the current thread.
        """
        sqlite_connection = getattr(self._local, "connection", None)

        if sqlite_connection is None:
            sqlite_connection = connect(
                self._database_path,
                check_same_thread=False,
            )
            sqlite_connection.row_factory = Row
            sqlite_connection.execute("PRAGMA foreign_keys = ON")
            self._local.connection = sqlite_connection

        return sqlite_connection

    def commit(self) -> None:
        """Commit pending changes when outside a managed transaction."""
        if self._transaction_depth == 0:
            self.connection.commit()

    def rollback(self) -> None:
        """Roll back pending changes."""
        self.connection.rollback()

    def close(self) -> None:
        """Close the current thread SQLite connection."""
        sqlite_connection = getattr(self._local, "connection", None)

        if sqlite_connection is not None:
            sqlite_connection.close()
            self._local.connection = None

    def _initialize_database(self) -> None:
        """Create the database directory and initialize the connection."""
        self._database_path.parent.mkdir(parents=True, exist_ok=True)
        _ = self.connection

    @property
    def _transaction_depth(self) -> int:
        """Return transaction depth for the current thread.

        Returns:
            Current thread transaction depth.
        """
        return int(getattr(self._local, "transaction_depth", 0))

    @_transaction_depth.setter
    def _transaction_depth(self, value: int) -> None:
        """Set transaction depth for the current thread.

        Args:
            value: Transaction depth.
        """
        self._local.transaction_depth = value
