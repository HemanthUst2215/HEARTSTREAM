#!/usr/bin/env python3
"""One-shot builder for marketing ws03 user story pipeline artifacts."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

from user_story_pipeline.export_csv import export_invest_scorecard_csv  # noqa: E402
from user_story_pipeline.invest_scorecard import evaluate_all  # noqa: E402

DATE = "2026-10-13-marketing-ws03"
TRANSCRIPT = f"artifacts/intake/{DATE}-transcript.txt"
PREREQ_DOCX = "Pre- read material - 03. D365_CE_ Day 03_Marketing 1_30092026.pptx"
PREREQ_TXT = "artifacts/intake/.pipeline/2026-10-13-marketing-ws03-prerequisite.txt"

CI = {
    "msd365_domain": "CRM",
    "msd365_application": "Customer Insights",
    "msd365_business_entity": "Lead to Opportunity",
}

KB = {
    "schema_version": "1.0",
    "knowledge_base_id": f"{DATE}-workshop-prerequisite-kb",
    "sources": [
        {
            "path": PREREQ_DOCX,
            "title": "D365 CE Solution Modelling Workshop Marketing Sept 2026 pre-read",
            "extracted_text": PREREQ_TXT,
        }
    ],
    "scope": {
        "in_scope_objectives": [
            {
                "id": "OBJ-001",
                "statement": "External analytics data ingestion and unification in D365 Customer Insights (WS-CE-01).",
                "source_path": PREREQ_DOCX,
                "source_locator": "WS-CE-01 / slide External Analytics Data Ingestion & Unification",
                "confidence": "explicit",
            },
            {
                "id": "OBJ-002",
                "statement": "Marketing research insights planning using Customer Insights audiences and analytics (WS-CE-02).",
                "source_path": PREREQ_DOCX,
                "source_locator": "WS-CE-02",
                "confidence": "explicit",
            },
            {
                "id": "OBJ-003",
                "statement": "Global marketing content activation via Customer Insights Journeys (WS-CE-03).",
                "source_path": PREREQ_DOCX,
                "source_locator": "WS-CE-03",
                "confidence": "explicit",
            },
            {
                "id": "OBJ-004",
                "statement": "Brand reputation campaign management with journeys, segmentation, and performance analytics (WS-CE-04).",
                "source_path": PREREQ_DOCX,
                "source_locator": "WS-CE-04",
                "confidence": "explicit",
            },
            {
                "id": "OBJ-005",
                "statement": "Marketing asset governance and campaign readiness (WS-CE-05).",
                "source_path": PREREQ_DOCX,
                "source_locator": "WS-CE-05",
                "confidence": "explicit",
            },
            {
                "id": "OBJ-006",
                "statement": "Marketing strategy and activation planning with KPI tracking (WS-CE-06).",
                "source_path": PREREQ_DOCX,
                "source_locator": "WS-CE-06",
                "confidence": "explicit",
            },
        ],
        "in_scope_modules": [
            {
                "id": "MOD-001",
                "statement": "D365 Customer Insights data sources, profile unification, and dynamic segmentation for distributor and vertical-market models.",
                "source_path": PREREQ_DOCX,
                "source_locator": "Process Flow 1; transcript agenda external analytics focus",
                "confidence": "explicit",
            },
            {
                "id": "MOD-002",
                "statement": "Account and contact 360 views in Customer Insights for marketing audiences (distinct from Sales CRM day-to-day).",
                "source_path": PREREQ_DOCX,
                "source_locator": "Unified customer profile; transcript 58:17–1:02:06",
                "confidence": "derived",
            },
        ],
        "out_of_scope": [
            {
                "id": "OOS-001",
                "statement": "Deep lead-to-opportunity sales process design (separate CRM sales workshops).",
                "source_path": TRANSCRIPT,
                "source_locator": "10:17–10:23 James; session reframed to marketing not lead management",
                "confidence": "explicit",
            },
        ],
    },
    "terminology": [
        {
            "term": "Customer Insights",
            "definition": "Microsoft Dynamics 365 marketing module discussed in workshop (industry term: marketing).",
            "source_path": TRANSCRIPT,
            "source_locator": "5:18–9:05",
        }
    ],
    "constraints": [
        {
            "id": "CON-001",
            "statement": "Standard D365 Customer Insights OOTB assumed in pre-read process flows unless workshop decides otherwise.",
            "source_path": PREREQ_DOCX,
            "source_locator": "Process Flow 1 header",
            "confidence": "explicit",
        }
    ],
}


def story(
    title: str,
    desc: str,
    ac: list[str],
    refs: list[str],
    locator: str,
) -> dict:
    return {
        "State": "New",
        "ID": "",
        "Work Item Type": "User Story",
        "Title 1": "",
        "Title 2": "",
        "Title 3": title,
        "Assigned To": "",
        "Area Path": "",
        "Description": desc,
        "Acceptance Criteria": "\n".join(f"- {line}" for line in ac),
        "Annexure ID1": "",
        "Fit Gap Status": "",
        "User Story Type": "",
        "prerequisite_refs": refs,
        "transcript_locator": locator,
        "transcript_source_path": TRANSCRIPT,
        **CI,
    }


def issue(title: str, desc: str, locator: str) -> dict:
    return {
        "State": "New",
        "ID": "",
        "Work Item Type": "Issue",
        "Title 1": "",
        "Title 2": "",
        "Title 3": title,
        "Assigned To": "",
        "Area Path": "",
        "Description": desc,
        "Acceptance Criteria": "",
        "Annexure ID1": "",
        "Fit Gap Status": "",
        "User Story Type": "",
    }


rows: list[dict] = [
    {
        "State": "In Review",
        "ID": "",
        "Work Item Type": "Workshop",
        "Title 1": "03. D365 CE Day 03 Marketing Customer Insights Workshop - 30-Sep-2026",
        "Title 2": "",
        "Title 3": "",
        "Assigned To": "",
        "Area Path": "Day 3\\CRM",
        "Description": "UST-led Customer Insights (marketing) workshop covering external analytics ingestion and unification, segmentation for distributor and vertical markets, unified profiles, and campaign readiness per WS-CE-01–WS-CE-06 pre-read.",
        "Acceptance Criteria": "",
        "Annexure ID1": "",
        "Fit Gap Status": "",
        "User Story Type": "",
    },
    story(
        "Connect CRM account and contact master data to Customer Insights",
        "As a marketing data steward, I need to connect Dynamics 365 CRM account and contact master data as Customer Insights data sources, so that marketing audiences use the same customer records as CRM.",
        [
            "CRM accounts and contacts are available as ingestible data sources in Customer Insights.",
            "Connection uses organization credentials without separate marketing-only logins.",
            "Source refresh expectations are documented for marketing operations.",
        ],
        ["OBJ-001", "MOD-001"],
        "39:05–45:28",
    ),
    story(
        "Ingest sales order and engagement data for unified profiles",
        "As a marketing analyst, I need to ingest sales orders and digital engagement data into Customer Insights, so that unified profiles reflect purchases and campaign interactions.",
        [
            "Sales order data can be mapped into Customer Insights as a data source.",
            "Engagement sources (for example web, email, events) can be linked to the same profile model.",
            "Marketing users can verify that profile metrics update after source refresh.",
        ],
        ["OBJ-001", "MOD-001"],
        "39:05–45:28",
    ),
    story(
        "Define match rules for unified customer profiles",
        "As a marketing data steward, I need to configure match and merge rules for accounts, contacts, and partner records in Customer Insights, so that duplicate profiles are resolved before segmentation.",
        [
            "Match keys (for example email, partner identifier combinations) are configured for profile unification.",
            "Duplicate profiles are surfaced for resolution per agreed marketing data governance.",
            "Unified profiles show a single 360 view per resolved customer or partner contact.",
        ],
        ["OBJ-001", "MOD-002"],
        "39:05–57:55",
    ),
    story(
        "Create dynamic segments by vertical end-market",
        "As a product marketer, I need to create dynamic Customer Insights segments by vertical end-market (for example hospital, EMS, education), so that I can target campaigns by where products are sold or used.",
        [
            "Segment rules can filter on vertical or market category attributes when present on accounts, contacts, or orders.",
            "At least the priority verticals discussed in workshop (hospital, EMS, fire, military) can be represented as segment criteria.",
            "Segments refresh automatically when underlying source data changes.",
        ],
        ["MOD-001", "OBJ-006"],
        "32:53–37:15",
    ),
    story(
        "Identify distributors serving multiple vertical markets",
        "As a marketing analyst, I need to build intersecting segments that find distributors active in more than one vertical market, so that I can tailor messaging for multi-vertical partners.",
        [
            "Separate segment definitions exist per vertical (for example hospital-focused distributors).",
            "An intersection or combined segment returns distributors qualifying for more than one vertical rule.",
            "Results are exportable for campaign audience selection.",
        ],
        ["MOD-001"],
        "50:33–50:33",
    ),
    story(
        "Use ship-to attributes in Customer Insights segment rules",
        "As a marketing analyst, I need to use segment rules that use ship-to city or address attributes from sales orders when available, so that geographic targeting reflects delivery location not only account headquarters.",
        [
            "Sales order ship-to fields are available as segment attributes when order data is ingested.",
            "Sample segment can filter customers or orders by ship-to city (workshop Houston example pattern).",
            "Documentation notes gaps when ship-to attributes are not yet populated in source data.",
        ],
        ["MOD-001", "OBJ-001"],
        "48:02–48:07",
    ),
    story(
        "Capture end-market segment at e-commerce order entry",
        "As a marketing operations lead, I need to capture end-market or vertical category during e-commerce order entry when feasible, so that Customer Insights segmentation is accurate at order time.",
        [
            "Order capture exposes a field or classification for end-market or vertical where business rules require it.",
            "Captured values flow to data available for Customer Insights segmentation.",
            "Workshop limitation that not all order nuances are capturable is recorded as open design input.",
        ],
        ["MOD-001", "OBJ-006"],
        "45:28–46:53",
    ),
    story(
        "Provide account-level marketing profiles with contact drill-down",
        "As a marketer, I need to view unified Customer Insights profiles at account level with linked contacts, so that I can plan account-based campaigns without losing contact-level detail.",
        [
            "Unified profile view supports account-centric navigation discussed in workshop.",
            "Linked contacts are visible from the account profile context.",
            "Marketing users can build segments using account attributes and related contact attributes.",
        ],
        ["MOD-002", "OBJ-002"],
        "58:17–59:55",
    ),
    story(
        "Enable worldwide marketing analytics visibility for product marketing",
        "As a global product marketer, I need to access Customer Insights analytics and audiences that are not limited to a single sales region, so that worldwide product planning uses consistent customer insight.",
        [
            "Role or audience scoping allows product marketing to view agreed global insight datasets.",
            "Regional sales-only restrictions do not block worldwide marketing views defined in workshop.",
            "Access approach is documented for US, Canada, LATAM, Europe, and Asia stakeholders as applicable.",
        ],
        ["OBJ-002", "MOD-002"],
        "1:04:55–1:05:40",
    ),
    story(
        "Update install base segment after partner tracing import",
        "As a marketing analyst, I need to update device or install-base segment attributes after late partner tracing files are imported, so that vertical market classification reflects tracings received after shipment.",
        [
            "Tracing or spreadsheet import can update install-base or device records linked to distributor shipments.",
            "Updated attributes are available for Customer Insights segmentation after processing.",
            "Process documents manual versus automated tracing timelines discussed in workshop.",
        ],
        ["MOD-001", "OBJ-001"],
        "37:15–38:39",
    ),
    story(
        "Detect vertical sales trends for targeted campaigns",
        "As a field marketer, I need to see emerging vertical sales trends over short periods, so that I can launch timely campaigns when a vertical market momentum spike is detected.",
        [
            "Marketing analytics can compare sales or shipment volumes by vertical over a configurable recent window.",
            "Trend or threshold signal is available to marketing without waiting six months for manual tracing consolidation.",
            "Output can seed audience selection for Customer Insights campaigns.",
        ],
        ["OBJ-006", "OBJ-004"],
        "1:22:55–1:23:49",
    ),
    story(
        "Ingest distributor sold-to location from partner channel into CI",
        "As a marketing data steward, I need to ingest distributor-reported sold-to location from the partner channel into data available to Customer Insights, so that vertical segmentation improves when partners report where units were sold.",
        [
            "Partner portal or channel submission can capture sold-to location or vertical per serial or order line.",
            "Ingested values are linked to distributor and device or order context for analytics.",
            "Data appears in Customer Insights sources after agreed refresh interval.",
        ],
        ["OBJ-001", "MOD-001"],
        "1:26:25–1:27:09",
    ),
    story(
        "Analyze account consumable purchase patterns for marketing outreach",
        "As a marketer, I need to analyze account-level consumable purchase history alongside equipment context in Customer Insights, so that I can identify accounts that stopped buying Philips consumables.",
        [
            "Purchase history for consumable part numbers can be associated with unified account profiles when purchase data is in scope.",
            "Marketers can filter accounts with equipment history but missing recent consumable purchases.",
            "Workshop dependency on complete purchase data linkage is documented.",
        ],
        ["OBJ-002", "MOD-002"],
        "1:31:52–1:33:26",
    ),
    issue(
        "Identify owners for external analytics source inventory",
        "Risk: External analytics sources for Customer Insights are not yet named by Heartstream.\nImpact: Data ingestion and unified analytics design for WS-CE-01 cannot be finalized.\nMitigation: Assign an owner to supply the analytics platform list and KPI definitions requested in workshop.",
        "1:39:11–1:39:27",
    ),
    issue(
        "Expand marketing stakeholder attendance for remaining sessions",
        "Risk: Key regional marketing stakeholders were not on the session invite list.\nImpact: Segmentation and campaign decisions may require a repeat session for global alignment.\nMitigation: Reschedule or repeat marketing workshop segments with worldwide marketing attendees per facilitator offer.",
        "6:01–9:35",
    ),
]


def main() -> None:
    intake = ROOT / "artifacts" / "intake"
    intake.mkdir(parents=True, exist_ok=True)
    (intake / f"{DATE}-workshop-prerequisite-knowledge-base.json").write_text(
        json.dumps(KB, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    (intake / f"{DATE}-user-story-rows.json").write_text(
        json.dumps(rows, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    stories_for_invest = [
        {
            "id": f"US-{i:02d}",
            "title": r.get("Title 3", ""),
            "description": r.get("Description", ""),
            "acceptanceCriteria": r.get("Acceptance Criteria", ""),
        }
        for i, r in enumerate(rows, start=1)
        if r.get("Work Item Type") == "User Story"
    ]
    invest = evaluate_all(stories_for_invest)
    export_invest_scorecard_csv(
        invest, intake / f"{DATE}-invest-scorecard.csv"
    )
    print(f"Wrote {len(rows)} rows, {len(stories_for_invest)} stories for INVEST")


if __name__ == "__main__":
    main()
