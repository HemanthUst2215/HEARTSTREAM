#!/usr/bin/env python3
"""DEV / REGRESSION ONLY — sample row corpus for layout and validator tests.

Not invoked by `/generate-user-stories-from-transcript` at runtime. Production runs
author rows from the transcript + rulebook + catalogs only. Replace or extend the
fixture functions when adding regression cases; do not treat this module as a
domain template for future workshops.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

try:
    import yaml
except ImportError:
    yaml = None

from ado_user_story_csv_layout import (  # noqa: E402
    acceptance_criteria_cell,
    apply_generation_defaults,
    blank_row,
    headers_from_rulebook,
    issue_description_cell,
    write_csv,
)

RULEBOOK = ROOT / "docs" / "intake" / "user-story-csv-rulebook.yaml"


def _headers() -> list[str]:
    if yaml is None:
        raise SystemExit("pip install pyyaml")
    rb = yaml.safe_load(RULEBOOK.read_text(encoding="utf-8"))
    return headers_from_rulebook(rb)


def blank() -> dict[str, str]:
    return blank_row(_headers())


def ac_lines(*bullets: str) -> str:
    return acceptance_criteria_cell(*bullets)


def risk_desc(risk: str, impact: str, mitigation: str) -> str:
    return issue_description_cell(risk, impact, mitigation)


def ce_workshop_2026_09_28_rows() -> list[dict[str, str]]:
    """Row set for Sales CE Record to Report workshop (2026-10-08 intake)."""
    rows: list[dict[str, str]] = []

    w = blank()
    w.update(
        {
            "Work Item Type": "Workshop",
            "Title": "01. Sales - CE Record to Report UST Led Workshop-20260928",
            "Description": (
                "UST-led workshop on Dynamics 365 CE record-to-report flow: partner lifecycle with ZINFI, "
                "lead and opportunity management, deal registration, quoting and approvals, fulfillment "
                "visibility, and install base topics discussed on 28-Sept-2026."
            ),
            "Area Path": r"Day 2\CRM",
            "Start Date": "28-09-2026 08:00",
        }
    )
    rows.append(w)

    e = blank()
    e.update(
        {
            "Work Item Type": "Epic",
            "Title": "01. Sales - CE Record to Report",
            "Description": (
                "End-to-end sales processes in Dynamics 365 CE from customer and partner record creation "
                "through quoting, order fulfillment visibility, and downstream reporting alignment."
            ),
        }
    )
    rows.append(e)

    f1 = blank()
    f1.update(
        {
            "Work Item Type": "Feature",
            "Title": "1. Partner lifecycle and Dynamics 365 CE synchronization",
            "Description": (
                "Input: ZINFI PRM onboarding and authorization; Activities: sync approved partners, "
                "training status, and visibility by legal entity; Output: authoritative partner data in CE."
            ),
            "Area Path": r"Day 2\CRM",
        }
    )
    rows.append(f1)

    f2 = blank()
    f2.update(
        {
            "Work Item Type": "Feature",
            "Title": "2. Deal registration, quoting, and fulfillment visibility",
            "Description": (
                "Input: reseller contracts and partner opportunities; Activities: deal registration, "
                "quotation discount approvals, ERP fulfillment status sync; Output: controlled channel sales and partner visibility."
            ),
            "Area Path": r"Day 2\CRM",
        }
    )
    rows.append(f2)

    stories = [
        (
            "Sync authorized partner to D365 CE after ZINFI onboarding",
            "As a CRM administrator, I need to synchronize a partner to Dynamics 365 CE only after ZINFI onboarding is complete including diligence, contract, and required training, so that CE contains finalized authorized partners only.",
            (
                "Partner is not created in CE before final onboarding is confirmed in ZINFI.",
                "Sync occurs when agreed activation criteria (contract, diligence, training) are met.",
                "Synced partner appears in the correct legal entity.",
            ),
        ),
        (
            "Link ZINFI and CE partner account identifiers",
            "As an integration owner, I need to link the ZINFI account number with the Dynamics 365 CE account record for each approved partner, so that partner data stays traceable across systems.",
            (
                "Each approved partner has a linked identifier in ZINFI and CE.",
                "Associated primary contact syncs with the account.",
                "Link is visible on the CE partner account.",
            ),
        ),
        (
            "Restrict partner visibility by legal entity",
            "As a sales user, I need to limit partner records synced from ZINFI to visibility within the associated HeartStream legal entity or region, so that partners outside my region are not exposed.",
            (
                "A partner onboarded for USA is visible only in the USA legal entity.",
                "Users in other legal entities do not see that partner in lists or search.",
                "Cross-region partner scenarios are handled per agreed exception rules.",
            ),
        ),
        (
            "Expose synced partners to authorized CRM sales users",
            "As a sales user, I need to allow authorized CRM users in a legal entity to view partners synced from ZINFI for that entity, so that order booking, lead, and opportunity work can use current partner data.",
            (
                "Authorized CRM users in the entity can open synced partner accounts.",
                "Partner appears in standard account search for that entity.",
                "Access respects existing CRM security roles.",
            ),
        ),
        (
            "Capture partner training status in CE from ZINFI",
            "As an account manager, I need to synchronize required partner training and certification status from ZINFI into Dynamics 365 CE, so that partner readiness is visible for sales and service processes.",
            (
                "Training completion status is received from ZINFI.",
                "Status is linked to the correct partner and contact.",
                "Completed, in-progress, and expired states are distinguishable.",
            ),
        ),
        (
            "Distinguish deal registration from standard opportunity",
            "As a channel manager, I need to mark and track deal registrations separately from standard opportunities in CRM, so that partner-claimed end-customer deals are identifiable.",
            (
                "User can indicate a deal registration on the relevant opportunity record.",
                "Deal registrations are searchable apart from non-registration opportunities.",
                "Registration is associated with the registering dealer or partner.",
            ),
        ),
        (
            "Check existing deal registration for end customer",
            "As a channel manager, I need to search CRM for an existing deal registration or opportunity for an end-user customer before assisting another distributor, so that duplicate partner pursuit is avoided.",
            (
                "Search returns prior deal registration or opportunity for the end customer when it exists.",
                "User can determine which dealer holds the registration.",
                "Result supports channel conflict decisions.",
            ),
        ),
        (
            "Apply reseller contract pricing to quotations",
            "As a sales operations user, I need to apply pricing from the active reseller contract and price group to channel partner quotations, so that quoted products reflect agreed commercial terms.",
            (
                "Quotation lines use contract price group where applicable.",
                "Products outside the contract scope are flagged or blocked per policy.",
                "Contract reference is traceable on the quote.",
            ),
        ),
        (
            "Route non-contract quotation discounts through approval tiers",
            "As a partner account manager, I need to route quotation discount variations beyond contractual limits through a tiered approval matrix, so that pricing exceptions are controlled.",
            (
                "Within-contract discounts proceed without extra approval when policy allows.",
                "Higher discounts route to partner account manager approval.",
                "Largest discounts require finance approval per matrix.",
            ),
        ),
        (
            "Notify approvers of pending quotation approvals",
            "As an approver, I need to receive timely notification when a quotation requires my approval, so that partner deals are not delayed.",
            (
                "Approver receives notification when a quote enters their approval step.",
                "Notification identifies quote, partner, and discount context.",
                "Pending items are visible in an approver work queue or equivalent.",
            ),
        ),
        (
            "Skip re-approval for delivery date only changes",
            "As a sales user, I need to change only the requested delivery date on an already approved quotation without restarting the full pricing approval flow, so that schedule updates are efficient.",
            (
                "RDD-only change does not trigger pricing approval.",
                "Pricing and configuration unchanged remain as approved.",
                "Audit trail records the delivery date change.",
            ),
        ),
        (
            "Re-approve quotation after pricing or configuration change",
            "As a sales user, I need to restart quotation approval when pricing or configuration changes before order confirmation, so that unauthorized discounts or configs are not ordered.",
            (
                "Price change before order confirm requires re-approval.",
                "Configuration change before order confirm requires re-approval.",
                "Cancellation or revision paths follow the same approval rules as stated in workshop.",
            ),
        ),
        (
            "Synchronize fulfillment status from ERP to CRM and ZINFI",
            "As a partner user, I need to view order fulfillment status synchronized from ERP through CRM to ZINFI, so that partners see current fulfillment state in the partner portal.",
            (
                "Key fulfillment statuses sync ERP to CRM.",
                "CRM to ZINFI sync exposes current status to partners.",
                "Status shown matches ERP at agreed sync frequency.",
            ),
        ),
        (
            "Control updates to install base device location",
            "As a service operations user, I need to follow a controlled process to update serialized install base location and customer address, so that recalls and service visits use accurate device location.",
            (
                "Location change requires defined ownership and validation.",
                "Approved updates change install base location on the serial record.",
                "Changes are auditable.",
            ),
        ),
        (
            "Raise partner support requests from ZINFI to CRM",
            "As a partner user, I need to escalate requests from ZINFI that synchronize to Dynamics 365 CE for triage, so that HeartStream can respond to partner-raised issues.",
            (
                "Partner can submit escalation from ZINFI.",
                "Request creates or updates a case or work item in CRM.",
                "CRM routing assigns triage per service process.",
            ),
        ),
        (
            "Support direct and indirect sales quotation paths",
            "As a sales user, I need to use CRM quotation flows for both direct HeartStream sales and indirect channel partner scenarios discussed in the workshop, so that regional models are accommodated.",
            (
                "Direct sales quotation path is available where discussed.",
                "Indirect partner quotation path respects partner-owned pricing tools where applicable.",
                "Regional exceptions are documented in fit-gap notes when required.",
            ),
        ),
        (
            "Create CE customer record for record-to-report flow",
            "As a sales operations user, I need to create customer records in Dynamics 365 CE with the agreed identifier (CRN), so that downstream record-to-report processes receive the correct starting entity.",
            (
                "CE customer or account record is created per agreed CRN rules.",
                "Record is available to downstream order and reporting processes.",
                "Creation timing aligns with workshop R2R discussion.",
            ),
        ),
        (
            "Track open contract examples for fit-gap analysis",
            "As a contracts analyst, I need to capture complex contract examples including pricing, discounts, rebates, and territory limits as tracked open items, so that contract fit-gap can be completed.",
            (
                "Complex contract samples are requested and logged as open items.",
                "Fit-gap disposition can be recorded when analysis completes.",
                "Ownership for contract examples is assigned.",
            ),
        ),
    ]

    for title, desc, bullets in stories:
        s = blank()
        s.update(
            {
                "Work Item Type": "User Story",
                "Title": title,
                "Description": desc,
                "Acceptance Criteria": ac_lines(*bullets),
            }
        )
        rows.append(s)

    for title, risk, impact, mitigation in [
        (
            "Partner master data edit ownership unresolved",
            "Ownership and edit rights for partner master data in CE after ZINFI sync remain in parking lot.",
            "Unauthorized changes may affect orders, credit, and contracts.",
            "Define read-only default and approval path with HeartStream sales ops.",
        ),
        (
            "QMS alignment for partner-reported patient events",
            "Case creation for customer feedback and patient events may not align with QMS and partner channel.",
            "Quality events may be missed or duplicated.",
            "Align in upcoming service workshop with quality team.",
        ),
    ]:
        i = blank()
        i.update(
            {
                "Work Item Type": "Issue",
                "Title": title,
                "Description": risk_desc(risk, impact, mitigation),
                "Area Path": r"Day 2\CRM",
            }
        )
        rows.append(i)

    return rows


def emit_csv(path: Path, rows: list[dict[str, str]]) -> None:
    if yaml is None:
        raise SystemExit("pip install pyyaml")
    rb = yaml.safe_load(RULEBOOK.read_text(encoding="utf-8"))
    headers = headers_from_rulebook(rb)
    projected: list[dict[str, str]] = []
    for row in rows:
        apply_generation_defaults(rb, row)
        if "Title" not in headers:
            row.pop("Title", None)
        projected.append({h: row.get(h) or "" for h in headers})
    write_csv(path, headers, projected)


def main() -> None:
    out = ROOT / "artifacts/intake/.pipeline/2026-10-08-user-stories-working.csv"
    rows = ce_workshop_2026_09_28_rows()
    emit_csv(out, rows)
    print(f"wrote {out} ({len(rows)} rows)")


if __name__ == "__main__":
    main()
