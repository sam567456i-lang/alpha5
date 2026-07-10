from dataclasses import dataclass

@dataclass
class PerformanceBenchmark:
    bars_per_second: float
    objects_generated_per_second: float
    peak_memory_mb: float
    replay_speed_multiplier: float

class PerformanceBenchmarker:
    """Tracks computational performance to prevent methodology bloat."""
    
    @staticmethod
    def assert_performance(benchmark: PerformanceBenchmark):
        if benchmark.bars_per_second < 50000:
            raise ValueError(f"Performance Regression: Engine is too slow ({benchmark.bars_per_second} bars/sec). Target: >50000.")
        if benchmark.peak_memory_mb > 4096:
            raise ValueError(f"Memory Leak Detected: Consumed {benchmark.peak_memory_mb} MB.")
