"""Project skeleton tests."""

from ai_stock_analyzer import __version__
from ai_stock_analyzer.analysis import Analyzer
from ai_stock_analyzer.application import UseCase
from ai_stock_analyzer.broker import BrokerClient
from ai_stock_analyzer.config import Settings
from ai_stock_analyzer.database import DatabaseConnection
from ai_stock_analyzer.database.repositories import Repository
from ai_stock_analyzer.indicator import Indicator
from ai_stock_analyzer.presentation import MainWindow
from ai_stock_analyzer.service import Service


def test_package_version_is_defined() -> None:
    """Verify the package exposes a version."""
    assert __version__


def test_architecture_layer_contracts_are_importable() -> None:
    """Verify all architecture layer contracts are importable."""
    assert Analyzer
    assert BrokerClient
    assert DatabaseConnection
    assert Indicator
    assert MainWindow
    assert Repository
    assert Service
    assert Settings
    assert UseCase
