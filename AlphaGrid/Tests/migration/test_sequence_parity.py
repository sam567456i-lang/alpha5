import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from Backend.core.methodology.legacy_archive.ict.sequence import ICTSequenceEngine
from Backend.core.methodology.narrative_node import NarrativeNode
from Backend.core.methodology.narrative_types import NarrativeNodeType, NarrativeStage
from Backend.core.methodology.evaluators.sequence_evaluator import SequenceEvaluator
from Backend.core.methodology.dto.base_candidate import SequenceCandidate, CandidateIdentity
from Backend.core.methodology.dto.base_evaluation import PassedEvaluation
from Backend.core.methodology.dto.base_interpretation import SequenceInterpretation, InterpretationIdentity
from Backend.core.methodology.projections.engine import ProjectionRegistry, ProjectionEngine
from Backend.core.methodology.projections.dto import NarrativeProjectionSpecification, DashboardProjectionSpecification
from test_parity_harness import ParityHarness
import datetime

def run_tests():
    legacy_engine = ICTSequenceEngine()
    
    def legacy_func(data):
        nodes = []
        for i, (ctype, cname) in enumerate(data):
            node = NarrativeNode(
                node_id=f"n_{i}",
                identity=None,
                concept_type=ctype,
                concept_name=cname,
                stage=NarrativeStage.EXECUTION,
                producer_plugin="ICTPlugin",
                producer_policy="v1.0"
            )
            nodes.append(node)
            
        sequences = legacy_engine.evaluate(nodes)
        
        configs = [seq.producer_policy for seq in sequences]
        configs.sort()
        return {"matched_labels": configs}

    # Platform 11 mapping: Generic Sequence Evaluator + ICT Projection Engine
    
    sequence_evaluator = SequenceEvaluator(policy_config={
        "sequences": [
            {
                "pattern": "consolidation-sweep-expansion-entry", 
                "requires": ["consolidation", "sweep", "expansion", "entry"]
            },
            {
                "pattern": "open-sweep-reversal",
                "requires": ["open", "sweep", "reversal"]
            }
        ]
    })
    
    registry = ProjectionRegistry()
    registry.register(NarrativeProjectionSpecification())
    registry.register(DashboardProjectionSpecification())
    
    ict_profile_rules = {
        "SequenceInterpretation": {
            "consolidation-sweep-expansion-entry": "AMD",
            "open-sweep-reversal": "JUDAS_SWING"
        }
    }
    projection_engine = ProjectionEngine(registry, ict_profile_rules)
    
    def plat11_func(data):
        # Translate the legacy node mock data into the generic elements Platform 11 expects upstream.
        # This mirrors how the CandidateBuilder translates upstream interpretations into elements.
        generic_mapping = {
            "ASIAN": "consolidation",
            "Sweep": "sweep",
            "CHOCH": "expansion",
            "MSS": "expansion",
            "OTE": "entry",
            "OPEN": "open",
            "Reversal": "reversal"
        }
        
        ordered_elements = []
        for ctype, cname in data:
            # simple mock translation
            for k, v in generic_mapping.items():
                if k in cname:
                    ordered_elements.append(v)
                    break
            else:
                ordered_elements.append(cname.lower())
                
        identity = CandidateIdentity(
            id="cand_seq",
            derived_from="chronological_group",
            policy="v1",
            profile="Generic",
            evaluation_id=None,
            sequence=1,
            created_at=datetime.datetime.now()
        )
        candidate = SequenceCandidate(
            identity=identity,
            ordered_elements=ordered_elements
        )
        
        result = sequence_evaluator.evaluate(candidate, context={})
        
        if isinstance(result, PassedEvaluation):
            interp_identity = InterpretationIdentity(
                id="interp_seq",
                methodology_id="generic",
                profile_id="ICT",
                evaluation_id="eval_1",
                candidate_id="cand_seq",
                version="v1",
                hash="mock_hash",
                created=datetime.datetime.now(),
                sequence=1,
                timeframe="M5"
            )
            interp = SequenceInterpretation(
                identity=interp_identity,
                sequence_pattern=result.metadata["matched_patterns"][0],
                event_order=result.metadata["event_order"],
                constraints_satisfied=result.metadata["constraints_satisfied"],
                coverage=result.metadata["coverage"]
            )
            
            projections = projection_engine.project(interp, consumer="Dashboard")
            
            configs = [p.label for p in projections]
            configs.sort()
            return {"matched_labels": configs}
        else:
            return {"matched_labels": []}

    # Test Case 1: AMD Match
    ParityHarness.assert_parity(
        input_data=[
            (NarrativeNodeType.SESSION_CONTEXT, "ASIAN Range"),
            (NarrativeNodeType.STRUCTURE_NARRATIVE, "Liquidity Sweep"),
            (NarrativeNodeType.STRUCTURE_NARRATIVE, "MSS"),
            (NarrativeNodeType.EXECUTION, "OTE Entry")
        ],
        legacy_func=legacy_func,
        platform11_func=plat11_func
    )
    
    # Test Case 2: Judas Swing Match
    ParityHarness.assert_parity(
        input_data=[
            (NarrativeNodeType.SESSION_CONTEXT, "NY OPEN"),
            (NarrativeNodeType.STRUCTURE_NARRATIVE, "Sweep"),
            (NarrativeNodeType.STRUCTURE_NARRATIVE, "Reversal")
        ],
        legacy_func=legacy_func,
        platform11_func=plat11_func
    )
    
    # Test Case 3: Rejected
    ParityHarness.assert_parity(
        input_data=[
            (NarrativeNodeType.STRUCTURE_NARRATIVE, "Sweep"),
            (NarrativeNodeType.SESSION_CONTEXT, "ASIAN Range")
        ],
        legacy_func=legacy_func,
        platform11_func=plat11_func
    )

    print("[PASS] Sequence Evaluation & Projection Parity Test Passed")

if __name__ == "__main__":
    run_tests()
