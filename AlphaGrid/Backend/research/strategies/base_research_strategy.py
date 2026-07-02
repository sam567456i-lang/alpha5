"""Base Research Strategy Framework."""

import logging
from typing import Any, Dict, List, Type
from datetime import timedelta

from Backend.research.engine.strategy_interface import AbstractStrategy
from Backend.features.engine import FeatureEngine
from Backend.features.registry import FeatureRegistry
from Backend.features.base import AbstractFeature
from Backend.concepts.engine import ConceptEngine
from Backend.concepts.registry import ConceptRegistry
from Backend.concepts.generator import AbstractConceptGenerator
from Backend.signals.primitive.engine import PrimitiveSignalEngine
from Backend.signals.primitive.base import AbstractPrimitiveSignalGenerator
from Backend.signals.primitive.context import SignalContext
from Backend.methodology.engine import MethodologyEngine
from Backend.methodology.base import AbstractMethodology
from Backend.research.engine.signal_engine import SignalEngine
from Backend.research.decision.rule_provider import RuleDecisionProvider

logger = logging.getLogger(__name__)


class BaseResearchStrategy(AbstractStrategy):
    """
    Base class for research strategies.
    Orchestrates the entire Phase 9 pipeline: 
    Features -> Concepts -> Methodology -> SignalEngine -> DecisionProvider.
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

    def get_features(self) -> List[Type[AbstractFeature]]:
        """Returns the list of features to register."""
        return self.config.features if self.config else []

    def get_concept_generators(self) -> List[AbstractConceptGenerator]:
        """Returns the list of instantiated concept generators."""
        if not self.config:
            return []
        return self.config.concept_generators  # type: ignore

    def get_primitive_signal_generators(self) -> List[AbstractPrimitiveSignalGenerator]:
        """Returns the list of instantiated primitive signal generators."""
        if not self.config:
            return []
        return self.config.primitive_signal_generators  # type: ignore

    def get_methodologies(self) -> List[AbstractMethodology]:
        """Returns the list of instantiated methodologies."""
        if not self.config:
            return []
        return self.config.methodologies  # type: ignore

    def _setup_pipeline(self) -> None:
        """Sets up the deterministic pipeline for the strategy."""
        # 1. Feature Store
        f_reg = FeatureRegistry()
        for feature_cls in self.get_features():
            f_reg.register(feature_cls)
        self.feature_engine = FeatureEngine(f_reg)

        # 2. Concept Engine
        c_reg = ConceptRegistry()
        for generator in self.get_concept_generators():
            c_reg.register(generator)
        self.concept_engine = ConceptEngine(c_reg)

        # 3. Primitive Signal Engine
        self.primitive_signal_engine = PrimitiveSignalEngine(self.get_primitive_signal_generators())

        # 4. Methodology Engine
        self.methodology_engine = MethodologyEngine(self.get_methodologies())

        # 4. Signal Engine
        self.signal_engine = SignalEngine()

        # 5. Decision Provider
        self.decision_provider = RuleDecisionProvider()

    def __init__(self, parameters: Dict[str, Any], random_generator: Any, config: Any = None) -> None:
        super().__init__(parameters, random_generator)
        self.config = config
        self.confidence_threshold = self.parameters.get("confidence_threshold", 0.6)
        self.cooldown_bars = self.parameters.get("cooldown_bars", 5)
        
        self.state = {
            "position": 0,
            "cooldown_counter": 0,
            "bar_count": 0,
            "decisions_log": []
        }
        
        if self.config:
            self._setup_pipeline()

    def on_market_event(self, event: Dict[str, Any]) -> None:
        self.state["bar_count"] += 1  # type: ignore
        
        if self.state["cooldown_counter"] > 0:  # type: ignore
            self.state["cooldown_counter"] -= 1  # type: ignore

        class DictWrapper:
            def __init__(self, d): self.__dict__.update(d)  # type: ignore
        
        snapshot = DictWrapper(event) if isinstance(event, dict) else event  # type: ignore
        timestamp = event.get("timestamp") if isinstance(event, dict) else snapshot.timestamp

        # 1. Compute features
        try:
            features = self.feature_engine.process(snapshot)

            # Inject raw market data for concepts that need price comparison (e.g. TrendConceptGenerator fallback)
            features["open"] = float(snapshot.open)  # type: ignore
            features["high"] = float(snapshot.high)  # type: ignore
            features["low"] = float(snapshot.low)  # type: ignore
            features["close"] = float(snapshot.close)  # type: ignore
            features["volume"] = float(snapshot.volume)  # type: ignore
        except Exception as e:
            logger.warning("Feature extraction failed: %s", e)
            return

        # 2. Compute concepts
        try:
            concepts = self.concept_engine.process(timestamp, features)  # type: ignore
        except Exception as e:
            logger.warning("Concept generation failed: %s", e)
            return

        # 3. Compute primitive signals
        primitive_signals = self.primitive_signal_engine.process(timestamp, list(concepts.values()))  # type: ignore
        signal_context = SignalContext(primitive_signals)

        # 4. Methodologies -> Evaluations
        evaluations = self.methodology_engine.evaluate(signal_context)

        # 5. Evaluations -> Trading Signals
        signals = self.signal_engine.process(evaluations)

        # 6. Trading Signals -> Decision
        decision = self.decision_provider.evaluate(signals, context={"features": features})

        # 6. Output / State tracking
        if decision.direction != "WAIT" and decision.confidence >= self.confidence_threshold:
            if self.state["cooldown_counter"] == 0:
                logger.info(
                    "[%s] %s Actionable Decision: %s (conf=%.2f) - %s", 
                    timestamp, self.__class__.__name__, decision.direction, decision.confidence, decision.reason
                )
                self.state["decisions_log"].append((timestamp, decision))  # type: ignore
                self.state["cooldown_counter"] = self.cooldown_bars
