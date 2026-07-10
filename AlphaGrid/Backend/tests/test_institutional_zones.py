import unittest
from datetime import datetime
from Backend.core.evidence_dtos.institutional_zones import BullishOrderBlock, BearishOrderBlock, BaseInstitutionalZone
from Backend.core.evidence_dtos.structure_events import BOSEvent, TransitionDirection
from Backend.core.evidence_dtos.structure import StructuralBoundaryObject, StructuralState
from Backend.core.evidence_dtos.base import PlatformIdentity
from Backend.core.analytical_rules.institutional_zone_rules import InstitutionalZoneConstructionRule

class MockLiquidityObject:
    def __init__(self, uuid):
        self.identity = PlatformIdentity(owner_family="LiquidityPools", uuid=uuid)

class TestInstitutionalZones(unittest.TestCase):
    
    def setUp(self):
        self.constructor = InstitutionalZoneConstructionRule()
        self.now = datetime.now()
        
        self.mock_bos = BOSEvent(
            event_id="evt_bos_1",
            event_type="BOS",
            trigger_time=self.now,
            trigger_evidence={},
            trigger_object_uuids=["struc_1"],
            source_object_revisions={"struc_1": 1},
            triggering_bar_timestamp=self.now,
            confidence=1.0,
            transition_direction=TransitionDirection.ASCENDING
        )
        
        self.mock_struc = StructuralBoundaryObject(
            identity=PlatformIdentity(owner_family="Structure", uuid="struc_1"),
            lineage=None,
            upper_bound=100.0,
            lower_bound=90.0,
            structural_state=StructuralState.CONTINUOUS
        )
        
        self.mock_liq = MockLiquidityObject("liq_1")

    def test_zone_provenance_enforcement(self):
        """Zone creation MUST fail without valid event, structure, and liquidity pointers."""
        # Missing BOS Event
        with self.assertRaises(ValueError):
            self.constructor.build_order_block(None, self.mock_struc, self.mock_liq, self.now)
            
        # Wrong Event Type (e.g. passing a string instead of BOSEvent)
        with self.assertRaises(ValueError):
            self.constructor.build_order_block("fake_event", self.mock_struc, self.mock_liq, self.now)

        # Missing Structure Boundary
        with self.assertRaises(ValueError):
            self.constructor.build_order_block(self.mock_bos, None, self.mock_liq, self.now)

        # Missing Liquidity Object
        with self.assertRaises(ValueError):
            self.constructor.build_order_block(self.mock_bos, self.mock_struc, None, self.now)

    def test_zone_successful_construction(self):
        """Verify successful instantiation and correct subclassing based on Event direction."""
        ob = self.constructor.build_order_block(self.mock_bos, self.mock_struc, self.mock_liq, self.now)
        
        self.assertIsInstance(ob, BullishOrderBlock)
        self.assertIsInstance(ob, BaseInstitutionalZone)
        
        # Verify lineage
        self.assertIn("evt_bos_1", ob.lineage.source_dto_uuids)
        self.assertIn("struc_1", ob.lineage.source_dto_uuids)
        self.assertIn("liq_1", ob.lineage.source_dto_uuids)
        
        # Verify specific zone attributes
        self.assertEqual(ob.origin_event_uuids, ["evt_bos_1"])
        self.assertEqual(ob.origin_structure_uuids, ["struc_1"])
        self.assertEqual(ob.origin_liquidity_uuids, ["liq_1"])

if __name__ == '__main__':
    unittest.main()
