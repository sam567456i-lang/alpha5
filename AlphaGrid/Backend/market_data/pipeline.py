from abc import ABC, abstractmethod
from typing import Any
from Backend.dtos.provider import DataQualityScore
from Backend.core.events import EventProvenance, CanonicalMarketEvent, EnrichedMarketEvent

class IValidator(ABC):
    @abstractmethod
    def validate(self, raw_payload: Any) -> DataQualityScore: pass

class INormalizer(ABC):
    @abstractmethod
    def normalize(self, raw_payload: Any, quality: DataQualityScore, provenance: EventProvenance) -> CanonicalMarketEvent: pass

class IDerivedDataGenerator(ABC):
    @abstractmethod
    def enrich(self, event: CanonicalMarketEvent) -> EnrichedMarketEvent: pass

class IStorageEngine(ABC):
    @abstractmethod
    async def store(self, event: CanonicalMarketEvent) -> bool: pass

class IPublisher(ABC):
    @abstractmethod
    async def publish(self, event: CanonicalMarketEvent) -> None: pass

class IRawFeedIngester(ABC):
    @abstractmethod
    async def ingest(self, raw_payload: Any) -> Any: pass
