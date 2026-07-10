import unittest
from datetime import datetime
from Backend.core.evidence_dtos.structure import InternalStructureObject, ExternalStructureObject, StructuralState
from Backend.core.evidence_dtos.base import PlatformIdentity
from Backend.core.analytical_rules.structure_rules import StructureConstructionRule

class MockSwing:
    def __init__(self, uuid, price):
        self.identity = PlatformIdentity(owner_family="Swing", uuid=uuid)
        self.price = price

class TestStructureObjects(unittest.TestCase):
    
    def setUp(self):
        self.constructor = StructureConstructionRule()
        self.now = datetime.now()

    def test_hierarchy_boundary_enforcement(self):
        """Internal Structure MUST mathematically fit inside External Structure."""
        ext_obj = ExternalStructureObject(
            identity=PlatformIdentity(owner_family="Structure", uuid="ext_1"),
            lineage=None,
            upper_bound=100.0,
            lower_bound=50.0,
            structural_state=StructuralState.CONTINUOUS
        )
        
        # Valid Internal Object
        int_obj_valid = InternalStructureObject(
            identity=PlatformIdentity(owner_family="Structure", uuid="int_1"),
            lineage=None,
            upper_bound=90.0,
            lower_bound=60.0,
            structural_state=StructuralState.NESTED
        )
        
        # Invalid Internal Object (Exceeds upper bound)
        int_obj_invalid = InternalStructureObject(
            identity=PlatformIdentity(owner_family="Structure", uuid="int_2"),
            lineage=None,
            upper_bound=110.0,
            lower_bound=60.0,
            structural_state=StructuralState.NESTED
        )

        # Should pass
        hierarchy = self.constructor.build_hierarchy(int_obj_valid, ext_obj, self.now)
        self.assertEqual(hierarchy.parent_uuid, "ext_1")
        self.assertIn("int_1", hierarchy.child_uuids)
        self.assertEqual(hierarchy.structural_state, StructuralState.NESTED)

        # Should fail mathematically
        with self.assertRaises(ValueError) as context:
            self.constructor.build_hierarchy(int_obj_invalid, ext_obj, self.now)
        
        self.assertIn("exceed External bounds", str(context.exception))

    def test_structural_leg_deep_provenance(self):
        """Structural Leg must exactly reference source swings in its lineage."""
        swing_a = MockSwing("sw_1", 100.0)
        swing_b = MockSwing("sw_2", 150.0)
        
        leg = self.constructor.build_leg(swing_a, swing_b, self.now)
        
        # Verify objective state mapping
        self.assertEqual(leg.structural_state, StructuralState.ASCENDING)
        self.assertEqual(leg.price_delta, 50.0)
        
        # Verify deep provenance
        self.assertIn("sw_1", leg.lineage.source_dto_uuids)
        self.assertIn("sw_2", leg.lineage.source_dto_uuids)
        self.assertEqual(leg.start_swing_uuid, "sw_1")
        self.assertEqual(leg.end_swing_uuid, "sw_2")
        
if __name__ == '__main__':
    unittest.main()
