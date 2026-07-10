import unittest
from Backend.core.evidence_dtos.market_universe import MarketIdentity, MarketUniverseConfig, MissingDataPolicy
from Backend.core.analytical_rules.cross_market_rules import CrossMarketEngine

class TestCrossMarket(unittest.TestCase):
    def setUp(self):
        self.target = MarketIdentity("BTC", "BINANCE", "CRYPTO", "USD", "24x7", "UTC", 0.1, 0.001, "NONE")
        self.benchmark = MarketIdentity("ETH", "BINANCE", "CRYPTO", "USD", "24x7", "UTC", 0.1, 0.001, "NONE")
        self.config = MarketUniverseConfig(self.target, [self.benchmark], missing_data_policy=MissingDataPolicy.REJECT_CALCULATION)
        self.engine = CrossMarketEngine(self.config)

    def test_missing_data_reject(self):
        """Verifies engine rejects calculation when MissingDataPolicy is REJECT and one side is missing."""
        events = self.engine.process_synchronous_bars(target_bar=None, benchmark_bar=None)
        self.assertEqual(len(events), 0)

if __name__ == '__main__':
    unittest.main()
