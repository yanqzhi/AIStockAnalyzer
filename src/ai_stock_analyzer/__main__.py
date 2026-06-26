"""Application entry point."""

import sys
from collections.abc import Sequence
from logging import Logger
from typing import cast

from PySide6.QtWidgets import QApplication

from ai_stock_analyzer.config import Settings
from ai_stock_analyzer.database import DatabaseManager
from ai_stock_analyzer.presentation.main_window import MainWindow
from ai_stock_analyzer.utils import configure_logger


def main(argv: Sequence[str] | None = None) -> int:
    """Start the AI Stock Analyzer desktop application.

    Args:
        argv: Optional command-line arguments.

    Returns:
        Application exit code.
    """
    logger: Logger | None = None
    database_manager: DatabaseManager | None = None

    try:
        settings = Settings()
        logger = configure_logger(__name__, settings.logging)
        database_manager = DatabaseManager(settings.database.path)
        app = _create_application(argv)
        window = MainWindow()
        window.show()

        return int(app.exec())
    except Exception:
        if logger is not None:
            logger.exception("Application failed to start")

        return 1
    finally:
        if database_manager is not None:
            database_manager.close()


def _create_application(argv: Sequence[str] | None = None) -> QApplication:
    """Create or return the current QApplication.

    Args:
        argv: Optional command-line arguments.

    Returns:
        QApplication instance.
    """
    existing_application = QApplication.instance()

    if existing_application is not None:
        return cast(QApplication, existing_application)

    arguments = list(sys.argv if argv is None else argv)
    return QApplication(arguments)


if __name__ == "__main__":
    raise SystemExit(main())
