#!/usr/bin/env python3
"""Provision the Academic OS Notion workspace (idempotent)."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any

from academic_os_client import NotionClient, NotionError, parse_notion_id

STATE_PATH = Path(__file__).resolve().parent / ".academic_os_state.json"
ROOT_TITLE = "🏠 Academic OS"

INITIAL_PROJECTS = ("ADAPTI-GUARD", "Agent Injection Bench")
INITIAL_CONCEPTS = (
    "Transformer",
    "Attention",
    "Dense Models",
    "Mixture of Experts",
    "LLM Agents",
    "Prompt Injection",
    "Indirect Prompt Injection",
    "RAG",
    "Tool Calling",
    "Agent Memory",
    "Runtime Defense",
    "AI Safety",
    "Trustworthy AI",
    "AI Governance",
)


def _select(options: tuple[str, ...]) -> dict:
    return {"select": {"options": [{"name": o} for o in options]}}


def _multi(options: tuple[str, ...] | None = None) -> dict:
    if options:
        return {"multi_select": {"options": [{"name": o} for o in options]}}
    return {"multi_select": {}}


def _relation(db_id: str, synced_name: str | None = None) -> dict:
    rel: dict[str, Any] = {"database_id": db_id}
    if synced_name:
        rel["dual_property"] = {"synced_property_name": synced_name}
    return {"relation": rel}


def _heading(text: str, level: int = 2) -> dict:
    key = f"heading_{level}"
    return {key: {"rich_text": [{"type": "text", "text": {"content": text}}]}}


def _paragraph(text: str) -> dict:
    return {
        "paragraph": {
            "rich_text": [{"type": "text", "text": {"content": text}}],
        }
    }


def load_state() -> dict:
    if STATE_PATH.exists():
        return json.loads(STATE_PATH.read_text())
    return {}


def save_state(state: dict) -> None:
    STATE_PATH.write_text(json.dumps(state, indent=2, sort_keys=True) + "\n")


def ensure_root(client: NotionClient, parent_id: str, state: dict) -> str:
    if state.get("root_page_id"):
        return state["root_page_id"]
    for page in client.search_pages(ROOT_TITLE):
        props = page.get("properties", {})
        title_items = props.get("title", {}).get("title", [])
        title = "".join(t.get("plain_text", "") for t in title_items)
        if title == ROOT_TITLE:
            state["root_page_id"] = page["id"]
            return page["id"]
    page = client.create_page(parent_id, ROOT_TITLE)
    state["root_page_id"] = page["id"]
    client.append_blocks(
        page["id"],
        [
            _heading("🎯 Current Focus"),
            _paragraph("Set your weekly focus here (manual)."),
        ],
    )
    return page["id"]


def create_databases(client: NotionClient, root_id: str, state: dict) -> dict[str, str]:
    db = state.setdefault("databases", {})

    parent = root_id

    def create_if_missing(key: str, title: str, properties: dict) -> str:
        if key in db:
            return db[key]
        existing_id = client.search_databases_under_page(parent, title)
        if existing_id:
            db[key] = existing_id
            return existing_id
        created = client.create_database(parent, title, properties)
        db[key] = created["id"]
        return created["id"]

    universities = create_if_missing(
        "universities",
        "Universities",
        {
            "University": {"title": {}},
            "Country": _select(
                (
                    "Austria",
                    "Belgium",
                    "Denmark",
                    "Finland",
                    "France",
                    "Germany",
                    "Ireland",
                    "Italy",
                    "Netherlands",
                    "Norway",
                    "Portugal",
                    "Spain",
                    "Sweden",
                    "Switzerland",
                    "United Kingdom",
                    "Other",
                )
            ),
            "City": {"rich_text": {}},
            "Website": {"url": {}},
            "Department": {"rich_text": {}},
            "Research Fit": _select(("Strong", "Medium", "Weak", "Unknown")),
            "Status": _select(
                (
                    "Researching",
                    "Target",
                    "Active",
                    "Applied",
                    "Rejected",
                    "Accepted",
                    "Archived",
                )
            ),
            "Notes": {"rich_text": {}},
        },
    )

    professors = create_if_missing(
        "professors",
        "Professors",
        {
            "Professor": {"title": {}},
            "Department": {"rich_text": {}},
            "Country": {"rich_text": {}},
            "Position": {"rich_text": {}},
            "Website": {"url": {}},
            "Google Scholar": {"url": {}},
            "Research Areas": _multi(),
            "Contact Status": _select(
                (
                    "Not Contacted",
                    "Researching",
                    "Drafting Email",
                    "Contacted",
                    "Replied",
                    "Follow-up",
                    "Closed",
                )
            ),
            "Last Contact": {"date": {}},
            "Next Action": {"rich_text": {}},
            "Notes": {"rich_text": {}},
        },
    )

    positions = create_if_missing(
        "phd_positions",
        "PhD Positions",
        {
            "Position": {"title": {}},
            "Country": {"rich_text": {}},
            "Research Area": _multi(),
            "Funding": {"rich_text": {}},
            "Salary": {"rich_text": {}},
            "Contract": {"rich_text": {}},
            "Start Date": {"date": {}},
            "Deadline": {"date": {}},
            "Application URL": {"url": {}},
            "Required Degree": {"rich_text": {}},
            "Required Skills": _multi(),
            "Status": _select(
                (
                    "Found",
                    "Investigating",
                    "Potential",
                    "Preparing",
                    "Applied",
                    "Closed",
                    "Rejected",
                    "Accepted",
                )
            ),
            "Notes": {"rich_text": {}},
        },
    )

    applications = create_if_missing(
        "applications",
        "Applications",
        {
            "Application": {"title": {}},
            "Country": {"rich_text": {}},
            "Deadline": {"date": {}},
            "Status": _select(
                (
                    "Researching",
                    "Preparing",
                    "Ready",
                    "Submitted",
                    "Interview",
                    "Offer",
                    "Rejected",
                    "Withdrawn",
                )
            ),
            "Submitted Date": {"date": {}},
            "Interview Date": {"date": {}},
            "Result": _select(("Pending", "Offer", "Rejected", "Withdrawn")),
            "Notes": {"rich_text": {}},
        },
    )

    documents = create_if_missing(
        "application_documents",
        "Application Documents",
        {
            "Document": {"title": {}},
            "Type": _select(
                (
                    "CV",
                    "SOP",
                    "Cover Letter",
                    "Research Proposal",
                    "Email",
                    "Transcript",
                    "Portfolio",
                    "Other",
                )
            ),
            "Version": {"rich_text": {}},
            "Created": {"date": {}},
            "Updated": {"date": {}},
            "Status": _select(("Draft", "Reviewing", "Final", "Submitted", "Archived")),
            "File": {"files": {}},
            "Notes": {"rich_text": {}},
        },
    )

    projects = create_if_missing(
        "research_projects",
        "Research Projects",
        {
            "Project": {"title": {}},
            "Status": _select(
                (
                    "Idea",
                    "Planning",
                    "Active",
                    "Experimenting",
                    "Writing",
                    "Submitted",
                    "Published",
                    "Archived",
                )
            ),
            "Research Area": _multi(),
            "GitHub": {"url": {}},
            "Start Date": {"date": {}},
            "Target Date": {"date": {}},
            "Notes": {"rich_text": {}},
        },
    )

    questions = create_if_missing(
        "research_questions",
        "Research Questions",
        {
            "Research Question": {"title": {}},
            "Research Area": _multi(),
            "Hypothesis": {"rich_text": {}},
            "Status": _select(
                (
                    "Proposed",
                    "Reviewing",
                    "Experimental",
                    "Supported",
                    "Not Supported",
                    "Rejected",
                    "Archived",
                )
            ),
            "Notes": {"rich_text": {}},
        },
    )

    experiments = create_if_missing(
        "experiments",
        "Experiments",
        {
            "Experiment": {"title": {}},
            "Hypothesis": {"rich_text": {}},
            "Condition": {"rich_text": {}},
            "Models": _multi(),
            "Dataset": {"rich_text": {}},
            "Budget": {"number": {"format": "number"}},
            "Status": _select(
                (
                    "Planned",
                    "Authorized",
                    "Running",
                    "Completed",
                    "Failed",
                    "Invalid",
                    "Archived",
                )
            ),
            "Start Date": {"date": {}},
            "End Date": {"date": {}},
            "Result": {"rich_text": {}},
            "Evidence": {"url": {}},
            "Git Commit": {"rich_text": {}},
            "Report": {"files": {}},
            "Notes": {"rich_text": {}},
        },
    )

    ideas = create_if_missing(
        "research_ideas",
        "Research Ideas",
        {
            "Idea": {"title": {}},
            "Research Area": _multi(),
            "Problem": {"rich_text": {}},
            "Potential Contribution": {"rich_text": {}},
            "Status": _select(
                (
                    "Captured",
                    "Exploring",
                    "Literature Review",
                    "Promising",
                    "Experiment Needed",
                    "Rejected",
                    "Converted to Project",
                )
            ),
            "Notes": {"rich_text": {}},
        },
    )

    papers = create_if_missing(
        "papers",
        "Papers",
        {
            "Paper": {"title": {}},
            "Authors": {"rich_text": {}},
            "Year": {"number": {"format": "number"}},
            "Venue": {"rich_text": {}},
            "URL": {"url": {}},
            "DOI": {"url": {}},
            "Research Area": _multi(),
            "Method": {"rich_text": {}},
            "Dataset": {"rich_text": {}},
            "Model": {"rich_text": {}},
            "Main Finding": {"rich_text": {}},
            "Limitation": {"rich_text": {}},
            "Reading Status": _select(("To Read", "Reading", "Read", "Extracted")),
            "Notes": {"rich_text": {}},
        },
    )

    concepts = create_if_missing(
        "concepts",
        "Concepts",
        {
            "Concept": {"title": {}},
            "Category": _select(("Architecture", "Security", "Governance", "Methods", "Other")),
            "Level": _select(("Intro", "Intermediate", "Advanced")),
            "Definition": {"rich_text": {}},
            "Status": _select(("Learning", "Understood", "Needs Review", "Reference")),
            "Notes": {"rich_text": {}},
        },
    )

    learning = create_if_missing(
        "learning_topics",
        "Learning Topics",
        {
            "Topic": {"title": {}},
            "Category": _select(("AI Security", "Trustworthy AI", "ML Systems", "Research Skills", "Other")),
            "Level": _select(("Intro", "Intermediate", "Advanced")),
            "Status": _select(
                ("Not Started", "Learning", "Practicing", "Understood", "Needs Review")
            ),
            "Notes": {"rich_text": {}},
        },
    )

    cv_versions = create_if_missing(
        "cv_versions",
        "CV Versions",
        {
            "CV": {"title": {}},
            "Version": {"rich_text": {}},
            "Target": _select(("AI Security", "Trustworthy AI", "Research", "General Academic")),
            "Created": {"date": {}},
            "Status": _select(("Draft", "Active", "Archived")),
            "File": {"files": {}},
            "Notes": {"rich_text": {}},
        },
    )

    publications = create_if_missing(
        "publications",
        "Publications",
        {
            "Publication": {"title": {}},
            "Authors": {"rich_text": {}},
            "Venue": {"rich_text": {}},
            "Year": {"number": {"format": "number"}},
            "Status": _select(("Draft", "Submitted", "Under Review", "Accepted", "Published")),
            "URL": {"url": {}},
            "DOI": {"url": {}},
            "Notes": {"rich_text": {}},
        },
    )

    tasks = create_if_missing(
        "tasks",
        "Tasks",
        {
            "Task": {"title": {}},
            "Area": _select(("PhD", "Research", "Learning", "Career", "Admin")),
            "Priority": _select(("Critical", "High", "Medium", "Low")),
            "Status": _select(("Todo", "In Progress", "Blocked", "Done", "Cancelled")),
            "Due Date": {"date": {}},
            "Type": _select(("Action", "Review", "Writing", "Meeting", "Admin", "Other")),
            "Notes": {"rich_text": {}},
        },
    )

    if state.get("relations_configured"):
        return db

    # Relations (second pass)
    client.update_database(
        universities,
        {
            "Professors": _relation(professors, "University"),
            "Positions": _relation(positions, "University"),
            "Applications": _relation(applications, "University"),
        },
    )
    client.update_database(
        professors,
        {
            "University": _relation(universities, "Professors"),
            "Relevant Papers": _relation(papers, "Professors"),
            "PhD Positions": _relation(positions, "Professor"),
            "Applications": _relation(applications, "Professor"),
        },
    )
    client.update_database(
        positions,
        {
            "University": _relation(universities, "Positions"),
            "Professor": _relation(professors, "PhD Positions"),
            "Application": _relation(applications, "Position"),
        },
    )
    client.update_database(
        applications,
        {
            "Position": _relation(positions, "Application"),
            "University": _relation(universities, "Applications"),
            "Professor": _relation(professors, "Applications"),
            "CV Version": _relation(cv_versions, "Applications"),
            "SOP Version": _relation(documents, "Application (SOP)"),
            "Cover Letter": _relation(documents, "Application (Cover Letter)"),
            "Documents": _relation(documents, "Application"),
        },
    )
    client.update_database(
        documents,
        {
            "Application": _relation(applications, "Documents"),
            "Professor": _relation(professors, "Documents"),
        },
    )
    client.update_database(
        projects,
        {
            "Paper": _relation(papers, "Related Project"),
            "Research Questions": _relation(questions, "Project"),
            "Experiments": _relation(experiments, "Project"),
            "Research Ideas": _relation(ideas, "Related Project"),
            "Tasks": _relation(tasks, "Project"),
        },
    )
    client.update_database(
        questions,
        {
            "Project": _relation(projects, "Research Questions"),
            "Experiments": _relation(experiments, "Research Question"),
            "Papers": _relation(papers, "Research Questions"),
        },
    )
    client.update_database(
        experiments,
        {
            "Project": _relation(projects, "Experiments"),
            "Research Question": _relation(questions, "Experiments"),
            "Decision": _relation(questions, "Decision Experiments"),
        },
    )
    client.update_database(
        ideas,
        {
            "Related Papers": _relation(papers, "Related Ideas"),
            "Related Project": _relation(projects, "Research Ideas"),
        },
    )
    client.update_database(
        papers,
        {
            "Related Project": _relation(projects, "Paper"),
            "Related Concepts": _relation(concepts, "Papers"),
        },
    )
    client.update_database(
        concepts,
        {
            "Related Concepts": _relation(concepts, "Related Concepts"),
            "Papers": _relation(papers, "Related Concepts"),
            "Projects": _relation(projects, "Concepts"),
            "Learning Topics": _relation(learning, "Concepts"),
        },
    )
    client.update_database(
        learning,
        {
            "Resources": _relation(papers, "Learning Resources"),
            "Concepts": _relation(concepts, "Learning Topics"),
            "Projects": _relation(projects, "Learning Topics"),
            "Next Topic": _relation(learning, "Previous Topic"),
        },
    )
    client.update_database(
        cv_versions,
        {"Applications": _relation(applications, "CV Version")},
    )
    client.update_database(
        publications,
        {"Project": _relation(projects, "Publications")},
    )
    client.update_database(
        tasks,
        {
            "Project": _relation(projects, "Tasks"),
            "Application": _relation(applications, "Tasks"),
        },
    )

    state["relations_configured"] = True
    return db


def create_database_views(client: NotionClient, db: dict[str, str], state: dict) -> None:
    if state.get("views_created"):
        return

    client.create_view_on_database(
        db["phd_positions"],
        "Active Positions",
        filter_obj={
            "or": [
                {"property": "Status", "select": {"equals": "Found"}},
                {"property": "Status", "select": {"equals": "Investigating"}},
                {"property": "Status", "select": {"equals": "Potential"}},
                {"property": "Status", "select": {"equals": "Preparing"}},
            ]
        },
    )
    client.create_view_on_database(
        db["phd_positions"],
        "Deadlines",
        "table",
        sorts=[{"property": "Deadline", "direction": "ascending"}],
    )
    client.create_view_on_database(
        db["phd_positions"],
        "Potential",
        filter_obj={"property": "Status", "select": {"equals": "Potential"}},
    )
    client.create_view_on_database(
        db["phd_positions"],
        "Applied",
        filter_obj={"property": "Status", "select": {"equals": "Applied"}},
    )
    client.create_view_on_database(
        db["phd_positions"],
        "Closed",
        filter_obj={
            "or": [
                {"property": "Status", "select": {"equals": "Closed"}},
                {"property": "Status", "select": {"equals": "Rejected"}},
            ]
        },
    )

    client.create_view_on_database(
        db["applications"],
        "Application Pipeline",
        "board",
        group_by_property="Status",
    )
    client.create_view_on_database(
        db["applications"],
        "Upcoming Deadlines",
        sorts=[{"property": "Deadline", "direction": "ascending"}],
    )
    client.create_view_on_database(
        db["applications"],
        "Preparing",
        filter_obj={"property": "Status", "select": {"equals": "Preparing"}},
    )
    client.create_view_on_database(
        db["applications"],
        "Submitted",
        filter_obj={"property": "Status", "select": {"equals": "Submitted"}},
    )
    client.create_view_on_database(
        db["applications"],
        "Interviews",
        filter_obj={"property": "Status", "select": {"equals": "Interview"}},
    )
    client.create_view_on_database(
        db["applications"],
        "Offers",
        filter_obj={"property": "Status", "select": {"equals": "Offer"}},
    )
    client.create_view_on_database(
        db["applications"],
        "Rejected",
        filter_obj={"property": "Status", "select": {"equals": "Rejected"}},
    )

    for area in ("PhD", "Research", "Learning"):
        client.create_view_on_database(
            db["tasks"],
            area,
            filter_obj={"property": "Area", "select": {"equals": area}},
        )
    client.create_view_on_database(
        db["tasks"],
        "Today",
        filter_obj={"property": "Due Date", "date": {"equals": "today"}},
    )
    client.create_view_on_database(
        db["tasks"],
        "This Week",
        filter_obj={"property": "Due Date", "date": {"this_week": {}}},
    )
    client.create_view_on_database(
        db["tasks"],
        "Overdue",
        filter_obj={"property": "Due Date", "date": {"before": "today"}},
    )
    client.create_view_on_database(
        db["tasks"],
        "High Priority",
        filter_obj={"property": "Priority", "select": {"equals": "High"}},
    )
    client.create_view_on_database(
        db["tasks"],
        "Blocked",
        filter_obj={"property": "Status", "select": {"equals": "Blocked"}},
    )

    state["views_created"] = True


def create_dashboard_linked_views(client: NotionClient, root_id: str, db: dict[str, str], state: dict) -> None:
    if state.get("dashboard_linked"):
        return

    sections = [
        ("🎓 PhD Applications", None),
        ("🔬 Research", None),
        ("📚 Learning", None),
        ("💼 Career", None),
        ("✅ Tasks", None),
        ("⚠️ Upcoming Deadlines", None),
        ("🔴 Blocked Items", None),
    ]
    children = []
    for heading, _ in sections:
        children.append(_heading(heading))
    client.append_blocks(root_id, children)

    ds = {k: client.data_source_id_for_database(v) for k, v in db.items()}

    client.create_linked_view_on_page(
        root_id,
        ds["applications"],
        "🎓 Application Pipeline",
        "board",
        filter_obj=None,
    )
    client.create_linked_view_on_page(
        root_id,
        ds["applications"],
        "⚠️ Upcoming Deadlines (Applications)",
        sorts=[{"property": "Deadline", "direction": "ascending"}],
    )
    client.create_linked_view_on_page(
        root_id,
        ds["phd_positions"],
        "⚠️ Upcoming Deadlines (Positions)",
        sorts=[{"property": "Deadline", "direction": "ascending"}],
    )
    client.create_linked_view_on_page(
        root_id,
        ds["research_projects"],
        "🔬 Active Research",
        filter_obj={
            "or": [
                {"property": "Status", "select": {"equals": "Active"}},
                {"property": "Status", "select": {"equals": "Experimenting"}},
                {"property": "Status", "select": {"equals": "Writing"}},
            ]
        },
    )
    client.create_linked_view_on_page(
        root_id,
        ds["experiments"],
        "🧪 Experiments",
        "board",
    )
    client.create_linked_view_on_page(
        root_id,
        ds["papers"],
        "📚 Papers To Read",
        filter_obj={"property": "Reading Status", "select": {"equals": "To Read"}},
    )
    client.create_linked_view_on_page(
        root_id,
        ds["research_ideas"],
        "💡 Research Ideas",
        "board",
    )
    client.create_linked_view_on_page(
        root_id,
        ds["tasks"],
        "✅ Tasks",
        filter_obj={
            "and": [
                {"property": "Status", "select": {"does_not_equal": "Done"}},
                {"property": "Status", "select": {"does_not_equal": "Cancelled"}},
            ]
        },
        sorts=[{"property": "Due Date", "direction": "ascending"}],
    )
    client.create_linked_view_on_page(
        root_id,
        ds["tasks"],
        "🔴 Blocked (Tasks)",
        filter_obj={"property": "Status", "select": {"equals": "Blocked"}},
    )
    client.create_linked_view_on_page(
        root_id,
        ds["experiments"],
        "🔴 Blocked (Experiments)",
        filter_obj={
            "or": [
                {"property": "Status", "select": {"equals": "Failed"}},
                {"property": "Status", "select": {"equals": "Invalid"}},
            ]
        },
    )

    state["dashboard_linked"] = True


def create_templates(client: NotionClient, db: dict[str, str], state: dict) -> None:
    if state.get("templates_created"):
        return

    def template_children(sections: tuple[str, ...]) -> list[dict]:
        blocks = []
        for section in sections:
            blocks.append(_heading(section, 3))
            blocks.append(_paragraph(""))
        return blocks

    client.create_page_in_database(
        db["professors"],
        "Professor",
        "Template — Professor",
        template_children(
            (
                "Research Areas",
                "Relevant Papers",
                "Research Connection",
                "Potential PhD Topics",
                "Contact History",
                "Next Action",
                "Notes",
            )
        ),
    )
    client.create_page_in_database(
        db["applications"],
        "Application",
        "Template — Application",
        template_children(
            (
                "Position Summary",
                "Motivation",
                "Document Checklist",
                "Interview Prep",
                "Timeline",
                "Notes",
            )
        ),
    )
    client.create_page_in_database(
        db["research_projects"],
        "Project",
        "Template — Research Project",
        template_children(
            (
                "Overview",
                "Research Questions",
                "Experiments",
                "Paper Draft",
                "GitHub Links",
                "Notes",
            )
        ),
    )
    client.create_page_in_database(
        db["experiments"],
        "Experiment",
        "Template — Experiment",
        template_children(
            (
                "Research Question",
                "Hypothesis",
                "Experimental Design",
                "Models",
                "Dataset",
                "Budget",
                "Execution",
                "Results",
                "Statistical Analysis",
                "Validity",
                "Evidence",
                "Git Commit",
                "Decision",
            )
        ),
    )
    client.create_page_in_database(
        db["papers"],
        "Paper",
        "Template — Paper",
        template_children(
            (
                "Summary",
                "Method",
                "Findings",
                "Limitations",
                "Connections",
                "Notes",
            )
        ),
    )
    client.create_page_in_database(
        db["tasks"],
        "Task",
        "Template — Task",
        template_children(("Context", "Steps", "Blockers", "Notes")),
    )

    state["templates_created"] = True


def seed_initial_rows(client: NotionClient, db: dict[str, str], state: dict) -> None:
    seeded = state.setdefault("seeded", {})
    for name in INITIAL_PROJECTS:
        if name in seeded.get("projects", []):
            continue
        client.create_page_in_database(db["research_projects"], "Project", name)
        seeded.setdefault("projects", []).append(name)

    for name in INITIAL_CONCEPTS:
        if name in seeded.get("concepts", []):
            continue
        client.create_page_in_database(db["concepts"], "Concept", name)
        seeded.setdefault("concepts", []).append(name)


def resolve_parent_id(client: NotionClient, parent_raw: str | None) -> str:
    if parent_raw:
        return parse_notion_id(parent_raw)
    results = client.search_pages("Academic OS")
    for page in results:
        parent = page.get("parent", {})
        if parent.get("type") == "page_id":
            return parent["page_id"]
    raise SystemExit(
        "NOTION_PARENT_PAGE_ID is required: share a parent page with the integration "
        "and pass its ID or URL."
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Provision Academic OS in Notion")
    parser.add_argument("--parent-page-id", default=os.environ.get("NOTION_PARENT_PAGE_ID"))
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    token = os.environ.get("NOTION_API_KEY")
    if not token:
        print("NOTION_API_KEY is not set.", file=sys.stderr)
        return 2
    if args.dry_run:
        print("Dry run OK: credentials present.")
        return 0

    client = NotionClient(token)
    state = load_state()
    try:
        parent_id = resolve_parent_id(client, args.parent_page_id)
        root_id = ensure_root(client, parent_id, state)
        databases = create_databases(client, root_id, state)
        create_database_views(client, databases, state)
        create_dashboard_linked_views(client, root_id, databases, state)
        create_templates(client, databases, state)
        seed_initial_rows(client, databases, state)
        state["parent_page_id"] = parent_id
        save_state(state)
        print(json.dumps({"root_page_id": root_id, "databases": databases}, indent=2))
        return 0
    except NotionError as exc:
        print(f"Notion API error: {exc} body={exc.body}", file=sys.stderr)
        save_state(state)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
