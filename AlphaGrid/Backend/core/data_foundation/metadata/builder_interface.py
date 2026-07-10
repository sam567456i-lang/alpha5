from abc import ABC, abstractmethod
from typing import Iterator, Any
from Backend.core.data_foundation.contracts.schemas import DatasetDefinition, DatasetManifest

class DatasetBuilder(ABC):
    """
    Contract for constructing an immutable dataset.
    This interface guarantees that all generated datasets produce a valid manifest.
    """
    
    @abstractmethod
    def build(self, definition: DatasetDefinition, data_stream: Iterator[Any]) -> DatasetManifest:
        """
        Consumes a validated stream of data (OHLC or Ticks), writes it to the underlying storage,
        and produces an immutable DatasetManifest.
        """
        pass
