import unittest
from datetime import datetime
from Backend.core.evidence_dtos.liquidity_events import TouchEvent, SweepEvent
from Backend.core.analytical_rules.liquidity_event_rules import LiquidityEventExtractionRule

class MockLiquidityObject:
    def __init__(self, uuid, price, rev):
        class MockId:
            def __init__(self, u):
                self.uuid = u
        self.identity = MockId(uuid)
        self.upper_bound = price
        self.operational_revision = rev

class TestLiquidityEvents(unittest.TestCase):
    
    def setUp(self):
        self.extractor = LiquidityEventExtractionRule()
        self.now = datetime.now()

    def test_touch_event_extraction(self):
        obj = MockLiquidityObject("pool_123", 100.0, 5)
        tick = {"price": 100.0005, "timestamp": self.now} # Within 0.001 tolerance
        
        events = self.extractor.extract(tick, [obj])
        self.assertEqual(len(events), 1)
        
        evt = events[0]
        self.assertIsInstance(evt, TouchEvent)
        self.assertEqual(evt.trigger_object_uuids[0], "pool_123")
        
        # Verify it locked the revision
        self.assertEqual(evt.source_object_revisions["pool_123"], 5)
        
        # Verify relationship creation
        self.assertEqual(evt.relationships[0].target_uuid, "pool_123")
        self.assertEqual(evt.relationships[0].relationship_type.value, "references")

    def test_sweep_event_extraction(self):
        obj = MockLiquidityObject("ref_abc", 50.0, 2)
        tick = {"price": 50.02, "timestamp": self.now} # Pierces slightly
        
        events = self.extractor.extract(tick, [obj])
        self.assertEqual(len(events), 1)
        
        evt = events[0]
        self.assertIsInstance(evt, SweepEvent)
        self.assertEqual(evt.source_object_revisions["ref_abc"], 2)

if __name__ == '__main__':
    unittest.main()
