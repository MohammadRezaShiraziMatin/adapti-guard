"""Security event_id helpers (P2.4 / P3 provenance).

Historical P2 and P3 Stage-B (`p3_stage_b_20260916T235438Z_7e401714`) used the
legacy schema without detector/policy:

    ``{trajectory_id}::t{turn}::{tool}::{reason_or_state}``

That caused identical ``event_id`` strings to recur across detector×policy arms
of the same trajectory/turn (per-arm dedup still correct for metrics).

Scoped schema (future P3 live when ``detector_id`` + ``policy_id`` are supplied):

    ``{trajectory_id}::{detector_id}::{policy_id}::t{turn}::{tool}::{reason_or_state}``

Do not rewrite historical run artifacts to the scoped schema.
"""

from __future__ import annotations

EVENT_ID_SCHEMA_LEGACY = "p2.event_id.v1"
EVENT_ID_SCHEMA_SCOPED = "p3.event_id.v2"
HISTORICAL_P3_STAGE_B_LEGACY_RUN_ID = "p3_stage_b_20260916T235438Z_7e401714"


def make_security_event_id(
    trajectory_id: str,
    turn_id: int,
    tool_name: str,
    reason_or_state: str,
    *,
    detector_id: str | None = None,
    policy_id: str | None = None,
) -> str:
    """Deterministic security ``event_id``.

    When both ``detector_id`` and ``policy_id`` are provided, emit the scoped
    schema so IDs are unique across trajectory×detector×policy×turn×event.
    Otherwise emit the legacy schema (P2 / historical P3 Stage-B compatible).
    """
    tid = str(trajectory_id)
    tool = str(tool_name)
    reason = str(reason_or_state)
    turn = int(turn_id)
    if (detector_id is None) ^ (policy_id is None):
        raise ValueError(
            "detector_id and policy_id must both be set or both omitted "
            "for make_security_event_id"
        )
    if detector_id is not None and policy_id is not None:
        return (
            f"{tid}::{detector_id}::{policy_id}::t{turn}::{tool}::{reason}"
        )
    return f"{tid}::t{turn}::{tool}::{reason}"


def event_id_schema_for(
    *,
    detector_id: str | None = None,
    policy_id: str | None = None,
) -> str:
    if detector_id is not None and policy_id is not None:
        return EVENT_ID_SCHEMA_SCOPED
    return EVENT_ID_SCHEMA_LEGACY
