import unittest
from datetime import datetime
from Backend.core.evidence_dtos.imbalance import FVG, ImbalanceDirection, ImbalanceLifecycleState
from Backend.core.evidence_dtos.imbalance_events import PartialFillEvent, FullFillEvent
from Backend.core.analytical_rules.imbalance_event_rules import ImbalanceEventEngine
from Backend.core.analytical_rules.imbalance_lifecycle_rules import ImbalanceLifecycleEngine

class TestImbalanceEventSourcing(unittest.TestCase):
    
    def setUp(self):
        self.event_engine = ImbalanceEventEngine()
        self.lifecycle_engine = ImbalanceLifecycleEngine()
        self.now = datetime.now()

        # 10 point high FVG
        from Backend.core.evidence_dtos.base import PlatformIdentity, LineageRecord
        self.fvg = FVG(
            identity=PlatformIdentity(owner_family="ImbalanceObjects", uuid="fvg_1"),
            lineage=LineageRecord(platform="Platform10", family="ImbalanceObjects", capability="Tests", source_dto_uuids=[], source_rule_ids=[], source_engine_id="", parent_object_uuids=[], source_revision="1.0", version="1.0", replay_id="", timestamp=self.now),
            imbalance_uuid="fvg_1",
            upper_bound=110.0,
            lower_bound=100.0,
            height=10.0,
            direction=ImbalanceDirection.BULLISH,
            lifecycle_state=ImbalanceLifecycleState.ACTIVE
        )

    def test_partial_fill_cqrs_pipeline(self):
        """Test the pure Event Sourcing separation: Event Engine -> Lifecycle Engine."""
        
        # Tick drops into the FVG by 4.2 points (110 - 4.2 = 105.8)
        tick = {"price": 105.8, "timestamp": self.now}
        
        # 1. Event Engine answers "What happened?"
        events = self.event_engine.scan_penetration(tick, self.fvg)
        self.assertEqual(len(events), 1)
        
        event = events[0]
        self.assertIsInstance(event, PartialFillEvent)
        self.assertAlmostEqual(event.penetration_depth_observed, 4.2, places=2)
        self.assertAlmostEqual(event.fill_percent_observed, 42.0, places=2)
        
        # PROVE Event Engine did NOT mutate the FVG
        self.assertEqual(self.fvg.fill_geometry.fill_percent, 0.0)
        self.assertEqual(self.fvg.lifecycle_state, ImbalanceLifecycleState.ACTIVE)
        
        # 2. Lifecycle Engine answers "How does the object change?"
        updated_fvg = self.lifecycle_engine.process_event(event, self.fvg)
        
        self.assertAlmostEqual(updated_fvg.fill_geometry.fill_percent, 42.0, places=2)
        self.assertAlmostEqual(updated_fvg.fill_geometry.filled_height, 4.2, places=2)
        self.assertAlmostEqual(updated_fvg.fill_geometry.remaining_height, 5.8, places=2)
        self.assertEqual(updated_fvg.lifecycle_state, ImbalanceLifecycleState.ACTIVE)
        self.assertEqual(updated_fvg.fill_geometry.first_touch, self.now)

    def test_full_fill_cqrs_pipeline(self):
        """Verify tick blasting entirely through the FVG generates full fill logic."""
        
        tick = {"price": 95.0, "timestamp": self.now} # Way below the 100.0 lower bound
        
        events = self.event_engine.scan_penetration(tick, self.fvg)
        self.assertEqual(len(events), 1)
        
        event = events[0]
        self.assertIsInstance(event, FullFillEvent)
        
        updated_fvg = self.lifecycle_engine.process_event(event, self.fvg)
        
        self.assertEqual(updated_fvg.fill_geometry.fill_percent, 100.0)
        self.assertEqual(updated_fvg.fill_geometry.filled_height, 10.0)
        self.assertEqual(updated_fvg.fill_geometry.remaining_height, 0.0)
        self.assertEqual(updated_fvg.lifecycle_state, ImbalanceLifecycleState.FILLED)

if __name__ == '__main__':
    unittest.main()
