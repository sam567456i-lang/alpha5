---
Authority: Level 2
Parent: Docs/Governance/Platform10_Family_Development_Standard.md
Type: Capability Family Specification
Domain: Core Institutional Objects
Platform: 10
Version: 1.0.0
Status: ACTIVE
CRL: CRL-2
---

# Liquidity Objects Family Specification

**Family:** Liquidity Objects
**Owns:** ✓ Objects, ✓ Lifecycle, ✓ Quality
**Consumes:** ✓ Time, ✓ Price, ✓ Swing, ✓ Range, ✓ Geometry
**Publishes:** ✓ LiquidityObjectEvidence, ✓ LiquidityLifecycleEvidence, ✓ LiquidityQualityEvidence
**Never Publishes:** ✗ Events, ✗ Interpretations, ✗ Decisions, ✗ Methodology Terms

## 1. Domain Definition
The **Liquidity Objects Family** identifies, persists, and manages the lifecycle of structural price zones presumed to harbor liquidity. Per Platform 10 Rule 6, it explicitly strictly produces **Objects** and delegates dynamic price interactions (Sweeps, Grabs) to the **Liquidity Events** family.

It strictly categorizes these objects into:
- **ReferenceLevel:** PDH, PDL, PWH, PWL, PMH, PML.
- **SwingLiquidity:** Swing High, Swing Low, EQH, EQL.
- **SessionLiquidity:** Asian High/Low, London High/Low, NY High/Low.
- **RangeLiquidity:** IRL, ERL, Premium, Discount, Equilibrium.
- **LiquidityPool:** Buy Side, Sell Side, Resting.

## 2. Identity and State Management
Every liquidity object is a first-class entity managed via a `LiquidityObjectIdentity`. 

### 2.1 The Identity Struct
- `UUID`: Globally unique identifier.
- `ObjectType`: ReferenceLevel, SwingLiquidity, SessionLiquidity, RangeLiquidity, LiquidityPool.
- `OriginFamily`: The family that produced the underlying primitive.
- `CreationTime`: Origin timestamp.
- `ConfirmationTime`: Timestamp when the object transitioned to Confirmed state.
- `Timeframe`: Evaluated resolution.
- `PriceRange`: The price or span of prices bounding the liquidity object.
- `ParentObjects`: UUIDs of any contributing primitives.
- `LifecycleState`: Current state in the lifecycle.
- `Confidence`: Objective scalar (0.0 to 1.0) denoting cluster strength.
- `Version`: Increments on state transition.
- `ReplayID`: Unique identifier linking to the precise tick simulation state.
- `Checksum`: Hash of the struct state for bit-for-bit replay validation.

### 2.2 The Lifecycle State Machine
1. **Candidate:** Object tentatively identified but unconfirmed.
2. **Detected:** Object structurally valid but pending confirmation buffer.
3. **Confirmed:** Object locked into history.
4. **Active:** Object currently exposed to live price action.
5. **Inactive:** Object still exists but is too distant from current price to be relevant for immediate processing.
6. **Consumed:** Object fully liquidated by price action.
7. **Superseded:** Object eclipsed by a newer, more prominent object of the same type.
8. **Archived:** Object retired from memory (written to historical data store).

## 3. Engine Components
The family is composed of the following orchestrated engines:

### 3.1 Reference Level Engine
- **Purpose:** Extracts static absolute high/low limits from calendar aggregations (PDH, PDL, PMH, PML).
- **Inputs:** `TimeEvidence`, `PriceEvidence`.

### 3.2 Swing Liquidity Engine
- **Purpose:** Upgrades `SwingEvidence` (e.g. Confirmed Pivots) into `SwingLiquidity` objects. Detects structural clusters (EQH/EQL).
- **Inputs:** `SwingEvidence`, `GeometryEvidence`.

### 3.3 Session Liquidity Engine
- **Purpose:** Translates Time boundaries (Asian, London, NY) into actionable High/Low liquidity zones.
- **Inputs:** `TimeEvidence`, `PriceEvidence`.

### 3.4 Range Liquidity Engine
- **Purpose:** Translates structural ranges into discrete gradient objects (Premium, Discount, Equilibrium, IRL, ERL).
- **Inputs:** `RangeBoundaryEvidence`, `GeometryEvidence`.

### 3.5 Liquidity Pool Engine
- **Purpose:** Aggregates individual Reference, Swing, Session, and Range objects into unified `BuySide` or `SellSide` Resting Pools.
- **Inputs:** Outputs from Engines 3.1 - 3.4.

## 4. Certification Gates
This family cannot be marked complete until all engines pass the strict 19-step standard execution lifecycle, culminating in a `Liquidity_Objects_Certification.md` report.
