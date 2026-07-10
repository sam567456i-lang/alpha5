import unittest
from datetime import datetime
from Backend.core.evidence_dtos.base import PlatformIdentity, LineageRecord
from Backend.core.interfaces.feature_registry import FeatureRegistry, FeatureMetadata, FeatureGroup, NormalizationType, FeatureValidationConstraints
from Backend.core.analytical_rules.feature_rules import NormalizationEngine
from Backend.core.evidence_dtos.features import RawFeature

class TestFeatureEngineering(unittest.TestCase):
    def setUp(self):
        self.registry = FeatureRegistry()
        meta = FeatureMetadata(
            feature_id="trend.strength",
            version="v1",
            group=FeatureGroup.TREND,
            data_type="float",
            normalization=NormalizationType.MIN_MAX,
            update_frequency="per_bar",
            dependencies=["Trend"],
            validation_constraints=FeatureValidationConstraints(allowed_range=(0.0, 100.0), expected_units="ADX", null_handling="zero", required_capabilities=[]),
            consumer_platforms=["Platform11"]
        )
        self.registry.register(meta)
        self.engine = NormalizationEngine(self.registry)

    def test_normalization(self):
        """Verifies MIN_MAX normalization appropriately maps a raw ADX of 50 to 0.5."""
        mock_id = PlatformIdentity(owner_family="Test")
        mock_lin = LineageRecord("P", "F", "C", [], [], "E", [], "1", "1", "", datetime.now())
        raw = RawFeature(identity=mock_id, lineage=mock_lin, feature_id="trend.strength", feature_version="v1", raw_value=50.0)
        vec = self.engine.normalize(raw)
        
        self.assertEqual(vec.normalized_value, 0.5)

    def test_unregistered_rejection(self):
        """Verifies the engine safely rejects features completely absent from the Registry API."""
        mock_id = PlatformIdentity(owner_family="Test")
        mock_lin = LineageRecord("P", "F", "C", [], [], "E", [], "1", "1", "", datetime.now())
        raw = RawFeature(identity=mock_id, lineage=mock_lin, feature_id="ghost.feature", feature_version="v1", raw_value=50.0)
        
        with self.assertRaises(KeyError):
            self.engine.normalize(raw)

if __name__ == '__main__':
    unittest.main()
