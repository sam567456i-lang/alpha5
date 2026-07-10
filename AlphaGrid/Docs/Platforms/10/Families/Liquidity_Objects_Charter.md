---
Authority: Level 2
Parent: Docs/Governance/Platform10_Family_Development_Standard.md
Domain: Core Institutional Objects
Platform: 10
Family: Liquidity Objects
Version: 1.0.0
Status: ACTIVE
CRL: CRL-1
---

# Liquidity Objects Family Charter

## 1. Purpose
The Liquidity Objects Family manages persistent spatial zones derived from historical price action where liquidity is assumed to rest. It is responsible for initializing, managing, and tracking the lifecycle of these distinct object types.

## 2. Scope
The Liquidity Objects Family is strictly organized by object type, never by arbitrary timeframes. It owns:
- **ReferenceLevel:** PDH, PDL, PWH, PWL, PMH, PML.
- **SwingLiquidity:** Swing High, Swing Low, EQH, EQL.
- **SessionLiquidity:** Asian High/Low, London High/Low, NY High/Low.
- **RangeLiquidity:** IRL, ERL, Premium, Discount, Equilibrium.
- **LiquidityPool:** Buy Side, Sell Side, Resting.

Every emitted object possesses a unique `LiquidityObjectIdentity` containing UUID, Object Type, Creation Time, Source, Parent Objects, Timeframe, Confidence, Version, and Lifecycle State.

## 3. The Object Lifecycle
Liquidity Objects are stateful and persistent. They follow a strict immutable lifecycle:
`Candidate` → `Detected` → `Confirmed` → `Active` → `Inactive` → `Consumed` → `Superseded` → `Archived`

## 4. Explicit Non-Goals (Out of Scope)
Per Platform 10 Rule 6 (Object/Event Separation), the Liquidity Objects Family **shall not**:
- Generate or detect Dynamic Events (Sweeps, Grabs, Raids, Stop Hunts).
- React dynamically to real-time price action crossing levels (this is the sole domain of `Liquidity Events`).
- Calculate raw distances or intersections (delegated to Geometry).

## 5. Upstream Dependencies
- `GeometryEvidence` (Containment, Touch, Overlap, Distance)
- `RangeBoundaryEvidence` (Premium/Discount anchors)
- `SwingEvidence` (Swing High/Low sources)
- `TimeEvidence` (Session definitions)

## 6. Downstream Consumers
- **Liquidity Events:** Subscribes to Liquidity Objects by Identity to determine when they are Swept or Grabbed.
- **Institutional Zones:** Aggregates Liquidity Objects and Structure to form high-probability zones.
