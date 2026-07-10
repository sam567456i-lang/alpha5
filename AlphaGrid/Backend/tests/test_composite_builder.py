import unittest
from Backend.core.interfaces.profile_framework import ProfileIdentity, ProfileSnapshot
from Backend.core.analytical_rules.composite_builder import CompositeProfileBuilder

class TestCompositeProfileBuilder(unittest.TestCase):
    def setUp(self):
        self.builder = CompositeProfileBuilder()
        self.ident1 = ProfileIdentity("p1", "BTC", "1m", "SESSION", "24x7", "FIXED_1.0")
        self.ident2 = ProfileIdentity("p2", "BTC", "1m", "SESSION", "24x7", "FIXED_1.0")
        self.composite_ident = ProfileIdentity("comp1", "BTC", "1m", "WEEKLY", "24x7", "FIXED_1.0")

    def test_composite_merge(self):
        """Verifies daily snapshots perfectly aggregate into composite snapshots."""
        snap1 = ProfileSnapshot(
            identity=self.ident1,
            histogram={100.0: 5, 101.0: 2},
            poc_price=100.0, vah_price=105.0, val_price=95.0
        )
        snap2 = ProfileSnapshot(
            identity=self.ident2,
            histogram={101.0: 10, 102.0: 1},
            poc_price=101.0, vah_price=106.0, val_price=96.0
        )
        
        comp_snap = self.builder.merge_snapshots([snap1, snap2], self.composite_ident)
        
        # 101.0 had 2 in snap1, 10 in snap2 -> 12 total.
        # 100.0 had 5 total.
        self.assertEqual(comp_snap.histogram[101.0], 12)
        self.assertEqual(comp_snap.histogram[100.0], 5)
        
        # POC should shift to 101.0 because 12 > 5
        self.assertEqual(comp_snap.poc_price, 101.0)
        self.assertEqual(comp_snap.identity.window, "WEEKLY")

if __name__ == '__main__':
    unittest.main()
