from Backend.core.interfaces.core_interfaces import ISnapshotStore
from typing import Optional

class SnapshotManager(ISnapshotStore):
    """
    Serializes state at three granularity levels:
    - Light: Graph only
    - Normal: Graph + Feature Store
    - Full: Entire runtime (Graph + Features + Queues + Config + Plugins)
    """
    def __init__(self):
        self.snapshots = {}
        
    def save_snapshot(self, snapshot_id: str, data: bytes, level: str = "NORMAL"):
        if level not in ["LIGHT", "NORMAL", "FULL"]:
            raise ValueError(f"Invalid snapshot level: {level}")
            
        self.snapshots[snapshot_id] = {
            "level": level,
            "data": data
        }
        
    def load_snapshot(self, snapshot_id: str) -> Optional[bytes]:
        snap = self.snapshots.get(snapshot_id)
        if snap:
            return snap["data"]
        return None
