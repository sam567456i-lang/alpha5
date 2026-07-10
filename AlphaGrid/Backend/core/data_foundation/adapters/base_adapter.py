from abc import ABC, abstractmethod
from typing import Iterator, Dict, Any
from Backend.core.data_foundation.contracts.schemas import ContractValidator

class BaseIngestionAdapter(ABC):
    """Base plugin for vendor-specific data ingestion."""
    
    def __init__(self, source_metadata: Any):
        self.source = source_metadata
        
    @abstractmethod
    def connect(self):
        pass
        
    @abstractmethod
    def fetch_data(self, symbol: str, start_time: str, end_time: str) -> Iterator[Dict[str, Any]]:
        """Must yield raw dicts that map perfectly to the Data Contracts."""
        pass
        
    def ingest(self, symbol: str, start_time: str, end_time: str) -> Iterator[Any]:
        self.connect()
        for raw_data in self.fetch_data(symbol, start_time, end_time):
            # The adapter is responsible for validating contracts as it streams
            # This ensures garbage data crashes the ingest process immediately
            valid_record = ContractValidator.validate_ohlc(raw_data)
            yield valid_record
