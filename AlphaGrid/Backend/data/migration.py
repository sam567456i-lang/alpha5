"""Alembic migration infrastructure helpers."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .exceptions import DatabaseDependencyError, DatabaseMigrationError
from .settings import MigrationSettings


@dataclass(frozen=True, slots=True)
class MigrationManager:
    """Build Alembic configuration for migration commands."""

    settings: MigrationSettings
    database_url: str

    def build_config(self) -> object:
        """Return an Alembic config object."""

        if not self.settings.config_path.exists():
            raise DatabaseMigrationError(
                f"Alembic config does not exist: {self.settings.config_path}"
            )
        if not self.settings.script_location.exists():
            raise DatabaseMigrationError(
                f"Alembic script location does not exist: {self.settings.script_location}"
            )
        try:
            from alembic.config import Config
        except ModuleNotFoundError as exc:
            raise DatabaseDependencyError("alembic is required for migrations.") from exc

        config = Config(str(self.settings.config_path))
        config.set_main_option("script_location", str(self.settings.script_location))
        config.set_main_option("sqlalchemy.url", self.database_url)
        return config


def migration_base_path(project_root: str | Path) -> Path:
    """Return the migration base location inside the frozen structure."""

    return Path(project_root) / "Database" / "migrations"
