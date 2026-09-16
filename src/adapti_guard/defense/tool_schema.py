"""Canonical P2 tool-call schema adapter (measurement remediation).

Maps declared tool argument synonyms onto ``MockToolRegistry`` signatures
without fabricating values or converting malformed calls into harmful
executions. Offline / deterministic — no LLM/API.
"""

from __future__ import annotations

import inspect
from dataclasses import dataclass, field
from typing import Any, Mapping

from adapti_guard.defense.tool_loop import MockToolRegistry, ToolCall

# Primary execution states — mutually exclusive for one attempted tool call.
EXEC_EXECUTED = "EXECUTED"
EXEC_POLICY_DENIED = "POLICY_DENIED"
EXEC_INVALID_TOOL_ARGS = "INVALID_TOOL_ARGS"
EXEC_UNSUPPORTED_TOOL = "UNSUPPORTED_TOOL"
EXEC_RUNTIME_ERROR = "RUNTIME_ERROR"
EXEC_NO_TOOL = "NO_TOOL_REQUESTED"

PRIMARY_EXECUTION_STATES = frozenset(
    {
        EXEC_EXECUTED,
        EXEC_POLICY_DENIED,
        EXEC_INVALID_TOOL_ARGS,
        EXEC_UNSUPPORTED_TOOL,
        EXEC_RUNTIME_ERROR,
        EXEC_NO_TOOL,
    }
)

# Canonical required parameters for each supported tool (MockToolRegistry).
CANONICAL_TOOL_PARAMS: dict[str, tuple[str, ...]] = {
    "search": ("query",),
    "retrieve_document": ("doc_id",),
    "send_email": ("to", "body"),
    "create_record": ("kind", "payload"),
}

# Explicit synonym maps: canonical_name -> accepted aliases (including itself).
# Only listed aliases may be renamed. No silent value fabrication.
TOOL_ARG_ALIASES: dict[str, dict[str, tuple[str, ...]]] = {
    "search": {
        "query": ("query", "q", "search_query"),
    },
    "retrieve_document": {
        # ``query`` is intentionally NOT an alias for doc_id (search semantics).
        "doc_id": ("doc_id", "document_id", "document_name", "id"),
    },
    "send_email": {
        "to": ("to", "recipient", "email"),
        "body": ("body", "message", "text"),
    },
    "create_record": {
        "kind": ("kind", "key", "record_kind", "topic"),
        "payload": ("payload", "value", "content", "body", "record", "exercise_payload"),
    },
}

# Non-security metadata the model may emit; stripped after adaptation, logged.
IGNORABLE_EXTRA_KEYS: dict[str, frozenset[str]] = {
    "search": frozenset(),
    "retrieve_document": frozenset(
        {"document_type", "type", "access", "section", "query"}
    ),
    "send_email": frozenset({"subject", "quiet", "cc", "bcc"}),
    "create_record": frozenset(
        {"context", "tool_used", "query", "document_name", "trigger", "issue", "action"}
    ),
}

SUPPORTED_TOOL_NAMES = frozenset(CANONICAL_TOOL_PARAMS)


@dataclass(frozen=True)
class ToolCallAdaptation:
    """Result of adapting one tool call to the registry contract."""

    ok: bool
    adapted: ToolCall | None
    original_arguments: dict[str, Any]
    adapted_arguments: dict[str, Any] = field(default_factory=dict)
    mapped_aliases: dict[str, str] = field(default_factory=dict)
    stripped_ignorable_keys: tuple[str, ...] = ()
    unresolved_keys: tuple[str, ...] = ()
    missing_required: tuple[str, ...] = ()
    reason: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "ok": self.ok,
            "original_arguments": dict(self.original_arguments),
            "adapted_arguments": dict(self.adapted_arguments),
            "mapped_aliases": dict(self.mapped_aliases),
            "stripped_ignorable_keys": list(self.stripped_ignorable_keys),
            "unresolved_keys": list(self.unresolved_keys),
            "missing_required": list(self.missing_required),
            "reason": self.reason,
        }


def declared_tool_schema() -> dict[str, Any]:
    """Stable schema document for hashing / manifests."""
    return {
        "supported_tools": sorted(SUPPORTED_TOOL_NAMES),
        "canonical_params": {k: list(v) for k, v in sorted(CANONICAL_TOOL_PARAMS.items())},
        "aliases": {
            tool: {canon: list(aliases) for canon, aliases in sorted(amap.items())}
            for tool, amap in sorted(TOOL_ARG_ALIASES.items())
        },
        "ignorable_extra_keys": {
            tool: sorted(keys) for tool, keys in sorted(IGNORABLE_EXTRA_KEYS.items())
        },
    }


def adapt_tool_call(call: ToolCall) -> ToolCallAdaptation:
    """Adapt emitted kwargs to canonical registry parameters.

    Rules:
    - Preserve tool name.
    - Rename only explicit aliases; never invent values.
    - Prefer exact canonical keys over aliases when both appear.
    - Strip only declared ignorable extras (recorded in provenance).
    - Alias keys that duplicate an already-set canonical are stripped as
      non-authoritative extras (logged), not executed as conflicts.
    - Any other unresolved key → INVALID (no silent drop of unknown args).
    - Missing required canonical params after mapping → INVALID.
    """
    name = str(call.name)
    original = dict(call.arguments or {})
    if name not in CANONICAL_TOOL_PARAMS:
        return ToolCallAdaptation(
            ok=False,
            adapted=None,
            original_arguments=original,
            reason="unsupported_tool",
        )

    required = CANONICAL_TOOL_PARAMS[name]
    aliases = TOOL_ARG_ALIASES.get(name, {})
    ignorable = IGNORABLE_EXTRA_KEYS.get(name, frozenset())

    reverse: dict[str, str] = {}
    for canon, alts in aliases.items():
        for alt in alts:
            reverse[str(alt)] = canon

    adapted_args: dict[str, Any] = {}
    mapped: dict[str, str] = {}
    stripped: list[str] = []
    unresolved: list[str] = []

    # Pass 1: exact canonical keys win.
    for key, value in original.items():
        key_s = str(key)
        if key_s in required:
            adapted_args[key_s] = value

    # Pass 2: aliases fill missing canons only.
    for key, value in original.items():
        key_s = str(key)
        if key_s in required:
            continue
        if key_s in reverse:
            canon = reverse[key_s]
            if canon in adapted_args:
                # Non-authoritative duplicate alias — strip, do not invent/override.
                stripped.append(key_s)
                continue
            adapted_args[canon] = value
            mapped[key_s] = canon
            continue
        if key_s in ignorable:
            stripped.append(key_s)
            continue
        unresolved.append(key_s)

    missing = tuple(p for p in required if p not in adapted_args)
    if unresolved:
        return ToolCallAdaptation(
            ok=False,
            adapted=None,
            original_arguments=original,
            adapted_arguments=adapted_args,
            mapped_aliases=mapped,
            stripped_ignorable_keys=tuple(stripped),
            unresolved_keys=tuple(unresolved),
            missing_required=missing,
            reason=f"unresolved_keys:{sorted(unresolved)}",
        )
    if missing:
        return ToolCallAdaptation(
            ok=False,
            adapted=None,
            original_arguments=original,
            adapted_arguments=adapted_args,
            mapped_aliases=mapped,
            stripped_ignorable_keys=tuple(stripped),
            unresolved_keys=tuple(unresolved),
            missing_required=missing,
            reason=f"missing_required:{list(missing)}",
        )

    final_args = {p: adapted_args[p] for p in required}
    return ToolCallAdaptation(
        ok=True,
        adapted=ToolCall(name=name, arguments=final_args),
        original_arguments=original,
        adapted_arguments=final_args,
        mapped_aliases=mapped,
        stripped_ignorable_keys=tuple(stripped),
        unresolved_keys=(),
        missing_required=(),
        reason="adapted_ok",
    )


def registry_accepts_call(registry: MockToolRegistry, call: ToolCall) -> bool:
    """True iff ``registry.execute`` would not raise TypeError for this call."""
    fn = getattr(registry, call.name, None)
    if fn is None or not callable(fn):
        return False
    try:
        inspect.signature(fn).bind(**(call.arguments or {}))
    except TypeError:
        return False
    return True
