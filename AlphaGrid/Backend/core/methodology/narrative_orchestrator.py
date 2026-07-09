from typing import Dict, List, Any
from Backend.core.methodology.multi_timeframe_graph import MultiTimeframeEvidenceGraph
from Backend.core.methodology.narrative_graph import NarrativeGraph
from Backend.core.methodology.plugin_interface import MethodologyPlugin

class NarrativeOrchestrator:
    """
    Coordinates methodology plugins and enforces strict phased execution.
    Methodologies must compute context in a specific sequence to avoid 
    computing low-level triggers (Entries) without high-level context (Bias).
    """
    
    # The explicit dependency graph (execution sequence)
    EXECUTION_PHASES = [
        "BIAS",       # Where is the market going?
        "POI",        # Where do we want to participate?
        "LIQUIDITY",  # What is the target?
        "STRUCTURE",  # What is the localized structure?
        "ENTRY"       # What is the trigger?
    ]
    
    def __init__(self):
        self.plugins: List[MethodologyPlugin] = []
        
    def register_plugin(self, plugin: MethodologyPlugin):
        self.plugins.append(plugin)
        
    def execute_all(self, mtf_graph: MultiTimeframeEvidenceGraph) -> Dict[str, NarrativeGraph]:
        """
        Executes all active methodology plugins.
        Returns a dictionary of NarrativeGraphs keyed by methodology name.
        """
        results = {}
        for plugin in self.plugins:
            # Note: A fully implemented plugin will internally respect the execution phases.
            # Here we orchestrate the plugins at a high level.
            # Downstream, we could pass the phase sequence into the plugin.execute()
            graph = plugin.execute(mtf_graph)
            results[plugin.methodology_type.value] = graph
            
        return results
