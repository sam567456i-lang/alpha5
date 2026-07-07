from typing import Any
from Backend.market_data.pipeline import INormalizer
from Backend.core.events import CanonicalMarketEvent, EventProvenance
from Backend.dtos.provider import DataQualityScore
from Backend.dtos.instrument import InstrumentID, AssetClass

class DefaultNormalizer(INormalizer):
    def normalize(self, raw_payload: Any, quality: DataQualityScore, provenance: EventProvenance) -> CanonicalMarketEvent:
        if not isinstance(raw_payload, dict):
            return CanonicalMarketEvent(provenance=provenance, quality=quality, instrument_id=InstrumentID('UNKNOWN', 'UNKNOWN', AssetClass.EQUITY))

        symbol = raw_payload.get('symbol', 'UNKNOWN')
        exchange = raw_payload.get('exchange', 'NSE')
        instrument_id = InstrumentID(exchange=exchange, symbol=symbol, asset_class=AssetClass.EQUITY)
        
        price = float(raw_payload.get('price', raw_payload.get('ltp', 0.0)))
        volume = float(raw_payload.get('volume', 0.0))
        bid = raw_payload.get('bid')
        ask = raw_payload.get('ask')
        
        return CanonicalMarketEvent(
            provenance=provenance, quality=quality, instrument_id=instrument_id,
            price=price, volume=volume, bid=bid, ask=ask
        )
