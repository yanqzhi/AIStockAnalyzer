"""Project exception definitions."""


class AIStockAnalyzerError(Exception):
    """Base exception for AI Stock Analyzer errors."""


class ConfigurationError(AIStockAnalyzerError):
    """Raised when application configuration is invalid."""


class InfrastructureError(AIStockAnalyzerError):
    """Raised when infrastructure setup or access fails."""


class ValidationError(AIStockAnalyzerError):
    """Raised when input validation fails."""
