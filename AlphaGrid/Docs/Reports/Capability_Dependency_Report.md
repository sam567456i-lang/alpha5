# Capability Dependency Report

This report illustrates the explicitly mapped dependency graph of the planned architecture.

### ftr-ohlcv (Platform 9)
Lineage: Data Provider -> **OHLCV** -> Raw Price Data

### con-trend (Platform 10)
Lineage: Swing -> **Trend** -> Uptrend -> Downtrend -> Sideways

### ftr-atr (Platform 0)
Lineage: (No Inputs) -> **ATR Feature Generator** -> (No Outputs)

### ftr-sr (Platform 0)
Lineage: (No Inputs) -> **Support/Resistance Feature Generator** -> (No Outputs)

### ftr-hlbreakout (Platform 0)
Lineage: (No Inputs) -> **High/Low Breakout Feature Generator** -> (No Outputs)

### ftr-volbreakout (Platform 0)
Lineage: (No Inputs) -> **Volatility Breakout Feature Generator** -> (No Outputs)

### con-breakout (Platform 0)
Lineage: (No Inputs) -> **Breakout Concept Generator** -> (No Outputs)

### meth-breakout (Platform 0)
Lineage: TrendState -> TrendFeature -> TrendConcept -> **Breakout Methodology** -> BreakoutSignal

### sig-breakout (Platform 0)
Lineage: (No Inputs) -> **Breakout Primitive Signal Generator** -> (No Outputs)

### strat-srbreakout (Platform 0)
Lineage: (No Inputs) -> **S/R Breakout Strategy** -> (No Outputs)

### strat-hlbreakout (Platform 0)
Lineage: (No Inputs) -> **High/Low Breakout Strategy** -> (No Outputs)

### strat-volbreakout (Platform 0)
Lineage: (No Inputs) -> **Volatility Breakout Strategy** -> (No Outputs)

### ana-100 (Platform 8)
Lineage: Raw Price Data -> **Trend Analysis** -> TrendState

### ana-101 (Platform 8)
Lineage: Raw Price Data -> **Momentum Analysis** -> MomentumState

### ana-102 (Platform 8)
Lineage: Raw Price Data -> **Volume Analysis** -> VolumeState

### ana-103 (Platform 8)
Lineage: Raw Price Data -> **Volatility Analysis** -> VolatilityState

### ana-104 (Platform 8)
Lineage: Raw Price Data -> **Geometry Analysis** -> GeometryState

### ana-105 (Platform 8)
Lineage: Raw Price Data -> **Price Action Analysis** -> PriceActionState

### ana-106 (Platform 8)
Lineage: Raw Price Data -> **Liquidity Analysis** -> LiquidityState

### ana-107 (Platform 8)
Lineage: Raw Price Data -> **Market Structure Analysis** -> MarketStructureState

### ana-108 (Platform 8)
Lineage: Raw Price Data -> **Imbalance Analysis** -> ImbalanceState

### ana-109 (Platform 8)
Lineage: Raw Price Data -> **Institutional Zones Analysis** -> InstitutionalZonesState

### ana-110 (Platform 8)
Lineage: Raw Price Data -> **Auction Market Theory Analysis** -> AuctionMarketTheoryState

### ana-111 (Platform 8)
Lineage: Raw Price Data -> **Volume Profile Analysis** -> VolumeProfileState

### ana-112 (Platform 8)
Lineage: Raw Price Data -> **Market Profile Analysis** -> MarketProfileState

### ana-113 (Platform 8)
Lineage: Raw Price Data -> **Wyckoff Analysis** -> WyckoffState

### ana-114 (Platform 8)
Lineage: Raw Price Data -> **Options Analysis** -> OptionsState

### ana-115 (Platform 8)
Lineage: Raw Price Data -> **Open Interest Analysis** -> OpenInterestState

### ana-116 (Platform 8)
Lineage: Raw Price Data -> **Greeks Analysis** -> GreeksState

### ana-117 (Platform 8)
Lineage: Raw Price Data -> **Implied Volatility Analysis** -> ImpliedVolatilityState

### ana-118 (Platform 8)
Lineage: Raw Price Data -> **Dealer Positioning Analysis** -> DealerPositioningState

### ana-119 (Platform 8)
Lineage: Raw Price Data -> **Expiry Behaviour Analysis** -> ExpiryBehaviourState

### ana-120 (Platform 8)
Lineage: Raw Price Data -> **Futures Build-up Analysis** -> FuturesBuild-upState

### ana-121 (Platform 8)
Lineage: Raw Price Data -> **India VIX Analysis** -> IndiaVIXState

### ana-122 (Platform 8)
Lineage: Raw Price Data -> **Market Breadth Analysis** -> MarketBreadthState

### ana-123 (Platform 8)
Lineage: Raw Price Data -> **Macro Analysis** -> MacroState

### ana-124 (Platform 8)
Lineage: Raw Price Data -> **Statistical Analysis** -> StatisticalState

### ana-125 (Platform 8)
Lineage: Raw Price Data -> **Quantitative Analysis** -> QuantitativeState

### ana-126 (Platform 8)
Lineage: Raw Price Data -> **Machine Learning Features Analysis** -> MachineLearningFeaturesState

### ana-127 (Platform 8)
Lineage: Raw Price Data -> **Session Analysis** -> SessionState

### ana-128 (Platform 8)
Lineage: Raw Price Data -> **Time Analysis** -> TimeState

### ana-129 (Platform 8)
Lineage: Raw Price Data -> **Calendar Analysis** -> CalendarState

### ana-130 (Platform 8)
Lineage: Raw Price Data -> **Multi-Timeframe Analysis** -> Multi-TimeframeState

### meth-200 (Platform 13)
Lineage: TrendState -> TrendFeature -> TrendConcept -> **Trend Following Methodology** -> TrendFollowingSignal

### meth-201 (Platform 13)
Lineage: TrendState -> TrendFeature -> TrendConcept -> **Mean Reversion Methodology** -> MeanReversionSignal

### meth-202 (Platform 13)
Lineage: TrendState -> TrendFeature -> TrendConcept -> **ICT Methodology** -> ICTSignal

### meth-203 (Platform 13)
Lineage: TrendState -> TrendFeature -> TrendConcept -> **SMC Methodology** -> SMCSignal

### meth-204 (Platform 13)
Lineage: WyckoffState -> TrendFeature -> TrendConcept -> **Wyckoff Methodology** -> WyckoffSignal

### meth-205 (Platform 13)
Lineage: TrendState -> TrendFeature -> TrendConcept -> **ORB Methodology** -> ORBSignal

### meth-207 (Platform 13)
Lineage: TrendState -> TrendFeature -> TrendConcept -> **Pullback Methodology** -> PullbackSignal

### meth-208 (Platform 13)
Lineage: TrendState -> TrendFeature -> TrendConcept -> **Range Methodology** -> RangeSignal

### meth-209 (Platform 13)
Lineage: TrendState -> TrendFeature -> TrendConcept -> **Scalping Methodology** -> ScalpingSignal

### meth-210 (Platform 13)
Lineage: TrendState -> TrendFeature -> TrendConcept -> **Intraday Methodology** -> IntradaySignal

### meth-211 (Platform 13)
Lineage: TrendState -> TrendFeature -> TrendConcept -> **Swing Methodology** -> SwingSignal

### meth-212 (Platform 13)
Lineage: TrendState -> TrendFeature -> TrendConcept -> **Positional Methodology** -> PositionalSignal

### meth-213 (Platform 13)
Lineage: OptionsState -> TrendFeature -> TrendConcept -> **Options Methodology** -> OptionsSignal

### meth-214 (Platform 13)
Lineage: VolatilityState -> TrendFeature -> TrendConcept -> **Volatility Methodology** -> VolatilitySignal

### meth-215 (Platform 13)
Lineage: TrendState -> TrendFeature -> TrendConcept -> **Pairs Methodology** -> PairsSignal

### meth-216 (Platform 13)
Lineage: TrendState -> TrendFeature -> TrendConcept -> **Seasonality Methodology** -> SeasonalitySignal

### intel-300 (Platform 22)
Lineage: Opportunity -> Signal -> ExecutionState -> **Filtering Capability** -> FilteringView

### intel-301 (Platform 22)
Lineage: Opportunity -> Signal -> ExecutionState -> **Sorting Capability** -> SortingView

### intel-302 (Platform 22)
Lineage: Opportunity -> Signal -> ExecutionState -> **Ranking Capability** -> RankingView

### intel-303 (Platform 22)
Lineage: Opportunity -> Signal -> ExecutionState -> **Searching Capability** -> SearchingView

### intel-304 (Platform 22)
Lineage: Opportunity -> Signal -> ExecutionState -> **Grouping Capability** -> GroupingView

### intel-305 (Platform 22)
Lineage: Opportunity -> Signal -> ExecutionState -> **Saved Views Capability** -> SavedViewsView

### intel-306 (Platform 22)
Lineage: Opportunity -> Signal -> ExecutionState -> **Bookmarks Capability** -> BookmarksView

### intel-307 (Platform 22)
Lineage: Opportunity -> Signal -> ExecutionState -> **Layouts Capability** -> LayoutsView

### intel-308 (Platform 22)
Lineage: Opportunity -> Signal -> ExecutionState -> **Watchlists Capability** -> WatchlistsView

### intel-309 (Platform 22)
Lineage: Opportunity -> Signal -> ExecutionState -> **Portfolio Filters Capability** -> PortfolioFiltersView

### intel-310 (Platform 22)
Lineage: Opportunity -> Signal -> ExecutionState -> **Risk Filters Capability** -> RiskFiltersView

### intel-311 (Platform 22)
Lineage: Opportunity -> Signal -> ExecutionState -> **Market Filters Capability** -> MarketFiltersView

### intel-312 (Platform 22)
Lineage: Opportunity -> Signal -> ExecutionState -> **Timeframe Filters Capability** -> TimeframeFiltersView

### intel-313 (Platform 22)
Lineage: Opportunity -> Signal -> ExecutionState -> **Strategy Filters Capability** -> StrategyFiltersView

### intel-314 (Platform 22)
Lineage: TrendState -> TrendFeature -> TrendConcept -> **Methodology Filters Capability** -> MethodologyFiltersSignal

### intel-315 (Platform 22)
Lineage: Raw Price Data -> **Analysis Filters Capability** -> AnalysisFiltersState

### intel-316 (Platform 22)
Lineage: Opportunity -> Signal -> ExecutionState -> **State Filters Capability** -> StateFiltersView

### intel-317 (Platform 22)
Lineage: Opportunity -> Signal -> ExecutionState -> **Feature Filters Capability** -> FeatureFiltersView

### intel-318 (Platform 22)
Lineage: Opportunity -> Signal -> ExecutionState -> **Concept Filters Capability** -> ConceptFiltersView

### intel-319 (Platform 22)
Lineage: Opportunity -> Signal -> ExecutionState -> **Evidence Filters Capability** -> EvidenceFiltersView

### intel-320 (Platform 22)
Lineage: Opportunity -> Signal -> ExecutionState -> **Confidence Filters Capability** -> ConfidenceFiltersView

### intel-321 (Platform 22)
Lineage: Opportunity -> Signal -> ExecutionState -> **Recommendation Filters Capability** -> RecommendationFiltersView

### intel-322 (Platform 22)
Lineage: Opportunity -> Signal -> ExecutionState -> **Opportunity Filters Capability** -> OpportunityFiltersView

### intel-323 (Platform 22)
Lineage: Opportunity -> Signal -> ExecutionState -> **Execution Filters Capability** -> ExecutionFiltersView

### intel-324 (Platform 22)
Lineage: Opportunity -> Signal -> ExecutionState -> **Explainability Filters Capability** -> ExplainabilityFiltersView

