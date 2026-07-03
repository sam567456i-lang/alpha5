"""Unit tests for CompositeMethodology."""

import pytest
from datetime import datetime, timezone
from Backend.methodology.composite import CompositeMethodology
from Backend.methodology.voting import UnanimousVoting, MajorityVoting, AnyVoting
from Backend.methodology.base import AbstractMethodology
from Backend.methodology.evaluation import MethodologyEvaluation
from Backend.signals.primitive.context import SignalContext

class MockMethodology(AbstractMethodology):
    def __init__(self, return_val=None):
        self.return_val = return_val
        
    @classmethod
    def get_name(cls) -> str:
        return "Mock"

    def evaluate(self, context):
        return self.return_val

def test_unanimous_voting():
    m1 = MockMethodology(MethodologyEvaluation("m1", datetime.now(timezone.utc), True, 1, 0.8))
    m2 = MockMethodology(MethodologyEvaluation("m2", datetime.now(timezone.utc), True, 1, 0.9))
    
    comp = CompositeMethodology([m1, m2], UnanimousVoting())
    ctx = SignalContext(tuple())
    res = comp.evaluate(ctx)
    
    assert res is not None
    assert res.direction == 1
    assert res.confidence == pytest.approx(0.85)

def test_majority_voting():
    m1 = MockMethodology(MethodologyEvaluation("m1", datetime.now(timezone.utc), True, 1, 0.8))
    m2 = MockMethodology(MethodologyEvaluation("m2", datetime.now(timezone.utc), True, 1, 0.9))
    m3 = MockMethodology(MethodologyEvaluation("m3", datetime.now(timezone.utc), True, -1, 0.5))
    
    comp = CompositeMethodology([m1, m2, m3], MajorityVoting())
    ctx = SignalContext(tuple())
    res = comp.evaluate(ctx)
    
    assert res is not None
    assert res.direction == 1

def test_any_voting_conflict():
    m1 = MockMethodology(MethodologyEvaluation("m1", datetime.now(timezone.utc), True, 1, 0.8))
    m2 = MockMethodology(MethodologyEvaluation("m2", datetime.now(timezone.utc), True, -1, 0.9))
    
    comp = CompositeMethodology([m1, m2], AnyVoting())
    ctx = SignalContext(tuple())
    res = comp.evaluate(ctx)
    
    assert res is not None
    assert res.direction == 0
