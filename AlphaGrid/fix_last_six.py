import os
import re

files_to_fix = [
    "Backend/tests/analytical_rules/imbalances/test_imbalance_lifecycle.py",
    "Backend/tests/analytical_rules/liquidity/test_pool_interactions.py"
]

for f in files_to_fix:
    if os.path.exists(f):
        content = open(f, 'r').read()
        # They both have evidence_data={}, without quality, because my previous script removed it.
        # Add quality back!
        content = re.sub(
            r"evidence_data=\{\},\n\s*(imbalance_identity|pool_identity)=",
            r"evidence_data={},\n            quality=EvidenceQualityMetadata(confidence=1.0, coverage=1.0, freshness=0.0, latency=0.0, source_quality=1.0, sample_size=1, stability=1.0),\n            superseded_by=None,\n            \g<1>=",
            content
        )
        
        # Some event instantiations in test_imbalance_lifecycle.py might also need superseded_by. Let's fix ImbalanceDetectedEventDTO
        if "test_imbalance_lifecycle.py" in f:
            content = re.sub(
                r"quality=EvidenceQualityMetadata\([^)]+\),(\s+)event_id=",
                r"quality=EvidenceQualityMetadata(confidence=1.0, coverage=1.0, freshness=0.0, latency=0.0, source_quality=1.0, sample_size=1, stability=1.0),\g<1>superseded_by=None,\g<1>event_id=",
                content
            )

        open(f, 'w').write(content)
