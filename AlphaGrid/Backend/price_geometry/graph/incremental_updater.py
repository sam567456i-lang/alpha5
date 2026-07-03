from typing import List, Any
from Backend.price_geometry.events import GeometryEvent
from Backend.price_geometry.graph.geometry_graph import GeometryGraph
from Backend.price_geometry.objects import LifecycleState

class IncrementalGeometryUpdates:
    """
    Consumes GeometryEvents from the Event Bus and applies them
    incrementally to the Canonical Geometry Graph.
    """
    def __init__(self, graph: GeometryGraph):
        self.graph = graph
        
    def handle_event(self, event: GeometryEvent) -> None:
        """Route domain events to graph mutations."""
        event_type = event.__class__.__name__
        
        # When a geometry object is created, we add it as a node.
        if event_type in ("SwingCreated", "BOSCreated", "LiquidityCreated"):
            self.graph.add_object(event.geometry_obj)
            
        # When an object is invalidated (e.g. Swept Liquidity or Filled FVG)
        elif event_type in ("FVGFilled", "BOSInvalidated"):
            # The event might carry the mutated object or just ID
            self.graph.update_object_state(
                event.geometry_obj.id, 
                LifecycleState.INVALIDATED,
                mitigated_price=getattr(event.geometry_obj, 'mitigated_price', None)
            )
            
    def process_batch(self, events: List[GeometryEvent]) -> None:
        """Process a batch of events sequentially."""
        # Sort events by timestamp strictly
        sorted_events = sorted(events, key=lambda e: e.timestamp)
        for e in sorted_events:
            self.handle_event(e)
