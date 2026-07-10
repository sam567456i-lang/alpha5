import unittest
from datetime import datetime
from Backend.core.evidence_dtos.base import PlatformIdentity, LineageRecord
from Backend.core.analytical_rules.amt_rules import AMTEngine
from Backend.core.evidence_dtos.market_profile import ValueArea, Excess

class TestAMTEngine(unittest.TestCase):
    def setUp(self):
        self.engine = AMTEngine()
        self.now = datetime.now()

    def test_rejection_logic(self):
        """Verifies Rejection fires when price tests VA and prints Excess tail."""
        mock_identity = PlatformIdentity(owner_family="Test")
        mock_lineage = LineageRecord(platform="Test", family="Test", capability="Test", source_dto_uuids=[], source_rule_ids=[], source_engine_id="Test", parent_object_uuids=[], source_revision="1", version="1", replay_id="", timestamp=self.now)
        
        # Prior Profile Value Area (VAH: 100, VAL: 80)
        prior_va = ValueArea(identity=mock_identity, lineage=mock_lineage, vah_price=100.0, val_price=80.0, poc_price=90.0)
        
        # Current Excess (Buying Tail pushing price UP from VAL)
        excess = Excess(identity=mock_identity, lineage=mock_lineage, is_buying_tail=True, tail_length=3.0)
        
        # Price tests the VAL (82.0)
        events = self.engine.evaluate_rejection(current_price=82.0, prior_va=prior_va, current_excess=excess, timestamp=self.now)
        
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0].rejected_price_level, 82.0)
        self.assertEqual(events[0].excess_tail_length, 3.0)

    def test_rejection_fails_without_excess(self):
        """Verifies Rejection correctly ignores VA tests that lack structural Excess."""
        mock_identity = PlatformIdentity(owner_family="Test")
        mock_lineage = LineageRecord(platform="Test", family="Test", capability="Test", source_dto_uuids=[], source_rule_ids=[], source_engine_id="Test", parent_object_uuids=[], source_revision="1", version="1", replay_id="", timestamp=self.now)
        prior_va = ValueArea(identity=mock_identity, lineage=mock_lineage, vah_price=100.0, val_price=80.0, poc_price=90.0)
        
        events = self.engine.evaluate_rejection(current_price=82.0, prior_va=prior_va, current_excess=None, timestamp=self.now)
        self.assertEqual(len(events), 0)

if __name__ == '__main__':
    unittest.main()
