import unittest
from datetime import datetime
from Backend.core.evidence_dtos.range import RangeRelationshipType
from Backend.core.analytical_rules.range_rules import (
    RangeLiquiditySelectionRule,
    RangeLiquidityValidationRule,
    RangeLiquidityConstructionRule
)

class TestRangeLiquidity(unittest.TestCase):
    
    def setUp(self):
        self.selector = RangeLiquiditySelectionRule()
        self.validator = RangeLiquidityValidationRule()
        self.constructor = RangeLiquidityConstructionRule()
        self.now = datetime.now()

    def test_zero_width_range(self):
        # Upper and lower are identical
        ranges = [{
            "id": "zero",
            "upper_bound": 100.0,
            "lower_bound": 100.0,
            "start_time": self.now
        }]
        selected = self.selector.select(ranges)
        validated = self.validator.validate(selected)
        self.assertEqual(len(validated), 1)
        
        objects, rels = self.constructor.construct(validated, self.now)
        # 1 Internal + 1 Reference + 3 Ratios + 2 Segments = 7 objects
        self.assertEqual(len(objects), 7)
        # Width should be 0
        internal_range = objects[0]
        self.assertEqual(internal_range.width, 0.0)

    def test_inverted_bounds(self):
        # Upper is less than lower (should be filtered out by selection)
        ranges = [{
            "id": "inv",
            "upper_bound": 90.0,
            "lower_bound": 100.0,
            "start_time": self.now
        }]
        selected = self.selector.select(ranges)
        self.assertEqual(len(selected), 0)

    def test_overlap_relationship(self):
        ranges = [
            {
                "id": "r1",
                "upper_bound": 100.0,
                "lower_bound": 50.0,
                "start_time": self.now
            },
            {
                "id": "r2",
                "upper_bound": 75.0,
                "lower_bound": 25.0,
                "start_time": self.now
            }
        ]
        selected = self.selector.select(ranges)
        validated = self.validator.validate(selected)
        objects, rels = self.constructor.construct(validated, self.now)
        
        self.assertEqual(len(rels), 1)
        self.assertEqual(rels[0].relationship_type, RangeRelationshipType.OVERLAPS)
        self.assertEqual(rels[0].source_uuid, "int_r1")
        self.assertEqual(rels[0].target_uuid, "int_r2")

    def test_negative_prices(self):
        # Synthetic extreme test for futures/spreads
        ranges = [{
            "id": "neg",
            "upper_bound": -10.0,
            "lower_bound": -50.0,
            "start_time": self.now
        }]
        selected = self.selector.select(ranges)
        validated = self.validator.validate(selected)
        self.assertEqual(len(validated), 1)
        objects, rels = self.constructor.construct(validated, self.now)
        internal = objects[0]
        self.assertEqual(internal.width, 40.0)
        self.assertEqual(internal.midpoint, -30.0)

    def test_massive_floating_point(self):
        # BTC or Zimbabwean dollar type sizes
        ranges = [{
            "id": "huge",
            "upper_bound": 1000000000.12345,
            "lower_bound": 500000000.12345,
            "start_time": self.now
        }]
        selected = self.selector.select(ranges)
        validated = self.validator.validate(selected)
        objects, rels = self.constructor.construct(validated, self.now)
        internal = objects[0]
        self.assertAlmostEqual(internal.width, 500000000.0, places=4)
        
if __name__ == '__main__':
    unittest.main()
