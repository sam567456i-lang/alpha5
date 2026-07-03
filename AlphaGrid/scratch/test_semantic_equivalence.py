import pickle
import time
from Backend.price_geometry.structure_engine import StructureEngine

class MockContext:
    def __init__(self, swings, dataset_id, timeframe, symbol):
        self.swings = swings
        self.dataset_id = dataset_id
        self.timeframe = timeframe
        self.symbol = symbol

def test_semantic_equivalence():
    with open('scratch/semantic_reference.pkl', 'rb') as f:
        ref = pickle.load(f)
        
    data = ref["data"]
    swings = ref["swings"]
    old_structures = ref["structures"]
    
    context = MockContext(swings, "stress_test_data", "1m", "BTCUSDT")
    struct_engine = StructureEngine()
    
    start = time.perf_counter()
    new_structures = struct_engine.process(data, context)
    end = time.perf_counter()
    
    assert len(new_structures) == len(old_structures), f"Lengths differ: {len(new_structures)} != {len(old_structures)}"
    
    for old_s, new_s in zip(old_structures, new_structures):
        if type(old_s).__name__ == "Structure":
            assert old_s.id.split('-')[:-1] == new_s.id.split('-')[:-1]
            assert getattr(old_s, 'is_bullish') == getattr(new_s, 'is_bullish')
        else:
            assert old_s.id == new_s.id
        assert old_s.timestamp == new_s.timestamp
        assert old_s.price == new_s.price
        assert getattr(old_s, 'structure_type', '') == getattr(new_s, 'structure_type', '')
        assert old_s.lifecycle_state == new_s.lifecycle_state
        
    print(f"Semantic Equivalence Verified! Processed {len(data)} bars in {end-start:.3f}s")
    
if __name__ == "__main__":
    test_semantic_equivalence()
