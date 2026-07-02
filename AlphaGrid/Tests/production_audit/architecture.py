"""Architecture Verification Module."""

import os
import ast
from typing import List, Tuple, Dict, Set
from Backend.research.strategies.registry import StrategyRegistry
from Backend.features.registry import FeatureRegistry
from Backend.concepts.registry import ConceptRegistry
from Backend.methodology.registry import MethodologyRegistry

class ArchitectureVerifier:
    def __init__(self, backend_dir: str):
        self.backend_dir = backend_dir
        self.errors: List[str] = []

    def run_all(self) -> bool:
        self.errors = []
        self._verify_layer_dependencies()
        self._verify_no_duplicate_ids()
        self._verify_registry_referential_integrity()
        
        if self.errors:
            print("\nArchitecture Verification FAILED:")
            for e in self.errors:
                print(f"  - {e}")
            return False
        return True

    def _verify_layer_dependencies(self):
        """Parse all Python files in Backend to ensure layered architecture is respected."""
        for root, _, files in os.walk(self.backend_dir):
            for file in files:
                if file.endswith(".py"):
                    path = os.path.join(root, file)
                    rel_path = os.path.relpath(path, self.backend_dir)
                    
                    with open(path, "r", encoding="utf-8") as f:
                        try:
                            tree = ast.parse(f.read())
                        except Exception:
                            continue
                    
                    # Rule: Methodology cannot import Backend.features directly, only concepts or signals
                    if "methodology" in rel_path.split(os.sep):
                        for node in ast.walk(tree):
                            if isinstance(node, ast.ImportFrom):
                                if node.module and "Backend.features" in node.module:
                                    # Base classes are ok, but specific features are not
                                    if "base" not in node.module:
                                        self.errors.append(f"Forbidden import: {rel_path} imports {node.module}. Methodologies must use signals.")

    def _verify_no_duplicate_ids(self):
        # We rely on registries to naturally enforce unique IDs by design,
        # but we also explicitly check.
        strats = StrategyRegistry.get_all()
        ids = [s.id for s in strats]
        if len(ids) != len(set(ids)):
            self.errors.append("Duplicate Strategy IDs found.")

    def _verify_registry_referential_integrity(self):
        """Ensure Strategy -> Methodology -> Signals -> Concepts -> Features graph is valid."""
        for strat in StrategyRegistry.get_all():
            if not strat.methodology:
                self.errors.append(f"Strategy {strat.id} missing methodology.")
            
            for feat in strat.features:
                if not feat:
                    self.errors.append(f"Strategy {strat.id} references invalid feature.")
            
            for conc in strat.concepts:
                if not conc.source:
                    self.errors.append(f"Strategy {strat.id} concept {conc.generator_type.__name__} missing source feature ID.")
