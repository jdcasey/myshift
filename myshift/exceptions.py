"""Custom exceptions for the myshift package."""


class MyshiftError(Exception):
    """Base exception class for myshift errors."""

    pass


class ConfigError(MyshiftError):
    """Raised when there is an error with configuration."""

    pass


class APIError(MyshiftError):
    """Raised when there is an error with the PagerDuty API."""

    pass


class ValidationError(MyshiftError):
    """Raised when input validation fails."""

    pass


class AuthenticationError(MyshiftError):
    """Raised when authentication with PagerDuty fails."""

    pass 