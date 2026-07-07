# Event Architecture Specification
*AlphaGrid Mandatory Infrastructure Framework 2/5*

All asynchronous boundaries within AlphaGrid communicate via a strongly-typed Event Bus. Everything from P10 onward emits events.

## 1. Event Registry (`event_registry.yaml`)
No event can be broadcast unless it is explicitly defined in the global Event Registry.
The registry must define:
* **Event ID**: e.g., `market.session.opened`
* **Producer**: The exact platform emitting the event.
* **Consumers**: The platforms permitted to listen.
* **Payload Schema**: DTO specification.

## 2. Core Events

### 2.1 Market & State Events
* `TickReceived`: Raw inbound market data.
* `MarketOpened` / `MarketClosed`: Hard boundary session events.
* `SessionChanged`: Progression through killzones/sessions.

### 2.2 Pipeline Events
* `FeatureCalculated`: A new derived time-series is available.
* `MethodologyCompleted`: A P10 plugin finished its intent generation.
* `OpportunityDetected`: P12 clustered intents into a single asset opportunity.
* `RecommendationGenerated`: P14 finalized an executable recommendation.
* `RiskRejected` / `RiskApproved`: P15 final pass/fail gate.

### 2.3 User / Presentation Events
* `AlertTriggered`: Triggered by P24 Notifications.

## 3. Event Handling Rules
* **Immutability**: Event payloads MUST be frozen DTOs.
* **Ordering**: Events must contain a monotonic sequence ID to guarantee deterministic ordering.
* **Replay Behavior**: The Event Bus must support a `ReplayMode` which suppresses external IO side effects (e.g. notifications) while allowing full pipeline reconstruction from a historical event log.
