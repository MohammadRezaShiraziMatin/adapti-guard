# Cursor agent entry (paste this)

How to start work in this repo. Documentation only. **No merge. No venue submit. No live LLM. No retune.**

## Launch rules

1. **Prefer Cursor IDE Agent** (local Agent chat in the IDE) over Cloud Agent when the task is docs, claims hygiene, or small code that does not need a remote VM.
2. **One new cloud agent per task.** Do not stack a second task onto a running or finished cloud agent. Open a **new** cloud agent, paste the starter block below, then the single task.
3. **Never continue an errored session.** If a cloud agent errors, times out, or leaves a dirty/conflicted tree, do **not** click continue on that session. Start a **new** cloud agent with this paste block and the same (or repaired) task.

Standing orders stay in [`MASTER_PROMPT.md`](MASTER_PROMPT.md) (canonical) and `.cursor/rules/adapti-guard.mdc` (mirror).

## Paste into a new agent (starter block)

Copy everything inside the fence. Replace `<PASTE ONE TASK>` with a single task. Do not add a second task in the same paste.

```text
Docs-only unless the task names otherwise. API=0. No merge. No frozen/AUDIT edits.

Read in this order before editing:
1. docs/START_HERE.md
2. docs/paper/dual_track/DUAL_TRACK_STATUS.md
3. docs/experiments/MASTER_PROMPT.md (canonical 10 invariants)

Track A VNEXT FAIL is immutable (pack 523c8818…). Track B Phase-1 SUPPORTED_IMPROVEMENT does not reverse Track A (pack c789811a…). Default API=0. Human merge only.

Task: <PASTE ONE TASK>
```

## Pointers (do not skip)

| File | Role |
| --- | --- |
| [`docs/START_HERE.md`](../START_HERE.md) | Human entry: read order, tree, P0 / P1 / LIVE gate |
| [`docs/paper/dual_track/DUAL_TRACK_STATUS.md`](../paper/dual_track/DUAL_TRACK_STATUS.md) | Track A vs Track B (read before claims) |
| [`docs/experiments/MASTER_PROMPT.md`](MASTER_PROMPT.md) | Canonical 10 invariants |

If the ask is ambiguous: docs + claims hygiene only. Point to `DUAL_TRACK_STATUS.md`. Do not start live eval, Phase 2 implementation, or venue text as a submit.
