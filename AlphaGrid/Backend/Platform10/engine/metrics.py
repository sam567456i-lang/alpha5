import threading
from Backend.Platform10.contracts.dtos import PlatformMetricsDTO

class PlatformMetrics:
    """Singleton tracker for Platform 10 Observability"""
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(PlatformMetrics, cls).__new__(cls)
                cls._instance.reset()
            return cls._instance
            
    def reset(self):
        self.total_executed = 0
        self.total_time_ms = 0.0
        self.success_count = 0
        self.failure_count = 0
        self.skipped_count = 0
        self.dependency_failures = 0
        self.cache_hits = 0
        self.cumulative_confidence = 0.0
        
    def record_success(self, duration_ms: float, confidence: float):
        with self._lock:
            self.total_executed += 1
            self.total_time_ms += duration_ms
            self.success_count += 1
            self.cumulative_confidence += confidence
            
    def record_failure(self, is_dependency: bool = False):
        with self._lock:
            self.failure_count += 1
            if is_dependency:
                self.dependency_failures += 1
                
    def record_skip(self):
        with self._lock:
            self.skipped_count += 1
            
    def record_cache_hit(self):
        with self._lock:
            self.cache_hits += 1
            
    def get_metrics(self) -> PlatformMetricsDTO:
        with self._lock:
            total_attempts = self.success_count + self.failure_count
            success_rate = (self.success_count / total_attempts) if total_attempts > 0 else 0.0
            failure_rate = (self.failure_count / total_attempts) if total_attempts > 0 else 0.0
            avg_conf = (self.cumulative_confidence / self.success_count) if self.success_count > 0 else 0.0
            avg_time = (self.total_time_ms / self.total_executed) if self.total_executed > 0 else 0.0
            
            return PlatformMetricsDTO(
                methodologies_executed=self.total_executed,
                total_execution_time_ms=self.total_time_ms,
                success_rate=success_rate,
                failure_rate=failure_rate,
                skipped=self.skipped_count,
                dependency_failures=self.dependency_failures,
                cache_hits=self.cache_hits,
                average_confidence=avg_conf,
                average_runtime_ms=avg_time
            )
