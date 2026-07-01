"""Compute Manager for AI Reproducibility."""

import os
import random
from typing import Optional
import numpy as np


class ComputeManager:
    """
    Manages deterministic compute settings for all AI operations.
    Owns CPU/GPU detection, seed management, thread limits, and BLAS config.
    """

    @staticmethod
    def set_deterministic(seed: int, num_threads: int = 1) -> None:
        """
        Forces deterministic behavior across common libraries.
        
        Args:
            seed: The master random seed.
            num_threads: Limit on parallel threads to avoid non-deterministic race conditions.
        """
        # 1. Standard Python and Numpy
        random.seed(seed)
        np.random.seed(seed)
        
        # 2. Environment level thread controls (BLAS, OpenMP)
        os.environ["OMP_NUM_THREADS"] = str(num_threads)
        os.environ["OPENBLAS_NUM_THREADS"] = str(num_threads)
        os.environ["MKL_NUM_THREADS"] = str(num_threads)
        os.environ["VECLIB_MAXIMUM_THREADS"] = str(num_threads)
        os.environ["NUMEXPR_NUM_THREADS"] = str(num_threads)
        
        # Note: If PyTorch or TensorFlow were imported, we would set their
        # deterministic flags here (e.g., torch.manual_seed, torch.use_deterministic_algorithms).

    @staticmethod
    def get_optimal_device() -> str:
        """
        Detects CPU vs GPU safely.
        """
        # Placeholder for actual hardware detection
        # e.g., return "cuda" if torch.cuda.is_available() else "cpu"
        return "cpu"
