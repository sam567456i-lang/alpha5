"""Market Replay Engine."""

import logging
import threading
import time
from typing import Any, Dict, Optional
from datetime import datetime
from enum import Enum

from Backend.research.engine.dataset_loader import DatasetLoader
# Foundation event bus import would go here for real integration
# from Backend.foundation.event_bus import EventBus


logger = logging.getLogger(__name__)


class ReplayState(Enum):
    READY = "READY"
    PLAYING = "PLAYING"
    PAUSED = "PAUSED"
    STOPPED = "STOPPED"
    COMPLETED = "COMPLETED"


class ReplayEngine:
    """
    Market Replay Engine.
    Streams historical data sequentially as a state machine simulating live market events.
    """

    def __init__(self, dataset_loader: DatasetLoader, event_bus: Any = None) -> None:
        self.dataset_loader = dataset_loader
        self.event_bus = event_bus
        self.state = ReplayState.READY
        self.speed_multiplier = 1.0
        
        self._lock = threading.RLock()
        self._play_event = threading.Event()
        
        self._events_cache = []
        self._current_index = 0
        
        self._worker_thread: Optional[threading.Thread] = None
        self._stop_requested = False

    def initialize(self, snapshot_id: str, storage_path: str) -> None:
        """Loads dataset into memory for replay."""
        with self._lock:
            if self.state not in (ReplayState.READY, ReplayState.STOPPED, ReplayState.COMPLETED):
                raise RuntimeError(f"Cannot initialize while in state {self.state}")
            
            # Load entire dataset into RAM for fast replay access
            self._events_cache = list(self.dataset_loader.load_and_verify(snapshot_id, storage_path))
            self._current_index = 0
            self.state = ReplayState.READY

    def start(self, speed_multiplier: float = 1.0) -> None:
        """Starts replay loop."""
        with self._lock:
            if self.state not in (ReplayState.READY, ReplayState.PAUSED):
                raise RuntimeError(f"Cannot start replay from state {self.state}")
                
            self.speed_multiplier = speed_multiplier
            self.state = ReplayState.PLAYING
            self._stop_requested = False
            self._play_event.set()
            
            if self._worker_thread is None or not self._worker_thread.is_alive():
                self._worker_thread = threading.Thread(target=self._replay_loop, daemon=True)
                self._worker_thread.start()

    def pause(self) -> None:
        """Pauses the replay loop."""
        with self._lock:
            if self.state == ReplayState.PLAYING:
                self.state = ReplayState.PAUSED
                self._play_event.clear()

    def resume(self) -> None:
        """Resumes a paused replay."""
        self.start(self.speed_multiplier)

    def seek(self, timestamp: Optional[datetime] = None, bar_index: Optional[int] = None) -> None:
        """
        Seeks replay to a specific timestamp or exact bar index deterministically.
        Must pause before seeking to avoid race conditions.
        """
        with self._lock:
            was_playing = (self.state == ReplayState.PLAYING)
            self.pause()
            
            if timestamp:
                # Seek to first event >= timestamp
                idx = 0
                for i, ev in enumerate(self._events_cache):
                    if ev["timestamp"] >= timestamp:
                        idx = i
                        break
                else:
                    idx = len(self._events_cache) # End of file
                self._current_index = idx
            elif bar_index is not None:
                if bar_index < 0 or bar_index > len(self._events_cache):
                    raise ValueError(f"Bar index {bar_index} out of bounds")
                self._current_index = bar_index
                
            if was_playing:
                self.resume()

    def single_step(self) -> None:
        """Emits exactly one event and remains paused."""
        with self._lock:
            if self.state == ReplayState.PLAYING:
                self.pause()
                
            if self._current_index < len(self._events_cache):
                self._emit_event(self._events_cache[self._current_index])
                self._current_index += 1
            
            if self._current_index >= len(self._events_cache):
                self.state = ReplayState.COMPLETED
                self._emit_completion()

    def stop(self) -> None:
        """Stops replay entirely."""
        with self._lock:
            self.state = ReplayState.STOPPED
            self._stop_requested = True
            self._play_event.set() # Unblock loop so it can exit
            if self._worker_thread:
                self._worker_thread.join(timeout=1.0)
                self._worker_thread = None

    def reset(self) -> None:
        """Resets replay cursor to 0. Requires explicit START to resume."""
        with self._lock:
            self.stop()
            self._current_index = 0
            self.state = ReplayState.READY

    def _emit_event(self, event_data: Dict[str, Any]) -> None:
        """Dispatches event to Foundation EventBus simulating LiveQuoteEngine."""
        if self.event_bus:
            # self.event_bus.publish(...)
            pass
            
    def _emit_completion(self) -> None:
        if self.event_bus:
            pass

    def _replay_loop(self) -> None:
        """Background thread executing the replay schedule."""
        last_real_time = time.perf_counter()
        
        while not self._stop_requested:
            self._play_event.wait()
            if self._stop_requested:
                break
                
            with self._lock:
                if self.state != ReplayState.PLAYING:
                    continue
                
                if self._current_index >= len(self._events_cache):
                    self.state = ReplayState.COMPLETED
                    self._emit_completion()
                    self._play_event.clear()
                    break
                    
                current_event = self._events_cache[self._current_index]
                self._emit_event(current_event)
                self._current_index += 1
                
                # If speed is unlimited (<= 0), don't sleep
                if self.speed_multiplier <= 0:
                    continue

                # Simulate wall-clock time scaled by multiplier
                # (For true time-series replay, we'd delta against previous event timestamp)
                # For this implementation, we simulate generic pacing.
                time.sleep(0.01 / self.speed_multiplier) 
