import unittest
from datetime import datetime
from Backend.core.evidence_dtos.base import LifecycleState
from Backend.core.evidence_dtos.liquidity import SwingLiquidityObject, SwingLiquidityEvidence
from Backend.core.analytical_rules.liquidity_rules import SwingLiquiditySelectionRule, SwingLiquidityConstructionRule

class MockSwingEvidence:
    def __init__(self, price, tolerance, hierarchy_level, uuid):
        self.price = price
        self.tolerance = tolerance
        self.hierarchy_level = hierarchy_level
        self.identity = {'uuid': uuid}

class TestSwingLiquidity(unittest.TestCase):
    
    def test_selection_and_construction(self):
        # 1. Setup mock upstream SwingEvidence
        swings = [
            MockSwingEvidence(price=105.0, tolerance=0.1, hierarchy_level=1, uuid="SWING-1"),
            MockSwingEvidence(price=100.0, tolerance=0.1, hierarchy_level=0, uuid="SWING-2")  # Minor swing, should be filtered
        ]
        
        # 2. Selection Phase (Ensures Single Ownership - we just filter existing swings)
        selector = SwingLiquiditySelectionRule()
        selected = selector.select(swings)
        
        self.assertEqual(len(selected), 1)
        self.assertEqual(selected[0].identity['uuid'], "SWING-1")
        
        # 3. Construction Phase
        constructor = SwingLiquidityConstructionRule()
        objects = constructor.construct(selected, datetime.now())
        
        self.assertEqual(len(objects), 1)
        obj: SwingLiquidityObject = objects[0]
        
        # Verify strict structural encapsulation
        self.assertEqual(obj.state, LifecycleState.CANDIDATE)
        self.assertEqual(obj.evidence.source_swing_uuid, "SWING-1")
        self.assertEqual(obj.evidence.price, 105.0)
        
        # Verify lineage contains the explicit revision
        self.assertEqual(obj.lineage.source_revision, "1.0.0")

if __name__ == '__main__':
    unittest.main()
