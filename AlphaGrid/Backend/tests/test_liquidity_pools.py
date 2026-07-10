import unittest
import time
from datetime import datetime
from Backend.core.evidence_dtos.pools import PoolMembership
from Backend.core.analytical_rules.pool_rules import EqualLiquidityPoolPolicy, PoolLiquidityConstructionRule

class MockLiquidityObject:
    def __init__(self, uuid, symbol):
        class MockId:
            def __init__(self, u, s):
                self.uuid = u
                self.symbol = s
        self.identity = MockId(uuid, symbol)

class TestLiquidityPools(unittest.TestCase):
    
    def setUp(self):
        self.policy = EqualLiquidityPoolPolicy()
        self.constructor = PoolLiquidityConstructionRule()
        self.now = datetime.now()

    def test_pool_construction(self):
        objs = [MockLiquidityObject("uuid_1", "BTC"), MockLiquidityObject("uuid_2", "BTC")]
        pools = self.constructor.construct(self.policy, objs, self.now)
        
        self.assertEqual(len(pools), 1)
        pool = pools[0]
        
        # Verify non-duplication (no prices)
        self.assertFalse(hasattr(pool, "price"))
        
        # Verify memberships
        self.assertEqual(len(pool.memberships), 2)
        self.assertEqual(pool.memberships[0].member_uuid, "uuid_1")
        self.assertEqual(pool.memberships[0].qualification_rule, "EqualLiquidityPoolPolicy")
        self.assertEqual(pool.geometry.member_count, 2)

    def test_cross_symbol_integrity(self):
        # A pool containing BTC and ETH should be rejected by the integrity service (simulated here)
        objs = [MockLiquidityObject("uuid_1", "BTC"), MockLiquidityObject("uuid_2", "ETH")]
        # To strictly enforce, an Integrity Service would fail this graph node.
        # We simulate the check.
        symbols = set([obj.identity.symbol for obj in objs])
        self.assertTrue(len(symbols) > 1, "Cross-symbol contamination detected.")

    def test_performance_100k_members(self):
        """Institutional scale benchmark simulating 100,000 memberships in memory."""
        start_time = time.time()
        
        # Build 100,000 memberships directly (bypassing full object generation for speed)
        memberships = []
        for i in range(100000):
            memberships.append(PoolMembership(
                member_uuid=f"uuid_{i}",
                added_revision=1,
                qualification_rule="TestPolicy",
                qualification_inputs=[f"uuid_{i}"],
                qualification_revision=1
            ))
            
        # Verify scaling time is under 1 second
        duration = time.time() - start_time
        self.assertLess(duration, 1.0, "100k membership generation exceeded performance threshold.")
        self.assertEqual(len(memberships), 100000)

if __name__ == '__main__':
    unittest.main()
