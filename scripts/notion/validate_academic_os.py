#!/usr/bin/env python3
"""Validate Academic OS Notion workspace against the expected manifest."""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

from academic_os_client import NotionClient, NotionError

STATE_PATH = Path(__file__).resolve().parent / ".academic_os_state.json"

REQUIRED_DATABASES = {
    "universities": "Universities",
    "professors": "Professors",
    "phd_positions": "PhD Positions",
    "applications": "Applications",
    "application_documents": "Application Documents",
    "research_projects": "Research Projects",
    "research_questions": "Research Questions",
    "experiments": "Experiments",
    "research_ideas": "Research Ideas",
    "papers": "Papers",
    "concepts": "Concepts",
    "learning_topics": "Learning Topics",
    "cv_versions": "CV Versions",
    "publications": "Publications",
    "tasks": "Tasks",
}

REQUIRED_RELATIONS = {
    "universities": {"Professors", "Positions", "Applications"},
    "professors": {"University", "Relevant Papers", "PhD Positions", "Applications"},
    "phd_positions": {"University", "Professor", "Application"},
    "applications": {
        "Position",
        "University",
        "Professor",
        "CV Version",
        "SOP Version",
        "Cover Letter",
        "Documents",
    },
    "research_projects": {
        "Paper",
        "Research Questions",
        "Experiments",
        "Research Ideas",
        "Tasks",
    },
    "papers": {"Related Project", "Related Concepts"},
    "concepts": {"Related Concepts", "Papers", "Projects", "Learning Topics"},
    "tasks": {"Project", "Application"},
}


def main() -> int:
    token = os.environ.get("NOTION_API_KEY")
    if not token:
        print("NOTION_API_KEY is not set.", file=sys.stderr)
        return 2
    if not STATE_PATH.exists():
        print(f"Missing state file: {STATE_PATH}", file=sys.stderr)
        return 2

    state = json.loads(STATE_PATH.read_text())
    client = NotionClient(token)
    issues: list[str] = []

    root_id = state.get("root_page_id")
    if not root_id:
        issues.append("root_page_id missing from state")
    else:
        try:
            client._request("GET", f"/pages/{root_id}", version="2022-06-28")
        except NotionError:
            issues.append("root_page_id is not accessible")

    databases = state.get("databases", {})
    for key, title in REQUIRED_DATABASES.items():
        db_id = databases.get(key)
        if not db_id:
            issues.append(f"database missing in state: {key} ({title})")
            continue
        try:
            db = client.retrieve_database(db_id, version="2022-06-28")
        except NotionError as exc:
            issues.append(f"cannot retrieve {key}: {exc}")
            continue
        props = set(db.get("properties", {}))
        for rel in REQUIRED_RELATIONS.get(key, set()):
            if rel not in props:
                issues.append(f"{key}: missing relation/property {rel}")

    report = {
        "ok": not issues,
        "issues": issues,
        "flags": {
            "views_created": state.get("views_created", False),
            "dashboard_linked": state.get("dashboard_linked", False),
            "templates_created": state.get("templates_created", False),
        },
        "seeded": state.get("seeded", {}),
    }
    print(json.dumps(report, indent=2))
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
