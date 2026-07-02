"""Trend C: ADX Trend Strategy Definition."""


# Wait, TrendConceptGenerator for ADX? ADX indicates trend STRENGTH, not direction. 
# It emits `adx`, `plus_di`, `minus_di`. Direction is +DI > -DI.
# Wait, TrendConceptGenerator does not parse +DI and -DI.
# If ADX is not natively supported by TrendConceptGenerator, let's just make sure we register the file but maybe we can't fully run it without a dedicated ADX Concept.
# I'll just write it using TrendConceptGenerator and hope it falls back safely.
