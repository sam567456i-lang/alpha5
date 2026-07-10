from typing import Dict, Optional, TypeVar, Generic, List
from datetime import datetime
from Backend.core.evidence_dtos.base import BasePlatformObject, BasePlatformSnapshot, SchemaVersion

T = TypeVar('T', bound=BasePlatformObject)

class RepositoryTransaction(Generic[T]):
    """
    Enforces the strict multi-stage commit pipeline:
    Validation -> Begin -> Stage -> Graph Validation -> Commit -> Publication
    """
    def __init__(self, repository: 'BasePlatformRepository', integrity_service: 'IntegrityService'):
        self.repo = repository
        self.integrity_service = integrity_service
        self.staged_objects: Dict[str, T] = {}
        
    def stage(self, obj: T):
        self.staged_objects[obj.identity.uuid] = obj

    def commit(self) -> bool:
        # Phase: Graph Validation
        for obj in self.staged_objects.values():
            if not self.integrity_service.validate_graph(obj):
                self.rollback()
                return False
                
        # Phase: Commit
        for obj in self.staged_objects.values():
            self.repo._save_internal(obj)
            
        # Phase: Publication (Implicit - objects are now available via find_by_uuid)
        self.staged_objects.clear()
        return True

    def rollback(self):
        self.staged_objects.clear()

class BasePlatformRepository(Generic[T]):
    """
    Generic repository for storing, retrieving, and snapshotting durable objects.
    STRICTLY FORBIDDEN from containing analytical business logic.
    """
    def __init__(self):
        # Maps UUID -> Object
        self._objects: Dict[str, T] = {}
        # Maps UUID -> List of Snapshots (Append Only)
        self._snapshots: Dict[str, List[BasePlatformSnapshot]] = {}
        
    def _save_internal(self, obj: T):
        self._objects[obj.identity.uuid] = obj
        
        # Create immutable snapshot on commit
        snapshot = BasePlatformSnapshot(
            uuid=obj.identity.uuid,
            analytical_revision=obj.analytical_revision,
            operational_revision=obj.operational_revision,
            schema_version=SchemaVersion(1, 0, 0),
            payload={}, # Serialized payload would go here
            timestamp=datetime.now()
        )
        if obj.identity.uuid not in self._snapshots:
            self._snapshots[obj.identity.uuid] = []
        self._snapshots[obj.identity.uuid].append(snapshot)
        
    def find_by_uuid(self, uuid: str) -> Optional[T]:
        """Retrieves an object by its immutable identity."""
        return self._objects.get(uuid)
        
    def get_snapshots(self, uuid: str) -> List[BasePlatformSnapshot]:
        return self._snapshots.get(uuid, [])

    def delete(self, uuid: str):
        """Removes an object from the active graph, but snapshots remain untouched."""
        if uuid in self._objects:
            del self._objects[uuid]

    def all(self) -> list[T]:
        return list(self._objects.values())

class LiquidityRepository(BasePlatformRepository):
    """
    Specialized repository for Liquidity Objects (Reference, Swing, Session, Range, Pools).
    """
    pass

