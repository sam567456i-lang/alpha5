import numpy as np
import pandas as pd
import cProfile
import pstats
from Backend.features.macd_generator import MACDFeatureGenerator

np.random.seed(99)
size = 50000
df = pd.DataFrame({
    "close": np.random.randn(size) * 10 + 100,
    "volume": np.random.randint(100, 1000, size)
})
df.attrs['symbol'] = 'PERF'
df.attrs['timeframe'] = '1m'

new_gen = MACDFeatureGenerator()

def run():
    for _ in range(100):
        new_gen.generate(df, "trace", "corr")

cProfile.run('run()', 'scratch/profile_stats')
p = pstats.Stats('scratch/profile_stats')
p.sort_stats('cumulative').print_stats(20)
