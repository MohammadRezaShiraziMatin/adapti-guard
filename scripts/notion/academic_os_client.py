"""Minimal Notion API client for Academic OS provisioning."""

from __future__ import annotations

import json
import re
import time
from typing import Any

import requests

NOTION_VERSION_LEGACY = "2022-06-28"
NOTION_VERSION_VIEWS = "2025-09-03"
API_BASE = "https://api.notion.com/v1"


class NotionError(RuntimeError):
    def __init__(self, message: str, status: int | None = None, body: Any = None):
        super().__init__(message)
        self.status = status
        self.body = body


def parse_notion_id(value: str) -> str:
    """Normalize a Notion ID or URL to hyphenated UUID."""
    value = value.strip()
    if value.startswith("http"):
        match = re.search(
            r"([0-9a-f]{32}|[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})",
            value,
            re.I,
        )
        if not match:
            raise ValueError(f"Could not parse Notion ID from URL: {value}")
        value = match.group(1)
    compact = value.replace("-", "")
    if len(compact) != 32 or not re.fullmatch(r"[0-9a-f]{32}", compact, re.I):
        raise ValueError(f"Invalid Notion ID: {value}")
    return (
        f"{compact[:8]}-{compact[8:12]}-{compact[12:16]}-"
        f"{compact[16:20]}-{compact[20:]}"
    )


class NotionClient:
    def __init__(self, token: str):
        self.token = token

    def _request(
        self,
        method: str,
        path: str,
        *,
        version: str,
        json_body: dict | None = None,
        params: dict | None = None,
    ) -> dict:
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Notion-Version": version,
            "Content-Type": "application/json",
        }
        url = f"{API_BASE}{path}"
        for attempt in range(5):
            resp = requests.request(
                method, url, headers=headers, json=json_body, params=params, timeout=60
            )
            if resp.status_code == 429:
                time.sleep(min(2 ** attempt, 16))
                continue
            if resp.status_code >= 400:
                try:
                    body = resp.json()
                except json.JSONDecodeError:
                    body = resp.text
                raise NotionError(
                    f"Notion API {method} {path} failed: {resp.status_code}",
                    resp.status_code,
                    body,
                )
            if resp.status_code == 204:
                return {}
            return resp.json()
        raise NotionError(f"Notion API rate limited: {method} {path}", 429)

    def search_pages(self, query: str) -> list[dict]:
        data = self._request(
            "POST",
            "/search",
            version=NOTION_VERSION_LEGACY,
            json_body={"query": query, "filter": {"property": "object", "value": "page"}},
        )
        return data.get("results", [])

    def search_databases_under_page(self, parent_page_id: str, title: str) -> str | None:
        data = self._request(
            "POST",
            "/search",
            version=NOTION_VERSION_LEGACY,
            json_body={
                "query": title,
                "filter": {"property": "object", "value": "database"},
            },
        )
        for item in data.get("results", []):
            parent = item.get("parent", {})
            if parent.get("type") == "page_id" and parent.get("page_id") == parent_page_id:
                db_title = "".join(
                    t.get("plain_text", "")
                    for t in item.get("title", [])
                )
                if db_title == title:
                    return item["id"]
        return None

    def create_page(self, parent_page_id: str, title: str) -> dict:
        return self._request(
            "POST",
            "/pages",
            version=NOTION_VERSION_LEGACY,
            json_body={
                "parent": {"type": "page_id", "page_id": parent_page_id},
                "properties": {
                    "title": {"title": [{"type": "text", "text": {"content": title}}]}
                },
            },
        )

    def append_blocks(self, block_id: str, children: list[dict]) -> dict:
        return self._request(
            "PATCH",
            f"/blocks/{block_id}/children",
            version=NOTION_VERSION_LEGACY,
            json_body={"children": children},
        )

    def create_database(
        self, parent_page_id: str, title: str, properties: dict[str, Any]
    ) -> dict:
        return self._request(
            "POST",
            "/databases",
            version=NOTION_VERSION_LEGACY,
            json_body={
                "parent": {"type": "page_id", "page_id": parent_page_id},
                "title": [{"type": "text", "text": {"content": title}}],
                "is_inline": False,
                "properties": properties,
            },
        )

    def update_database(self, database_id: str, properties: dict[str, Any]) -> dict:
        return self._request(
            "PATCH",
            f"/databases/{database_id}",
            version=NOTION_VERSION_LEGACY,
            json_body={"properties": properties},
        )

    def retrieve_database(self, database_id: str, version: str = NOTION_VERSION_VIEWS) -> dict:
        return self._request(
            "GET", f"/databases/{database_id}", version=version
        )

    def data_source_id_for_database(self, database_id: str) -> str:
        db = self.retrieve_database(database_id, version=NOTION_VERSION_VIEWS)
        sources = db.get("data_sources") or []
        if sources:
            return sources[0]["id"]
        # Legacy fallback: database id often matches single data source id.
        return database_id

    def create_page_in_database(
        self, database_id: str, title_property: str, title: str, children: list[dict] | None = None
    ) -> dict:
        body: dict[str, Any] = {
            "parent": {"database_id": database_id},
            "properties": {
                title_property: {"title": [{"type": "text", "text": {"content": title}}]}
            },
        }
        if children:
            body["children"] = children
        return self._request("POST", "/pages", version=NOTION_VERSION_LEGACY, json_body=body)

    def create_view_on_database(
        self,
        database_id: str,
        name: str,
        view_type: str = "table",
        *,
        filter_obj: dict | None = None,
        sorts: list[dict] | None = None,
        group_by_property: str | None = None,
    ) -> dict:
        body: dict[str, Any] = {
            "database_id": database_id,
            "name": name,
            "type": view_type,
        }
        if filter_obj is not None:
            body["filter"] = filter_obj
        if sorts is not None:
            body["sorts"] = sorts
        if group_by_property and view_type == "board":
            body["configuration"] = {
                "type": "board",
                "group_by": {
                    "type": "select",
                    "property": group_by_property,
                },
            }
        return self._request("POST", "/views", version=NOTION_VERSION_VIEWS, json_body=body)

    def create_linked_view_on_page(
        self,
        page_id: str,
        data_source_id: str,
        name: str,
        view_type: str = "table",
        *,
        filter_obj: dict | None = None,
        sorts: list[dict] | None = None,
        after_block_id: str | None = None,
    ) -> dict:
        body: dict[str, Any] = {
            "create_database": {"parent": {"type": "page_id", "page_id": page_id}},
            "data_source_id": data_source_id,
            "name": name,
            "type": view_type,
        }
        if filter_obj is not None:
            body["filter"] = filter_obj
        if sorts is not None:
            body["sorts"] = sorts
        if after_block_id:
            body["create_database"]["position"] = {
                "type": "after_block",
                "block_id": after_block_id,
            }
        return self._request("POST", "/views", version=NOTION_VERSION_VIEWS, json_body=body)
