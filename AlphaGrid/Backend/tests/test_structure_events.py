import unittest
from datetime import datetime
from Backend.core.evidence_dtos.structure_events import BOSEvent, TransitionDirection, StructureTransitionEvent
from Backend.core.analytical_rules.structure_event_rules import StructureEventExtractionRule
from Backend.core.evidence_dtos.base import PlatformIdentity

class MockStructureObject:
    def __init__(self, uuid, upper, lower, rev):
        self.identity = PlatformIdentity(owner_family="Structure", uuid=uuid)
        self.upper_bound = upper
        self.lower_bound = lower
        self.operational_revision = rev

class TestStructureEvents(unittest.TestCase):
    
    def setUp(self):
        self.extractor = StructureEventExtractionRule()
        self.now = datetime.now()

    def test_bos_event_inheritance(self):
        """Verify BOSEvent inherits the universal Transition abstraction."""
        obj = MockStructureObject("struc_abc", 100.0, 50.0, 3)
        tick = {"price": 105.0, "timestamp": self.now} # Breaks upper bound
        
        events = self.extractor.extract_bos(tick, [obj])
        self.assertEqual(len(events), 1)
        
        evt = events[0]
        self.assertIsInstance(evt, BOSEvent)
        self.assertIsInstance(evt, StructureTransitionEvent) # Abstraction test
        
        # Verify Transition fields
        self.assertEqual(evt.previous_structure_uuid, "struc_abc")
        self.assertEqual(evt.transition_direction, TransitionDirection.ASCENDING)
        self.assertEqual(evt.triggering_price, 105.0)
        
        # Verify strict Lineage lock
        self.assertEqual(evt.source_object_revisions["struc_abc"], 3)
        self.assertIn("struc_abc", evt.lineage.source_dto_uuids)

if __name__ == '__main__':
    unittest.main()
