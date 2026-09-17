"""Security event_id helpers (P2.4 / P3 provenance).

Schemas
-------
Legacy (historical P2 / P3 Stage-B R1 ``p3_stage_b_20260916T235438Z_7e401714``)::

    ``{trajectory_id}::t{turn}::{tool}::{reason_or_state}``

Scoped v2 (detector×policy, no repetition)::

    ``{trajectory_id}::{detector_id}::{policy_id}::t{turn}::{tool}::{reason_or_state}``

Scoped v3 (Q1 R2 — includes repetition to avoid cross-R contamination)::

    ``{trajectory_id}::{detector_id}::{policy_id}::R{repetition_id}::t{turn}::{tool}::{reason_or_state}``

Do not rewrite historical Stage-B (R1) event_id strings.
"""

from __future__ import annotations

EVENT_ID_SCHEMA_LEGACY = "p2.event_id.v1"
EVENT_ID_SCHEMA_SCOPED = "p3.event_id.v2"
EVENT_ID_SCHEMA_SCOPED_REP = "p3.event_id.v3"
HISTORICAL_P3_STAGE_B_LEGACY_RUN_ID = "p3_stage_b_20260916T235438Z_7e401714"


def make_security_event_id(
    trajectory_id: str,
    turn_id: int,
    tool_name: str,
    reason_or_state: str,
    *,
    detector_id: str | None = None,
    policy_id: str | None = None,
    repetition_id: str | None = None,
) -> str:
    """Deterministic security ``event_id``.

    ``repetition_id`` (e.g. ``R2``) requires detector_id and policy_id and emits
    the v3 schema so R1/R2 events cannot collide in paired analyses.
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
    if repetition_id is not None:
        if detector_id is None or policy_id is None:
            raise ValueError(
                "repetition_id requires detector_id and policy_id "
                "(p3.event_id.v3)"
            )
        rep = str(repetition_id)
        if not rep:
            raise ValueError("repetition_id must be non-empty")
        return (
            f"{tid}::{detector_id}::{policy_id}::{rep}::t{turn}::{tool}::{reason}"
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
    repetition_id: str | None = None,
) -> str:
    if repetition_id is not None:
        return EVENT_ID_SCHEMA_SCOPED_REP
    if detector_id is not None and policy_id is not None:
        return EVENT_ID_SCHEMA_SCOPED
    return EVENT_ID_SCHEMA_LEGACY
