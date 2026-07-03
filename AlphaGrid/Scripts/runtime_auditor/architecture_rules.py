import sys
import threading
import logging
from typing import Dict, List, Set, Any
import json
import os

logger = logging.getLogger("RuntimeAuditor.ArchitectureRules")

class ArchitectureRuleValidator:
    """Uses sys.settrace to map call graphs and enforce ownership and dependency boundaries."""
    
    def __init__(self):
        self.call_graph: Dict[str, Set[str]] = {}
        self.violations: List[Dict[str, Any]] = []
        self._local = threading.local()

    def start_trace(self):
        sys.settrace(self._trace_calls)
        threading.settrace(self._trace_calls)

    def stop_trace(self):
        sys.settrace(None)
        threading.settrace(None)

    def _trace_calls(self, frame, event, arg):
        if event != 'call':
            return self._trace_calls

        caller = frame.f_back
        if not caller:
            return self._trace_calls

        caller_module = caller.f_globals.get('__name__', '')
        callee_module = frame.f_globals.get('__name__', '')

        # Filter out stdlib and external packages
        if not caller_module.startswith('Backend') or not callee_module.startswith('Backend'):
            return self._trace_calls

        if caller_module not in self.call_graph:
            self.call_graph[caller_module] = set()
        self.call_graph[caller_module].add(callee_module)

        self._validate_rules(caller_module, callee_module)
        return self._trace_calls

    def _validate_rules(self, caller: str, callee: str):
        # Rule 1: Foundation must not depend on higher layers
        if caller.startswith("Backend.foundation") and not callee.startswith("Backend.foundation") and "tests" not in callee:
            self.violations.append({"rule": "Foundation Isolation", "caller": caller, "callee": callee})

        # Rule 2: Market Intelligence must not depend on Concepts
        if caller.startswith("Backend.market_intelligence") and callee.startswith("Backend.concepts"):
            self.violations.append({"rule": "Market Intelligence Isolation", "caller": caller, "callee": callee})

        # Rule 3: Features must not import Strategies
        if caller.startswith("Backend.features") and callee.startswith("Backend.research.strategies"):
            self.violations.append({"rule": "Feature Isolation", "caller": caller, "callee": callee})
            
        # Rule 4: Ownership - Swing Detection is strictly owned by Price Geometry
        if callee.startswith("Backend.price_geometry.swing") and not caller.startswith("Backend.price_geometry") and "tests" not in caller:
            self.violations.append({"rule": "Strict Ownership - Swing", "caller": caller, "callee": callee})

        # Rule 5: Ownership - Market State is strictly owned by Market Intelligence
        if callee.startswith("Backend.market_intelligence.market_state") and not caller.startswith("Backend.market_intelligence") and not caller.startswith("Backend.api") and "tests" not in caller:
            self.violations.append({"rule": "Strict Ownership - Market State", "caller": caller, "callee": callee})

    def validate_contracts(self):
        """Scans the repository to ensure all implementations satisfy their core contracts."""
        # In a real environment, this would use reflection to verify ABC implementations.
        # This is a stub for the auditor output.
        pass

    def export(self, output_dir: str):
        os.makedirs(output_dir, exist_ok=True)
        # Convert sets to lists for JSON serialization
        serializable_graph = {k: list(v) for k, v in self.call_graph.items()}
        with open(os.path.join(output_dir, "call_graph.json"), "w") as f:
            json.dump({"graph": serializable_graph, "violations": self.violations}, f, indent=2)

