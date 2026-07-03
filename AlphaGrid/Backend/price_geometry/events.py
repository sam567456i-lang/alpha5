from dataclasses import dataclass
from Backend.price_geometry.objects import GeometryObject
from datetime import datetime

# In a real system, these would inherit from an AbstractDomainEvent from foundation.event_bus

@dataclass(frozen=True)
class GeometryEvent:
    event_id: str
    timestamp: datetime
    geometry_obj: GeometryObject

@dataclass(frozen=True)
class SwingCreated(GeometryEvent):
    pass

@dataclass(frozen=True)
class BOSCreated(GeometryEvent):
    pass

@dataclass(frozen=True)
class LiquidityCreated(GeometryEvent):
    pass

@dataclass(frozen=True)
class FVGFilled(GeometryEvent):
    pass

@dataclass(frozen=True)
class BOSInvalidated(GeometryEvent):
    pass
