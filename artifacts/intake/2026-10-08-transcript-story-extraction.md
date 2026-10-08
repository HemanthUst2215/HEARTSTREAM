# Transcript Story Extraction — 01. Sales - CE Record to Report UST Led Workshop (28-Sep-2026)

**Source:** `01. Sales - CE Record to Report UST Led Workshop-20260928-en-US.docx` (persisted verbatim to `artifacts/intake/2026-10-08-transcript.txt`)
**Intake safety scan:** CLEAN (0 injection hits, 0 PII hits) — `artifacts/intake/2026-10-08-transcript.txt`
**Rulebook:** `docs/intake/user-story-csv-rulebook.yaml` (loaded; column order, taxonomy, title/AC formats applied as-is)

## Workshop scope (verbatim, timestamp 9:18–14:46)
Zinfi selected as PRM platform. Workshop validates partner life-cycle process across Zinfi (PRM) and Dynamics 365 CE. Scope: partner onboarding, lead/opportunity management, deal registration, partner visibility, account planning, training. Explicitly business-process level — not design/solution (13:06–13:10).

## Epic / Feature / User Story map with locators

### Epic 01 — Partner Onboarding & Lifecycle Sync (16:28–41:00)
- Feature 1. Partner Record Creation & Sync (Zenfi → Dynamics)
  - US: Sync approved partner from Zenfi to CRM only after onboarding is finalized (21:03–22:54, 23:50)
  - US: Partner visibility scoped to originating legal entity (27:14–28:47)
  - US: Record ownership — one owner (channel/account manager) with org-wide read visibility within legal entity (31:15–32:55)
  - US: Partner record read-only after sync; edits via approval flow (parking lot decision 39:31–40:06)
- Feature 2. Partner Training Status Sync
  - US: Capture partner training status in CRM, sourced from Zenfi LMS (24:59–25:14, 4:7:16–24 / 3:07:17–28)

### Epic 02 — Partner Account Planning (40:10–42:39)
- Feature 1. Account Planning Data Capture
  - US: Capture only required account-planning data points in CRM; full planning done in Zenfi (40:16–40:56)

### Epic 03 — Lead & Opportunity Management (49:04–2:22:00)
- Feature 1. Lead Creation & Distribution
  - US: Heartstream (sales/marketing) creates leads in CRM and distributes to partners via Zenfi sync (49:37–51:42)
  - US: Account managers can enter and maintain own leads (52:08–52:53)
  - US: Partners may optionally register their own leads in Zenfi, synced to CRM (51:27, 1:00:00–1:00:05 — noted as unlikely/low-adoption, DQ registered)
- Feature 2. Opportunity & Collaboration
  - US: Shared visibility of opportunity notes/communication between partner (Zenfi) and Heartstream (CRM) users (54:53–56:49)
  - US: Configurable opportunity pipeline stages at global level for phase 1 (1:26:03–1:31:48)
- Feature 3. Deal Registration & Channel Conflict
  - US: System prevents duplicate deal registration for the same customer/opportunity (professional/Pro business) (1:09:12–1:11:08)
  - US: Deal-registration flag distinguishes a registered deal from a standard opportunity, configurable by product/solution category (1:13:10–1:14:21)

### Epic 04 — Contract Management (1:47:22–2:34:00)
- Feature 1. Reseller (Sales & Service) Partner Contracts
  - US: Capture sales-partner contract with discount/rebate/pricing terms per product category (1:52:31–1:55:37)
  - US: Capture service-partner contract with spare-part discounts and SLA terms (1:53:17–1:53:29, 2:24:30–2:28:06)
  - US: Contract carries min/max duration (reseller: 1–3 yrs; direct: up to 5 yrs) (2:20:08–2:20:45)
  - US: List price indexing/price-increase mid-contract with 60-day notice to partner (2:18:33–2:19:17)
- Feature 2. Direct Customer Contracts
  - US: Support direct contracts for hospitals/EMS/Group Purchase Organizations, separate from reseller contracts (1:54:02–1:54:16, 2:06:22–2:06:51) — flagged Open DQ, deferred to follow-up session (2:06:12)
- Feature 3. Contract Approval & Visibility
  - US: Contract and approvals visible to partner via Zenfi (2:26:44–2:26:51)

### Epic 05 — Quotation & Discount Approval (1:58:57–2:41:00)
- Feature 1. Quotation Pricing & Discount Workflow
  - US: Quote pricing derives from the partner's contract terms by default (1:59:12–2:04:48)
  - US: Partner-applied additional discount beyond contract triggers tiered approval (account manager → regional sales director → head of finance) (2:16:05–2:17:15)
  - US: Quote can be generated without a full opportunity ("shell opportunity") for low-value/small-quantity items (2:38:44–2:41:04)
- Feature 2. Quote-to-Order Conversion
  - US: Approved quote converts to confirmed sales order in Dynamics 365 CRM, flowing to F&O for fulfillment (2:22:00–2:22:15)
  - US: Requested Delivery Date (RDD) captured on the order before fulfillment starts (2:42:38–2:44:23, mandatory per 2:44:47)
  - US: Quote/order revisions affecting pricing/configuration re-trigger approval; RDD-only changes do not (2:47:19–2:49:17)

### Epic 06 — Order Management & Fulfillment (2:50:05–3:05:33)
- Feature 1. Order Lock & Cancellation Control
  - US: Lock order from cancellation/edit after a defined fulfillment status (2:51:02–2:52:44)
- Feature 2. Shipment & Customs Documentation
  - US: Capture/attach required shipment/customs documents (invoice, certificate of origin, packing list) for applicable regions (2:53:02–2:55:12)

### Epic 07 — Install Base Management (2:55:33–3:07:01)
- Feature 1. Install Base Creation & Trigger
  - US: Install base record created on delivery (preferred) for serialized hardware (2:56:43–2:59:35) — open discussion on exact trigger by product type, DQ registered
  - US: Preserve original ship-to/order location permanently on the install base record (2:57:04–2:57:36)
- Feature 2. Install Base Location Update
  - US: Partner can request install-base location/customer update via Zenfi; CRM team owns and applies the change (2:59:38–3:06:19) — owning CRM team undetermined, DQ registered

### Epic 08 — Partner Case Management (3:07:48–3:08:24)
- Feature 1. Case Escalation
  - US: Partner raises case escalation from Zenfi, synchronized to CRM for triage and ownership (3:07:48–3:08:19) — detailed flow deferred to dedicated case-management session

## Open DQs (register, do not invent)
- DQ-001: Whether partners will meaningfully self-register leads in Zenfi (adoption uncertain) — 1:00:00
- DQ-002: Direct customer (hospital/GPO/EMS) contract model — deferred to follow-up session — 2:06:12
- DQ-003: Exact install-base creation trigger per product type (ship vs delivery vs activation) — 2:56:14
- DQ-004: Owning CRM team for install-base location-change requests — 3:01:02
- DQ-005: North America contracted direct-sales rep system access (Zenfi vs Dynamics) — 2:22:29–2:23:51
- DQ-006: Quoting-tool parity across Zenfi/Dynamics/E-store look-and-feel — 2:12:33 (parking lot)
- DQ-007: Workflow for quoting/ordering very low-value items (e.g., single battery) without creating an opportunity — 2:40:46 (parking lot, solutioning deferred)

## Parking lot items (explicitly deferred by facilitator, not converted to stories)
- Opportunity stage naming/gateways per region — 1:30:30
- Deal-registration "large deal" threshold definition — 1:14:40
- Discount-request workflow detail (tied to opportunity vs independent) — 2:38:00
- Install base ownership for location-change — 3:06:14
