from typing import Dict
from Backend.core.interfaces.market_data import Bar
from Backend.core.interfaces.profile_framework import (
    BaseAccumulator, BaseProfileFramework, ProfileIdentity, ProfileSnapshot
)

class VolumeAccumulator(BaseAccumulator[Bar]):
    """
    Accumulates Volume by price.
    Completely isolated from TPO/Time data.
    """
    def __init__(self, bin_size: float = 1.0):
        self.histogram: Dict[float, float] = {}
        self.bin_size = bin_size
        self.poc_price = 0.0
        self.max_volume = 0.0

    def add(self, sample: Bar) -> None:
        """Assigns Volume across the High-Low range of the bar."""
        low_bin = (sample.low_price // self.bin_size) * self.bin_size
        high_bin = (sample.high_price // self.bin_size) * self.bin_size
        
        # Distribute volume evenly across the bins in the range
        num_bins = int((high_bin - low_bin) / self.bin_size) + 1
        vol_per_bin = sample.volume / num_bins
        
        current = low_bin
        while current <= high_bin:
            self.histogram[current] = self.histogram.get(current, 0.0) + vol_per_bin
            # O(1) POC update
            if self.histogram[current] > self.max_volume:
                self.max_volume = self.histogram[current]
                self.poc_price = current
            current += self.bin_size

    def remove(self, sample: Bar) -> None:
        pass 

    def merge(self, other: 'BaseAccumulator[Bar]') -> None:
        pass 

    def snapshot(self, identity: ProfileIdentity) -> ProfileSnapshot:
        return ProfileSnapshot(
            identity=identity,
            histogram=dict(self.histogram),
            poc_price=self.poc_price,
            vah_price=self.poc_price + self.bin_size * 5, 
            val_price=self.poc_price - self.bin_size * 5
        )

    def restore(self, snapshot: ProfileSnapshot) -> None:
        self.histogram = dict(snapshot.histogram)
        self.poc_price = snapshot.poc_price
        self.max_volume = self.histogram.get(self.poc_price, 0.0)

class VolumeProfileEngine(BaseProfileFramework[Bar]):
    """
    Execution engine for Volume Profile.
    Inherits the universal framework and strictly drives the VolumeAccumulator.
    """
    def __init__(self, identity: ProfileIdentity, bin_size: float = 1.0):
        accumulator = VolumeAccumulator(bin_size=bin_size)
        super().__init__(identity, accumulator)
