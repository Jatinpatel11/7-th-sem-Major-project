"""
Custom exceptions for data service error handling.
"""


class DataServiceError(Exception):
    """Base exception for data service errors."""
    pass


class InvalidSymbolError(DataServiceError):
    """Raised when stock symbol is invalid or not found."""
    pass


class APIRateLimitError(DataServiceError):
    """Raised when API rate limit is exceeded."""
    pass


class NetworkError(DataServiceError):
    """Raised when network connectivity issues occur."""
    pass


class DataNotAvailableError(DataServiceError):
    """Raised when data is not available for the requested symbol."""
    pass
