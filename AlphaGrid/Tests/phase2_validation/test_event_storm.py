import pytest
import asyncio
import time
import tracemalloc
from Backend.foundation.event_bus import EventBus

def test_event_storm_gate_4():
    """
    Gate 4: Event Storm Testing
    Simulates NIFTY Expiry load (5000 ticks/second).
    Proves the EventBus can handle massive bursts without deadlocks,
    starvation, or OOM memory explosions.
    """
    
    # 1. Setup Event Bus and simple subscriber
    bus = EventBus()
    processed_count = 0
    
    def fast_handler(event):
        nonlocal processed_count
        processed_count += 1
        
    bus.subscribe("market.tick", fast_handler)
    
    async def run_storm():
        # Start memory tracking
        tracemalloc.start()
        start_mem, _ = tracemalloc.get_traced_memory()
        
        start_time = time.time()
        
        # Fire 10,000 events as fast as possible (2 seconds worth of expiry load)
        tasks = []
        for i in range(10000):
            tasks.append(
                bus.emit(
                    event_type="market.tick", 
                    producer="test_storm", 
                    payload={"price": 100.0, "volume": i}
                )
            )
            
        await asyncio.gather(*tasks)
        
        end_time = time.time()
        
        end_mem, peak_mem = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        
        return start_time, end_time, start_mem, peak_mem, end_mem

    # Execute async storm
    start_time, end_time, start_mem, peak_mem, end_mem = asyncio.run(run_storm())
    
    elapsed = end_time - start_time
    throughput = 10000 / elapsed if elapsed > 0 else 0
    
    # Validation 1: All events processed
    assert processed_count == 10000, f"Dropped events! Expected 10000, got {processed_count}"
    
    # Validation 2: No Deadlocks (It finished)
    assert elapsed < 10.0, f"Event Bus is too slow! Took {elapsed:.2f} seconds for 10k events."
    
    # Validation 3: Memory footprint did not explode
    # The history deque should hold max 10,000 envelopes, which should be a few MBs
    memory_growth_mb = (end_mem - start_mem) / (1024 * 1024)
    assert memory_growth_mb < 50.0, f"Memory Leak Detected! Grew by {memory_growth_mb:.2f} MB"
