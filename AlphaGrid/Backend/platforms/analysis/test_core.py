from Backend.platforms.analysis.core import (
    AnalysisContext, AnalysisResult, AnalysisRegistration, 
    AnalysisRegistry, BaseAnalysis, AnalysisFactory, AnalysisEngine
)

class DummyTechnicalAnalysis(BaseAnalysis):
    def get_registration(self) -> AnalysisRegistration:
        return AnalysisRegistration(
            id="dummy_tech_01",
            name="DummyTechnical",
            category="Technical",
            subcategory="Trend",
            required_indicators=["EMA", "RSI"],
            required_markets=["Crypto", "Stocks"]
        )

    def execute(self, context: AnalysisContext) -> AnalysisResult:
        res = AnalysisResult(
            analysis_type="Technical",
            market=context.market,
            symbol=context.symbol,
            timeframe=context.timeframe,
            status="SUCCESS",
            confidence=85.5,
            numeric_score=0.75,
            normalized_score=75.0,
            signals=["BUY"],
            evidence="EMA crossed above price"
        )
        return res

def test_engine():
    # Register dummy class in factory
    AnalysisFactory.register_class("DummyTechnical", DummyTechnicalAnalysis)
    
    # Import and register the real implementation
    from Backend.platforms.analysis.technical.trend.MovingAverageTrendAnalysis import MovingAverageTrendAnalysis
    AnalysisFactory.register_class("MovingAverageTrendAnalysis", MovingAverageTrendAnalysis)
    
    # Initialize Engine
    engine = AnalysisEngine()
    
    # Create Context for Dummy
    context = AnalysisContext(
        market="Crypto",
        symbol="BTC/USD",
        timeframe="1H",
        indicators={"EMA": 50000.0, "RSI": 45.0, "EMA_9": 52000.0, "EMA_21": 51000.0, "SMA_50": 49000.0, "SMA_200": 45000.0}
    )
    
    # Execute Pipeline with both
    results = engine.execute(["DummyTechnical", "MovingAverageTrendAnalysis"], context)
    
    # Assert Dummy
    assert "DummyTechnical" in results
    res_dummy = results["DummyTechnical"]
    assert res_dummy.is_valid()
    
    # Assert Real MovingAverageTrendAnalysis
    assert "MovingAverageTrendAnalysis" in results
    res_ma = results["MovingAverageTrendAnalysis"]
    assert res_ma.is_valid()
    assert res_ma.metadata["trend_direction"] == "BULLISH"
    assert res_ma.numeric_score == 80.0
    
    print("Platform 5 (Analysis Core) successfully executed!")
    print(f"MA Trend Result: {res_ma}")

if __name__ == "__main__":
    test_engine()
