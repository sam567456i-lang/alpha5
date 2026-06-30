# AlphaGrid Infinity X 5.0 — API & Service Contracts

## Overview

All API endpoints are served at:

```
http://localhost:8000/api/v1/<domain>/...
```

Interactive documentation is available at:
- Swagger UI: `http://localhost:8000/api/docs`
- ReDoc: `http://localhost:8000/api/redoc`

---

## Response Envelope

Every REST response returns a consistent JSON envelope.

### Success
```json
{
  "success": true,
  "message": "OK",
  "data": {},
  "timestamp": "2026-06-30T18:00:00Z",
  "execution_time": 0.0042
}
```

### Paginated List
```json
{
  "success": true,
  "message": "OK",
  "data": [],
  "pagination": {
    "total": 100,
    "page": 1,
    "page_size": 50,
    "total_pages": 2
  },
  "timestamp": "...",
  "execution_time": 0.003
}
```

### Error
```json
{
  "success": false,
  "error_code": "VALIDATION_ERROR",
  "message": "Request validation failed.",
  "details": [{ "loc": ["body", "quantity"], "msg": "value must be greater than 0" }],
  "timestamp": "..."
}
```

---

## HTTP Status Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 201 | Created |
| 204 | No Content (archive/delete) |
| 400 | Validation Error |
| 403 | Forbidden |
| 404 | Not Found |
| 409 | Conflict |
| 422 | Unprocessable Entity (path/query param type error) |
| 429 | Rate Limit Exceeded |
| 500 | Internal Server Error |
| 503 | Market Closed |

---

## Error Codes

| Code | Trigger |
|------|---------|
| `VALIDATION_ERROR` | Invalid request body or parameter |
| `NOT_FOUND` | Requested resource does not exist |
| `FORBIDDEN` | Access explicitly denied |
| `CONFLICT` | Duplicate or conflicting state |
| `RATE_LIMIT` | API quota exceeded |
| `MARKET_CLOSED` | Live operation outside market hours |
| `SYSTEM_ERROR` | Unexpected internal error |

---

## REST Endpoints

### Market — `/api/v1/market`

| Method | Path | Purpose |
|--------|------|---------|
| GET | `/status` | Current market session state |
| GET | `/instruments` | Instrument catalog (`?exchange=NSE&segment=F&O`) |
| GET | `/ohlcv` | Historical OHLCV candles (`?symbol=NIFTY&timeframe=15m`) |
| GET | `/live` | Live price quotes (`?symbols=NIFTY,BANKNIFTY`) |
| GET | `/breadth` | Market breadth metrics |
| GET | `/regime` | Detected market regime |
| GET | `/calendar` | Economic calendar |
| GET | `/news` | Market news (`?limit=20&category=rbi`) |

### Options — `/api/v1/options`

| Method | Path | Purpose |
|--------|------|---------|
| GET | `/chain` | Option chain (`?symbol=NIFTY&expiry=2026-07-31`) |
| GET | `/greeks` | Option Greeks |
| GET | `/iv` | Implied Volatility surface |
| GET | `/pcr` | Put-Call Ratio |
| GET | `/max-pain` | Max Pain strike |

### Features — `/api/v1/features`

| Method | Path | Purpose |
|--------|------|---------|
| GET | `` | Latest computed features (`?symbol=NIFTY`) |
| GET | `/history` | Feature time series |
| POST | `/recalculate` | Trigger feature recalculation |

### Strategies — `/api/v1/strategies`

| Method | Path | Purpose |
|--------|------|---------|
| GET | `` | All registered strategies |
| GET | `/{id}` | Single strategy |
| POST | `/{id}/validate` | Trigger paper validation |
| POST | `/{id}/backtest` | Trigger historical backtest |

### Recommendations — `/api/v1/recommendations`

| Method | Path | Purpose |
|--------|------|---------|
| GET | `/live` | Currently active recommendations |
| GET | `/history` | Historical recommendations (paginated) |
| GET | `/{id}` | Single recommendation detail |

### Portfolio — `/api/v1/portfolio`

| Method | Path | Purpose |
|--------|------|---------|
| GET | `` | Portfolio summary with positions and PnL |
| POST | `/trades` | Record a new manual trade |
| PUT | `/trades/{id}` | Update an existing trade |
| DELETE | `/trades/{id}` | Soft-archive a trade |

**POST `/trades` body:**
```json
{
  "symbol": "NIFTY",
  "trade_type": "BUY",
  "quantity": 50,
  "entry_price": 24000.0,
  "notes": "Optional note"
}
```

### Research — `/api/v1/research`

| Method | Path | Purpose |
|--------|------|---------|
| GET | `` | All research experiments (paginated) |
| POST | `/backtest` | Run a research backtest |
| POST | `/replay` | Start a market replay session |

### AI — `/api/v1/ai`

| Method | Path | Purpose |
|--------|------|---------|
| GET | `/predictions` | Recent AI predictions (`?symbol=NIFTY&limit=20`) |
| GET | `/explanation` | AI explanation for a recommendation (`?recommendation_id=<uuid>`) |
| GET | `/models` | Registered AI models |

### Reports — `/api/v1/reports`

| Method | Path | Purpose |
|--------|------|---------|
| GET | `` | All generated reports (paginated) |
| POST | `/generate` | Generate a new report |
| GET | `/{id}` | Download a specific report |

### Dashboard — `/api/v1/dashboard`

| Method | Path | Purpose |
|--------|------|---------|
| GET | `` | Combined dashboard summary |
| GET | `/layout` | User's saved widget layout |
| PUT | `/layout` | Save new widget layout |

### System — `/api/v1/system`

| Method | Path | Purpose |
|--------|------|---------|
| GET | `/status` | System health and component statuses |
| POST | `/live/start` | Transition to Live mode |
| POST | `/live/stop` | Transition to Offline mode |
| POST | `/live/pause` | Pause live data collection |
| POST | `/live/resume` | Resume paused live data collection |

---

## WebSocket Channels

Channels are available at `ws://localhost:8000/ws/<channel>`.

| Channel | URL | Purpose |
|---------|-----|---------|
| Market | `/ws/market` | Live price updates |
| Recommendations | `/ws/recommendations` | New/updated recommendations |
| Portfolio | `/ws/portfolio` | Portfolio state changes |
| AI | `/ws/ai` | AI prediction results |
| News | `/ws/news` | Market news alerts |
| System | `/ws/system` | System health events |

### WebSocket Event Format
```json
{
  "event": "MarketUpdated",
  "data": { ... }
}
```

### WebSocket Events

| Event | Channel | Trigger |
|-------|---------|---------|
| `MarketUpdated` | market | Live price tick |
| `RecommendationCreated` | recommendations | New recommendation |
| `RecommendationUpdated` | recommendations | Score changed |
| `RecommendationExpired` | recommendations | Recommendation expired |
| `TradeAdded` | portfolio | Manual trade recorded |
| `ReportGenerated` | system | Report ready for download |
| `AICompleted` | ai | Prediction pipeline finished |
| `SystemWarning` | system | Health warning detected |

---

## Versioning

- Current version: `/api/v1`
- Breaking changes require a new version prefix: `/api/v2`
- Backward compatibility must be maintained until the old version is formally deprecated

---

## Pagination

List endpoints accept:

| Parameter | Default | Max | Description |
|-----------|---------|-----|-------------|
| `page` | `1` | — | Page number (1-indexed) |
| `page_size` | `50` | `500` | Results per page |

---

## Service Layer Contract

All routers delegate to a typed service class. The service interface is the stable contract — routers must never bypass the service layer.

| Router | Service Class |
|--------|--------------|
| Market | `Backend.api.services.MarketService` |
| Options | `Backend.api.services.OptionsService` |
| Features | `Backend.api.services.FeaturesService` |
| Strategies | `Backend.api.services.StrategiesService` |
| Recommendations | `Backend.api.services.RecommendationsService` |
| Portfolio | `Backend.api.services.PortfolioService` |
| Research | `Backend.api.services.ResearchService` |
| AI | `Backend.api.services.AIService` |
| Reports | `Backend.api.services.ReportsService` |
| Dashboard | `Backend.api.services.DashboardService` |
| System | `Backend.api.services.SystemService` |

When a business module (Market Platform, Portfolio Engine, etc.) is implemented in a later phase, **only the service class body changes** — the router and its contract remain untouched.
