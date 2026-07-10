import unittest
from datetime import datetime, date, time
from Backend.core.evidence_dtos.session import SessionBoundaryType, SessionDefinition, TradingCalendar, TradingDay
from Backend.core.analytical_rules.session_rules import SessionLiquiditySelectionRule, SessionLiquidityConstructionRule

class TestSessionLiquidity(unittest.TestCase):
    
    def setUp(self):
        self.selector = SessionLiquiditySelectionRule()
        self.constructor = SessionLiquidityConstructionRule()

    def _build_mock_boundaries(self, overrides):
        base = {
            "session_id": "london",
            "boundary_type": "HIGH",
            "price": 1.2500,
            "origin_bar_timestamp": datetime(2026, 7, 9, 10, 0),
            "calendar_id": "forex",
            "window_start": datetime(2026, 7, 9, 8, 0),
            "window_end": datetime(2026, 7, 9, 17, 0)
        }
        base.update(overrides)
        return [base]

    def test_basic_construction(self):
        boundaries = self._build_mock_boundaries({})
        selected = self.selector.select(boundaries)
        objects = self.constructor.construct(selected, datetime.now())
        
        self.assertEqual(len(objects), 1)
        obj = objects[0]
        self.assertEqual(obj.evidence.session_id, "london")
        self.assertEqual(obj.identity.calendar, "forex")
        self.assertEqual(obj.identity.session, "london")
        self.assertEqual(obj.identity.boundary, "HIGH")

    def test_midnight_crossing_session(self):
        # e.g., Asia session crossing midnight
        boundaries = self._build_mock_boundaries({
            "session_id": "asia",
            "window_start": datetime(2026, 7, 9, 23, 0),
            "window_end": datetime(2026, 7, 10, 8, 0)
        })
        selected = self.selector.select(boundaries)
        objects = self.constructor.construct(selected, datetime.now())
        self.assertEqual(len(objects), 1)
        self.assertEqual(objects[0].evidence.window_end.day, 10)

    def test_dst_transition(self):
        # DST transition window (shortened/lengthened)
        boundaries = self._build_mock_boundaries({
            "session_id": "new_york",
            "window_start": datetime(2026, 3, 8, 9, 30),
            "window_end": datetime(2026, 3, 8, 16, 0)
        })
        objects = self.constructor.construct(self.selector.select(boundaries), datetime.now())
        self.assertEqual(len(objects), 1)

    def test_half_day_holiday(self):
        # e.g., Thanksgiving half day
        boundaries = self._build_mock_boundaries({
            "session_id": "nyse",
            "window_start": datetime(2026, 11, 27, 9, 30),
            "window_end": datetime(2026, 11, 27, 13, 0) # Early close
        })
        objects = self.constructor.construct(self.selector.select(boundaries), datetime.now())
        self.assertEqual(objects[0].evidence.window_end.hour, 13)

    def test_crypto_continuous(self):
        # 24/7 crypto
        boundaries = self._build_mock_boundaries({
            "session_id": "crypto_daily",
            "calendar_id": "crypto",
            "window_start": datetime(2026, 7, 9, 0, 0),
            "window_end": datetime(2026, 7, 9, 23, 59, 59)
        })
        objects = self.constructor.construct(self.selector.select(boundaries), datetime.now())
        self.assertEqual(objects[0].identity.calendar, "crypto")

    def test_invalid_upstream_filtering(self):
        # Missing price
        boundaries = [{"session_id": "london", "boundary_type": "HIGH"}]
        selected = self.selector.select(boundaries)
        self.assertEqual(len(selected), 0)

if __name__ == '__main__':
    unittest.main()
