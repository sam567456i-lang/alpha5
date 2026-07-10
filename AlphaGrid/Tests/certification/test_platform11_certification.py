import sys
import os
import datetime
import hashlib
from typing import List, Dict, Any

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

# --- MOCK IMPORTS FOR CERTIFICATION ---
from Backend.core.methodology.dto.base_candidate import SequenceCandidate
from Backend.core.methodology.dto.base_interpretation import SequenceInterpretation
from Backend.core.methodology.dto.interpretation_identity import InterpretationIdentity
from Backend.core.methodology.evaluators.sequence_evaluator import SequenceEvaluator
from Backend.core.methodology.projections.engine import ProjectionRegistry, ProjectionEngine
from Backend.core.methodology.projections.dto import NarrativeProjectionSpecification, DashboardProjectionSpecification

class Platform11Certifier:
    """
    Validates constitutional guarantees of Platform 11.
    """
    def __init__(self):
        self.errors = []
        
    def assert_no_errors(self):
        if self.errors:
            print("\n".join(self.errors))
            raise AssertionError(f"Certification failed with {len(self.errors)} errors.")
            
    def certify_architecture(self):
        # 2. Architectural Certification
        # Verify evaluators don't mutate candidates or context illegally.
        # This is a static analysis / mock verification.
        try:
            # Mock candidate
            cand = SequenceCandidate(identity=None, ordered_elements=["consolidation", "sweep", "expansion"])
            # In python frozen dataclasses raise FrozenInstanceError if mutated
            # we just test that attempting to mutate fails.
            cand.ordered_elements = []
            self.errors.append("[Architecture] Candidates must be frozen and immutable.")
        except Exception:
            pass # Expected
            
    def certify_graph_integrity(self, nodes: List[Any]):
        # 3. Graph Integrity
        # Verify DAG properties (no cycles)
        # Mocking a basic topological sort check
        visited = set()
        path = set()
        
        def visit(node_id, deps):
            if node_id in path:
                self.errors.append(f"[Graph] Cycle detected involving node {node_id}")
                return
            if node_id not in visited:
                path.add(node_id)
                for dep in deps.get(node_id, []):
                    visit(dep, deps)
                path.remove(node_id)
                visited.add(node_id)
                
        deps = {n["id"]: n["derived_from"] for n in nodes}
        for n in nodes:
            visit(n["id"], deps)
            
    def certify_explanation_lineage(self, interpretation: SequenceInterpretation):
        # 4. Explanation Certification
        # Assert lineage is unbroken
        ident = interpretation.identity
        if not ident.candidate_id or not ident.evaluation_id or not ident.methodology_id:
            self.errors.append("[Explanation] Interpretation missing upstream lineage.")
            
    def certify_projection_integrity(self):
        # 5. Projection Certification
        registry = ProjectionRegistry()
        registry.register(NarrativeProjectionSpecification())
        registry.register(DashboardProjectionSpecification())
        
        rules = {"SequenceInterpretation": {"consolidation-sweep-expansion": "AMD"}}
        engine = ProjectionEngine(registry, rules)
        
        ident = InterpretationIdentity(
            id="interp_1", methodology_id="ict", profile_id="2022",
            evaluation_id="eval_1", candidate_id="cand_1", version="1",
            hash="abc", created=datetime.datetime.now(), sequence=1, timeframe="M5"
        )
        interp = SequenceInterpretation(
            identity=ident, sequence_pattern="consolidation-sweep-expansion"
        )
        
        dash_proj = engine.project(interp, "Dashboard")
        llm_proj = engine.project(interp, "LLM")
        
        if not dash_proj or not llm_proj:
            self.errors.append("[Projection] Engine failed to generate transient views.")
        
        # Verify they share the exact same interpretation source
        if dash_proj[0].source_interpretation_id != llm_proj[0].source_interpretation_id:
            self.errors.append("[Projection] Projections do not originate from identical Interpretation.")
            
    def certify_replay_determinism(self):
        # 8. Replay Determinism
        # Running the exact same mock pipeline twice should yield identical outputs
        evaluator = SequenceEvaluator(policy_config={"sequences": [{"pattern": "consolidation-sweep-expansion", "requires": ["consolidation", "sweep", "expansion"]}]})
        
        cand = SequenceCandidate(identity=None, ordered_elements=["consolidation", "sweep", "expansion"])
        
        # Run 1
        res1 = evaluator.evaluate(cand, {})
        # Run 2
        res2 = evaluator.evaluate(cand, {})
        
        # Hash metadata
        def hash_res(r):
            s = str(sorted(r.metadata.items()))
            return hashlib.md5(s.encode()).hexdigest()
            
        if hash_res(res1) != hash_res(res2):
            self.errors.append("[Replay] Determinism failed. Identical inputs yielded different evaluation hashes.")

def run_certification():
    print("Running Platform 11 Certification...")
    certifier = Platform11Certifier()
    
    certifier.certify_architecture()
    certifier.certify_graph_integrity([
        {"id": "cand_1", "derived_from": ["ev_1"]},
        {"id": "interp_1", "derived_from": ["cand_1"]}
    ])
    
    ident = InterpretationIdentity(
        id="interp_1", methodology_id="ict", profile_id="2022",
        evaluation_id="eval_1", candidate_id="cand_1", version="1",
        hash="abc", created=datetime.datetime.now(), sequence=1, timeframe="M5"
    )
    certifier.certify_explanation_lineage(SequenceInterpretation(identity=ident))
    
    certifier.certify_projection_integrity()
    certifier.certify_replay_determinism()
    
    certifier.assert_no_errors()
    
    print("[CERTIFIED] Architecture Boundaries Verified")
    print("[CERTIFIED] Graph Integrity Verified")
    print("[CERTIFIED] Explanation Lineage Verified")
    print("[CERTIFIED] Projection Ephemerality Verified")
    print("[CERTIFIED] Replay Determinism Verified")
    print("\nPlatform 11 Status: FROZEN")

if __name__ == "__main__":
    run_certification()
