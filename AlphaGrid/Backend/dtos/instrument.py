from dataclasses import dataclass

class AssetClass:
    EQUITY = 'EQUITY'
    FUTURES = 'FUTURES'
    OPTIONS = 'OPTIONS'

@dataclass(frozen=True)
class InstrumentID:
    symbol: str
    exchange: str
    asset_class: str
    
    def __str__(self):
        return f'{self.exchange}:{self.symbol}'
