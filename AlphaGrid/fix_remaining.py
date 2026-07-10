import os
import re

files_with_region_quality = [
    "Backend/tests/analytical_rules/auction/test_auction_logic.py",
    "Backend/tests/analytical_rules/imbalances/test_derived_imbalances.py",
    "Backend/tests/analytical_rules/imbalances/test_imbalance_lifecycle.py",
    "Backend/tests/analytical_rules/institutional_zones/test_derived_institutional_zones.py",
    "Backend/tests/analytical_rules/liquidity/test_pool_interactions.py"
]

for f in files_with_region_quality:
    if os.path.exists(f):
        content = open(f, 'r').read()
        # RegionState doesn't take quality or superseded_by. 
        # Remove them if they were injected between evidence_data={}, and region_identity=
        content = re.sub(
            r"evidence_data=\{\},\s*quality=EvidenceQualityMetadata\([^)]+\),\s*superseded_by=None,", 
            r"evidence_data={},", 
            content
        )
        content = re.sub(
            r"evidence_data=\{\},\s*quality=EvidenceQualityMetadata\([^)]+\),", 
            r"evidence_data={},", 
            content
        )
        open(f, 'w').write(content)

f_engine = "Backend/core/analytical_rules/capabilities/liquidity/pool_lifecycle_engine.py"
if os.path.exists(f_engine):
    content = open(f_engine, 'r').read()
    content = content.replace("evidence_data=current_state.evidence_data,", "evidence_data=current_state.evidence_data,\n            quality=current_state.quality,")
    open(f_engine, 'w').write(content)

f_pool_test = "Backend/tests/analytical_rules/liquidity/test_pool_lifecycle.py"
if os.path.exists(f_pool_test):
    content = open(f_pool_test, 'r').read()
    # Missing superseded_by in PoolDetectedEventDTO
    content = re.sub(
        r"quality=EvidenceQualityMetadata\([^)]+\),(\s+)event_id=",
        r"quality=EvidenceQualityMetadata(confidence=1.0, coverage=1.0, freshness=0.0, latency=0.0, source_quality=1.0, sample_size=1, stability=1.0),\g<1>superseded_by=None,\g<1>event_id=",
        content
    )
    open(f_pool_test, 'w').write(content)
