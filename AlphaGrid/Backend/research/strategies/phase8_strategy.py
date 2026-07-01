"""Phase 8 Reference Strategy Implementations."""

import logging
from typing import Any, Dict, List
from datetime import timedelta

from Backend.research.engine.strategy_interface import AbstractStrategy, STRATEGY_REGISTRY
from Backend.features.engine import FeatureEngine
from Backend.features.registry import FeatureRegistry
from Backend.features.trend import SMAFeature, EMAFeature
from Backend.features.momentum import ROCFeature, RSIFeature
from Backend.features.volatility import ATRFeature, RelativeVolumeFeature
from Backend.concepts.engine import ConceptEngine
from Backend.concepts.registry import ConceptRegistry
from Backend.concepts.generators.momentum import MomentumConceptGenerator
from Backend.concepts.generators.trend import TrendConceptGenerator
from Backend.concepts.generators.volatility import VolatilityConceptGenerator
from Backend.methodology.engine import MethodologyEngine
from Backend.methodology.trend_following import TrendFollowingMethodology
from Backend.methodology.mean_reversion import MeanReversionMethodology
from Backend.research.decision.base import AbstractDecisionProvider
from Backend.research.decision.rule_provider import RuleDecisionProvider


logger = logging.getLogger(__name__)


class BasePhase8Strategy(AbstractStrategy):
    """
    Base class for Phase 8 strategies orchestrating the pipeline.
    """

    @classmethod
    def get_parameter_schema(cls) -> Dict[str, Dict[str, Any]]:
        return {
            "confidence_threshold": {"type": float, "required": False, "default": 0.6, "min": 0.0, "max": 1.0},
            "cooldown_bars": {"type": int, "required": False, "default": 5, "min": 0},
        }

    @classmethod
    def max_label_horizon(cls) -> timedelta:
        return timedelta(0)

    def _setup_pipeline(self, methodology_cls: Any) -> None:
        """Sets up the deterministic pipeline for the strategy."""
        # 1. Feature Store
        f_reg = FeatureRegistry()
        f_reg.register(SMAFeature)
        f_reg.register(EMAFeature)
        f_reg.register(ROCFeature)
        f_reg.register(RSIFeature)
        f_reg.register(ATRFeature)
        f_reg.register(RelativeVolumeFeature)
        self.feature_engine = FeatureEngine(f_reg)

        # 2. Concept Engine
        c_reg = ConceptRegistry()
        c_reg.register(MomentumConceptGenerator)
        c_reg.register(TrendConceptGenerator)
        c_reg.register(VolatilityConceptGenerator)
        self.concept_engine = ConceptEngine(c_reg)

        # 3. Methodology Engine
        self.methodology_engine = MethodologyEngine([methodology_cls()])

        # 4. Decision Provider
        self.decision_provider = RuleDecisionProvider()

    def __init__(self, parameters: Dict[str, Any], random_generator: Any) -> None:
        super().__init__(parameters, random_generator)
        self.confidence_threshold = self.parameters.get("confidence_threshold", 0.6)
        self.cooldown_bars = self.parameters.get("cooldown_bars", 5)
        
        self.state = {
            "position": 0,
            "cooldown_counter": 0,
            "bar_count": 0,
            "decisions_log": []
        }

    def on_market_event(self, event: Dict[str, Any]) -> None:
        self.state["bar_count"] += 1
        
        # Cooldown management
        if self.state["cooldown_counter"] > 0:
            self.state["cooldown_counter"] -= 1

        # Event dict must contain raw market data for Feature Store
        # (assuming BacktestEngine wraps dict in a MarketSnapshot or FeatureEngine handles dicts)
        # Actually, our FeatureEngine expects MarketSnapshot. Let's build a dummy snapshot if needed,
        # but the BacktestEngine contract states it sends Dict. The Feature implementation uses
        # snapshot.close (attribute access). Let's wrap dict if necessary.
        
        # Quick wrapper for the dict to support attribute access required by Features
        class DictWrapper:
            def __init__(self, d): self.__dict__.update(d)
        
        snapshot = DictWrapper(event) if isinstance(event, dict) else event

        # 1. Compute features
        try:
            features = self.feature_engine.process(snapshot)  # type: ignore
        except Exception as e:
            logger.warning("Feature extraction failed: %s", e)
            return

        # 2. Compute concepts
        timestamp = event.get("timestamp") if isinstance(event, dict) else snapshot.timestamp
        try:
            concepts = self.concept_engine.process(timestamp, features)
        except Exception as e:
            logger.warning("Concept generation failed: %s", e)
            return

        # 3. Methodologies -> Signals
        signals = self.methodology_engine.evaluate(concepts)

        # 4. Decision Provider -> Decision
        decision = self.decision_provider.evaluate(signals, context={"features": features})

        # 5. Output / State tracking
        if decision.direction != "WAIT" and decision.confidence >= self.confidence_threshold:
            if self.state["cooldown_counter"] == 0:
                logger.info(
                    "[%s] %s Actionable Decision: %s (conf=%.2f) - %s", 
                    timestamp, self.__class__.__name__, decision.direction, decision.confidence, decision.reason
                )
                self.state["decisions_log"].append((timestamp, decision))
                self.state["cooldown_counter"] = self.cooldown_bars


class TrendFollowingRuleStrategy(BasePhase8Strategy):
    """Production Trend Following strategy."""
    
    def __init__(self, parameters: Dict[str, Any], random_generator: Any) -> None:
        super().__init__(parameters, random_generator)
        self._setup_pipeline(TrendFollowingMethodology)


class MeanReversionRuleStrategy(BasePhase8Strategy):
    """Production Mean Reversion strategy."""
    
    def __init__(self, parameters: Dict[str, Any], random_generator: Any) -> None:
        super().__init__(parameters, random_generator)
        self._setup_pipeline(MeanReversionMethodology)


def register_phase8_strategies() -> None:
    """Registers the Phase 8 strategies with the StrategyRegistry."""
    STRATEGY_REGISTRY.register("TREND_FOLLOWING_RULE", TrendFollowingRuleStrategy)
    STRATEGY_REGISTRY.register("MEAN_REVERSION_RULE", MeanReversionRuleStrategy)
