import pandas as pd
from typing import List, Any, Dict
from datetime import datetime
import graphlib

from Backend.price_geometry.cache import GeometryCache
from Backend.price_geometry.factory import GeometryFactory
from Backend.price_geometry.registry import EngineRegistry

class GeometryEngineOrchestrator:
    """
    Master orchestrator for Structural Intelligence Platform.
    Runs individual geometry engines in a topological DAG, feeding results into the shared cache.
    """
    def __init__(self):
        self.registry = EngineRegistry()
        self.factory = GeometryFactory(self.registry)
        
        # Discover and instantiate all engines in this module
        self.factory.discover_engines()
        for name in self.factory._engine_classes.keys():
            self.factory.create_engine(name)
        
        # Build DAG
        self._build_dag()

    def _build_dag(self):
        self.engines = {}
        graph = {}
        for engine in self.registry.get_all():
            name = engine.engine_name
            self.engines[name] = engine
            # get_dependencies might not exist on older engines, default to []
            deps = getattr(engine, 'get_dependencies', lambda: [])()
            graph[name] = deps
            
        # Topologically sort engines
        sorter = graphlib.TopologicalSorter(graph)
        try:
            self.engine_sequence = list(sorter.static_order())
        except graphlib.CycleError as e:
            raise ValueError(f"Cycle detected in Geometry Engine DAG: {e}")

    def process_all(self, data: pd.DataFrame, context: Any) -> Dict[str, Any]:
        """
        Run the full geometry pipeline.
        Must receive a context containing 'geometry_cache', 'symbol', etc.
        """
        cache: GeometryCache = getattr(context, 'geometry_cache', None)
        if not cache:
            raise ValueError("GeometryEngineOrchestrator requires context.geometry_cache")
            
        new_objects = []
        symbol = getattr(context, 'symbol', None)
        
        # Execute topologically
        for name in self.engine_sequence:
            engine = self.engines[name]
            
            # Inject required dependencies into context dynamically based on cache
            # This enables engines to request specific lists (e.g., context.swings)
            setattr(context, 'swings', cache.get_by_type("Swing", symbol))
            setattr(context, 'pivots', cache.get_by_type("Pivot", symbol))
            setattr(context, 'structures', cache.get_by_type("Structure", symbol))
            setattr(context, 'existing_imbalances', cache.get_by_type("Imbalance", symbol))
            setattr(context, 'existing_pools', cache.get_by_type("Liquidity", symbol))
            setattr(context, 'existing_obs', cache.get_by_type("OrderBlock", symbol))
            
            outputs = engine.process(data, context)
            for obj in outputs:
                # Add to cache (cache handles deduplication by ID or updates if ID matches)
                cache.add(obj)
                new_objects.append(obj)
                
        # Generate summary snapshot
        snapshot = {
            "symbol": symbol or 'unknown',
            "timeframe": getattr(context, 'timeframe', 'unknown'),
            "timestamp": data.index[-1].isoformat() if not data.empty else datetime.utcnow().isoformat(),
            "new_objects_count": len(new_objects),
            "total_pivots": len(cache.get_by_type("Pivot", symbol)),
            "total_swings": len(cache.get_by_type("Swing", symbol)),
            "total_structures": len(cache.get_by_type("Structure", symbol)),
            "total_imbalances": len(cache.get_by_type("Imbalance", symbol)),
            "total_liquidity": len(cache.get_by_type("Liquidity", symbol)),
            "total_order_blocks": len(cache.get_by_type("OrderBlock", symbol)),
        }
        
        return snapshot
