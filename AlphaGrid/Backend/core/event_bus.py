"""
DEPRECATED: Core Event Bus wrapper.
The actual implementation resides in Backend/foundation/event_bus.py.
This file is maintained solely for backward compatibility and layer separation.
"""

from Backend.foundation.event_bus import (
    EventBus, 
    Event, 
    EventHandler,
    Priority
)

# Export the foundation event bus classes directly
__all__ = [
    "EventBus",
    "Event", 
    "EventHandler",
    "Priority"
]
