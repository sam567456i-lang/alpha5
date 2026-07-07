from typing import Any
from datetime import datetime, timezone
import math
from Backend.market_data.pipeline import IValidator
from Backend.dtos.provider import DataQualityScore

class DataQualityValidator(IValidator):
    def __init__(self):
        self.last_sequence = {}
        self.last_timestamp = {}

    def validate(self, raw_payload: Any) -> DataQualityScore:
        if not isinstance(raw_payload, dict):
            return self._build_fail_score()

        symbol = raw_payload.get('symbol', 'UNKNOWN')
        ts = raw_payload.get('timestamp')
        seq = raw_payload.get('sequence')
        price = raw_payload.get('price')
        volume = raw_payload.get('volume', 0)

        if ts is None or price is None or math.isnan(price):
            return self._build_fail_score()

        seq_score = 1.0
        gap_score = 1.0
        duplicate_score = 1.0
        
        if symbol in self.last_sequence:
            expected_seq = self.last_sequence[symbol] + 1
            if seq == self.last_sequence[symbol]:
                duplicate_score = 0.0
            elif seq > expected_seq:
                gap_score = max(0.0, 1.0 - ((seq - expected_seq) * 0.1))
            elif seq < expected_seq:
                seq_score = 0.0

        self.last_sequence[symbol] = seq

        ts_score = 1.0
        drift_score = 1.0
        now = datetime.now(timezone.utc).timestamp()
        if abs(now - ts) > 5.0:
            drift_score = 0.5

        ohlc_score = 1.0 if price > 0 else 0.0
        vol_score = 1.0 if volume >= 0 else 0.0

        overall = (seq_score + gap_score + duplicate_score + ts_score + drift_score + ohlc_score + vol_score) / 7.0

        return DataQualityScore(
            overall_score=overall, timestamp_score=ts_score, provider_score=1.0,
            exchange_score=1.0, sequence_score=seq_score, gap_score=gap_score,
            duplicate_score=duplicate_score, latency_score=1.0, spread_score=1.0,
            ohlc_score=ohlc_score, volume_score=vol_score, session_score=1.0,
            corporate_action_score=1.0, clock_drift_score=drift_score
        )

    def _build_fail_score(self) -> DataQualityScore:
        return DataQualityScore(0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0)
