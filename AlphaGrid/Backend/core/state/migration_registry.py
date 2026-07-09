from typing import Dict, Any, Callable

class MigrationRegistry:
    """Enforces strictly forward-only state migrations (V1 -> V2 -> V3)."""
    def __init__(self):
        self.migrations: Dict[str, Callable[[Any], Any]] = {}
        
    def register_migration(self, from_version: int, to_version: int, migrator: Callable[[Any], Any]):
        if to_version <= from_version:
            raise ValueError("Migrations must be strictly forward.")
        migration_key = f"{from_version}->{to_version}"
        self.migrations[migration_key] = migrator
        
    def migrate(self, data: Any, from_version: int, to_version: int) -> Any:
        migration_key = f"{from_version}->{to_version}"
        migrator = self.migrations.get(migration_key)
        if not migrator:
            raise ValueError(f"No forward migration found for {migration_key}")
        return migrator(data)

class ExportAdapter:
    """Optional adapter to export current state to a legacy format."""
    def export(self, current_data: Any, target_legacy_version: int) -> Any:
        raise NotImplementedError("Legacy export adapters are strictly opt-in.")
