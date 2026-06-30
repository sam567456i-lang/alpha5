"""Database module exception hierarchy."""

from __future__ import annotations

from Backend.foundation import AlphaGridError


class DatabaseError(AlphaGridError):
    """Base exception for database module failures."""


class DatabaseConfigurationError(DatabaseError):
    """Raised when database configuration is invalid."""


class DatabaseDependencyError(DatabaseError):
    """Raised when a required database dependency is unavailable."""


class DatabaseConnectionError(DatabaseError):
    """Raised when a database connection cannot be established or used."""


class DatabaseTransactionError(DatabaseError):
    """Raised when a transaction cannot be completed safely."""


class DatabaseMigrationError(DatabaseError):
    """Raised when migration infrastructure cannot be configured."""


class DatabaseWritePolicyError(DatabaseError):
    """Raised when a write violates database ownership rules."""


class RepositoryError(DatabaseError):
    """Raised when generic repository operations fail."""
