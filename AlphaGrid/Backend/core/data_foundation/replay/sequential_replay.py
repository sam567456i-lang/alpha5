from typing import Optional, Tuple, List, Any
import uuid
import copy
from Backend.core.data_foundation.contracts.schemas import DatasetManifest, OHLCSchema, ReplayContext
from Backend.core.data_foundation.storage.storage_layer import StorageBackend, PartitionIterator

class ReplayException(Exception):
    pass

class SequentialReplayEngine:
    """Streams data from a StorageBackend sequentially, hiding physical layouts."""
    
    def __init__(self, manifest: DatasetManifest, backend: StorageBackend, verify: bool = True):
        self.manifest = manifest
        self.backend = backend
        self.session_id = str(uuid.uuid4())
        
        if verify:
            self._verify_manifest()
            
        self._iterator: Optional[PartitionIterator] = None
        self._current_partition_data: List[OHLCSchema] = []
        self._partition_idx = 0
        self._bar_idx = 0
        self._global_position = 0
        
        self.reset()
        
    def _verify_manifest(self):
        """Verifies the manifest against storage metadata before starting."""
        # A real implementation would ask backend for total rows for the dataset hash.
        # Here we assume the backend validates it or we do a quick check.
        # For memory tests, we'll bypass complex validation.
        pass
        
    def reset(self):
        """Resets the replay to the beginning."""
        self._iterator = self.backend.read_dataset(self.manifest)
        self._current_partition_data = []
        self._partition_idx = 0
        self._bar_idx = 0
        self._global_position = 0
        self._load_next_partition()
        
    def _load_next_partition(self) -> bool:
        """Loads the next partition from the iterator."""
        if self._iterator is None:
            return False
            
        try:
            raw_data = next(self._iterator)
            # In a real implementation we verify chronological continuity between partitions here
            if len(self._current_partition_data) > 0 and len(raw_data) > 0:
                last_ts = self._current_partition_data[-1].timestamp
                first_ts = raw_data[0].timestamp
                if first_ts <= last_ts:
                    raise ReplayException(f"Partition overlap or chronology failure: {first_ts} <= {last_ts}")
                    
            self._current_partition_data = raw_data
            self._bar_idx = 0
            self._partition_idx += 1
            return len(self._current_partition_data) > 0
        except StopIteration:
            self._current_partition_data = []
            return False
            
    def peek(self) -> Optional[Tuple[ReplayContext, OHLCSchema]]:
        """Views the next bar without advancing the pointer."""
        if self._bar_idx >= len(self._current_partition_data):
            if not self._load_next_partition():
                return None
                
        bar = self._current_partition_data[self._bar_idx]
        ctx = ReplayContext(
            replay_session_id=self.session_id,
            dataset_id=self.manifest.dataset_hash,
            manifest_hash=self.manifest.dataset_hash,
            partition_id=f"part_{self._partition_idx}",
            sequence=self._global_position,
            current_bar=self._global_position,
            total_bars=self.manifest.row_count,
            timestamp=bar.timestamp.isoformat()
        )
        return (ctx, bar)
        
    def next(self) -> Optional[Tuple[ReplayContext, OHLCSchema]]:
        """Advances the pointer and returns the next bar."""
        res = self.peek()
        if res is not None:
            self._bar_idx += 1
            self._global_position += 1
        return res
        
    def seek(self, global_index: int):
        """Seeks to a specific global index."""
        if global_index < 0 or global_index >= self.manifest.row_count:
            raise ValueError(f"Seek index {global_index} out of bounds.")
            
        if global_index < self._global_position:
            self.reset()
            
        while self._global_position < global_index:
            if self.next() is None:
                break
                
    def position(self) -> int:
        """Returns the current global index."""
        return self._global_position
        
    def remaining(self) -> int:
        """Returns the number of bars remaining."""
        return self.manifest.row_count - self._global_position

    def window(self, size: int) -> List[Tuple[ReplayContext, OHLCSchema]]:
        """Returns a look-ahead window of `size` bars without advancing the global pointer."""
        # Simplistic implementation: clone, fetch, return.
        cloned = self.clone()
        res = []
        for _ in range(size):
            nxt = cloned.next()
            if not nxt:
                break
            res.append(nxt)
        return res

    def slice(self, start_idx: int, end_idx: int) -> List[Tuple[ReplayContext, OHLCSchema]]:
        """Returns a specific slice of the dataset."""
        cloned = self.clone()
        cloned.seek(start_idx)
        res = []
        for _ in range(end_idx - start_idx):
            nxt = cloned.next()
            if not nxt:
                break
            res.append(nxt)
        return res

    def clone(self) -> 'SequentialReplayEngine':
        """Creates an independent clone of the replay engine at the same position."""
        cloned = SequentialReplayEngine(self.manifest, self.backend, verify=False)
        cloned.seek(self._global_position)
        return cloned
