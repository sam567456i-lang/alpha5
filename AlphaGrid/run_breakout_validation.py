import json
import hashlib
import time
import psutil
import os
import numpy as np
import pandas as pd
from datetime import datetime

from Backend.features.volatility_breakout import VolatilityBreakoutFeatureGenerator
from Backend.concepts.core.breakout import BreakoutConceptGenerator
from Backend.methodologies.breakout import BreakoutMethodology
from Backend.signals.primitive.generators.breakout_signals import BreakoutPrimitiveSignalGenerator
from Backend.strategy.strategies.breakout_strategies import VolatilityBreakoutStrategy
from Shared.dtos.execution_context import ExecutionContext
from Backend.dtos.base import BaseObject

# --- MONKEY PATCH BASEOBJECT FOR LEGACY SCRIPTS ---
original_init = BaseObject.__init__
def patched_init(self, **kwargs):
    if 'execution_context' not in kwargs:
        kwargs['execution_context'] = ExecutionContext(
            session_id='legacy', trace_id=kwargs.get('trace_id', 'trace'),
            correlation_id=kwargs.get('correlation_id', 'cor'), instrument_id='TEST',
            environment='local', runtime_mode='test', exchange='TEST',
            provider='TEST', market='TEST', timezone='UTC', sequence_id=0,
            is_replay=True, build_version='1.0.0'
        )
    if 'owner' not in kwargs:
        kwargs['owner'] = 'Legacy'
    original_init(self, **kwargs)
BaseObject.__init__ = patched_init
# ---------------------------------------------------


def generate_market_data(rows: int) -> pd.DataFrame:
    np.random.seed(42)
    dates = pd.date_range(start='2020-01-01', periods=rows, freq='min')
    df = pd.DataFrame({
        'open': np.random.uniform(100, 110, rows),
        'high': np.random.uniform(110, 120, rows),
        'low': np.random.uniform(90, 100, rows),
        'close': np.random.uniform(95, 115, rows),
        'volume': np.random.uniform(1000, 5000, rows),
    }, index=dates)
    df.attrs['symbol'] = 'TEST/USD'
    df.attrs['timeframe'] = '1m'
    return df


def run_pipeline(data: pd.DataFrame, trace_id: str):
    # 1. Feature
    feature_gen = VolatilityBreakoutFeatureGenerator(atr_period=14, multiplier=1.5)
    feature_dto = feature_gen.generate(data, trace_id, "cor-1")
    
    # 2. Concept
    concept_gen = BreakoutConceptGenerator()
    concept_dto = concept_gen.generate([feature_dto], trace_id, "cor-1")
    
    # 3. Methodology
    meth_gen = BreakoutMethodology()
    meth_dto = meth_gen.evaluate(concept_dto, trace_id=trace_id, correlation_id="cor-1")
    
    # 4. Signal
    sig_gen = BreakoutPrimitiveSignalGenerator()
    sig_dto = sig_gen.generate(meth_dto, trace_id, "cor-1")
    
    # 5. Strategy
    strat_gen = VolatilityBreakoutStrategy(atr_period=14, multiplier=1.5)
    strat_dto = strat_gen.generate(sig_dto, trace_id, "cor-1")
    
    return {
        "FeatureDTO": feature_dto,
        "ConceptDTO": concept_dto,
        "MethodologyDTO": meth_dto,
        "SignalDTO": sig_dto,
        "StrategyDTO": strat_dto
    }


def main():
    print("=========================================")
    print("1. END-TO-END PIPELINE & DTO CAPTURE")
    print("=========================================")
    small_data = generate_market_data(100)
    dtos = run_pipeline(small_data, "trace-e2e-1")
    
    for name, dto in dtos.items():
        print(f"\n--- {name} ---")
        # Handle dict representation (assumes dataclass/pydantic or simple __dict__)
        try:
            dto_dict = dto.model_dump() # if pydantic
        except:
            dto_dict = dto.__dict__
        print(json.dumps(dto_dict, indent=2, default=str))
        
    print("\n=========================================")
    print("2. STRESS TEST, PERFORMANCE & MEMORY")
    print("=========================================")
    large_data = generate_market_data(100000)
    process = psutil.Process(os.getpid())
    mem_before = process.memory_info().rss
    
    start_time = time.time()
    cpu_start = time.process_time()
    
    _ = run_pipeline(large_data, "trace-stress-1")
    
    cpu_end = time.process_time()
    end_time = time.time()
    mem_after = process.memory_info().rss
    
    mem_before_mb = mem_before / (1024 * 1024)
    mem_after_mb = mem_after / (1024 * 1024)
    mem_diff_mb = mem_after_mb - mem_before_mb
    runtime = end_time - start_time
    cpu_time = cpu_end - cpu_start
    
    print(f"Dataset Size: 100,000 bars")
    print(f"Hardware CPU Count: {psutil.cpu_count()}")
    print(f"Elapsed Time: {runtime:.4f} seconds")
    print(f"CPU Time: {cpu_time:.4f} seconds")
    print(f"Peak RSS Before: {mem_before_mb:.2f} MB")
    print(f"Peak RSS After: {mem_after_mb:.2f} MB")
    print(f"Peak Memory Overhead: {mem_diff_mb:.2f} MB")
    
    print("\n=========================================")
    print("3. DETERMINISTIC REPLAY (SHA256)")
    print("=========================================")
    def strip_dynamic(dto_dict):
        d = dto_dict.copy()
        for key in ['id', 'trace_id', 'correlation_id', 'created_at', 'updated_at', 'checksum', 'lineage']:
            if key in d:
                del d[key]
        return d

    # Run 1
    dtos_run1 = run_pipeline(large_data, "trace-det-1")
    try:
        r1_dict = dtos_run1["StrategyDTO"].model_dump()
    except:
        r1_dict = dtos_run1["StrategyDTO"].__dict__
    
    payload1 = json.dumps(strip_dynamic(r1_dict), sort_keys=True, default=str)
    hash1 = hashlib.sha256(payload1.encode()).hexdigest()
    
    # Run 2
    dtos_run2 = run_pipeline(large_data, "trace-det-2")
    try:
        r2_dict = dtos_run2["StrategyDTO"].model_dump()
    except:
        r2_dict = dtos_run2["StrategyDTO"].__dict__
        
    payload2 = json.dumps(strip_dynamic(r2_dict), sort_keys=True, default=str)
    hash2 = hashlib.sha256(payload2.encode()).hexdigest()
    
    print(f"Run 1 SHA256: {hash1}")
    print(f"Run 2 SHA256: {hash2}")
    print(f"Match: {hash1 == hash2}")


if __name__ == "__main__":
    main()
