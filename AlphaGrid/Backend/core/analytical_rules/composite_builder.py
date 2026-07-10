from typing import List, Dict
from Backend.core.interfaces.profile_framework import ProfileSnapshot, ProfileIdentity

class CompositeProfileBuilder:
    """
    Aggregation layer for building composite profiles natively.
    Preserves single-responsibility by extracting merging logic out of the accumulators.
    """
    
    def merge_snapshots(self, snapshots: List[ProfileSnapshot], new_identity: ProfileIdentity) -> ProfileSnapshot:
        """
        Merges multiple daily/session snapshots into a larger composite snapshot.
        """
        if not snapshots:
            raise ValueError("Cannot merge empty snapshot list.")
            
        composite_histogram: Dict[float, float] = {}
        
        # Merge histograms
        for snap in snapshots:
            for price, val in snap.histogram.items():
                composite_histogram[price] = composite_histogram.get(price, 0.0) + val
                
        # Recompute POC
        max_val = -1
        poc_price = 0.0
        for price, val in composite_histogram.items():
            if val > max_val:
                max_val = val
                poc_price = price
                
        # Simple VA placeholder math
        bin_size = 1.0 # Should be extracted from policy
        vah_price = poc_price + bin_size * 5
        val_price = poc_price - bin_size * 5
        
        return ProfileSnapshot(
            identity=new_identity,
            histogram=composite_histogram,
            poc_price=poc_price,
            vah_price=vah_price,
            val_price=val_price
        )
