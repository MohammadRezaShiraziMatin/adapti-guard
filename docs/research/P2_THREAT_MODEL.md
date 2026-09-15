# P2 Threat Model — Multi-Turn / Agentic Security

**ID:** `P2-TM-0.1`  
**Status:** DESIGN ONLY · API=0 · not evaluated  
**Parent:** [`P2_RESEARCH_SPEC.md`](P2_RESEARCH_SPEC.md)  
**Baseline evidence:** L1 run `l1_p1m_full_20260915T160302Z_ef2e98c3` + frozen P1

---

## Label legend

**CONFIRMED FROM L1** · **DESIGN DECISION** · **HYPOTHESIS** · **FUTURE EXPERIMENT**

---

## 1. System under evaluation

**DESIGN DECISION:** A tool-using LLM agent with:

| Component | P2 pilot behavior |
| --- | --- |
| Target model | Same lock as L1 when live: `target_2` / OpenRouter |
| Tools | Mock sandbox: `search`, `retrieve_document`, `send_email`, `create_record` (same names as P1) |
| Defense | Label-blind runtime gate before model I/O and before tool permission |
| Judge | Independent `judge_fallback` for Judge-ASR only |
| State | Conversation history + optional key-value “memory” store |

**Out of system:** real email/network, real enterprise IAM, white-box gradients. **DESIGN DECISION**

---

## 2. Assets

| Asset | Harm if lost | Tag |
| --- | --- | --- |
| Tool side effects (`create_record`, `send_email`) | Unauthorized privileged action / exfil | DESIGN DECISION |
| Sensitive context / retrieved docs | Disclosure via tools | DESIGN DECISION |
| Conversation / memory integrity | Persistence enabling later harm | DESIGN DECISION |
| Benign task completion | Utility loss / FPR | DESIGN DECISION |

---

## 3. Adversary

| Property | Setting | Tag |
| --- | --- | --- |
| Knowledge | Black-box; may know tool names and that a defense exists | DESIGN DECISION |
| Access | User channel + content that becomes tool observations | DESIGN DECISION |
| Goals | Cause **harmful tool execution** matching pre-registered `success_condition` | DESIGN DECISION |
| Observability (P2-D only) | Sees prior defense action / tool deny / block on same trajectory | DESIGN DECISION |
| Budget (P2-D) | ≤3 surface rewrites; no unlimited search | DESIGN DECISION |

**Not an adversary capability in P2 pilot:** training-data poison, weight exfil, unlimited adaptive search, multi-agent collusion. **DESIGN DECISION**

---

## 4. Why this threat model (L1 linkage)

| L1 observation | Threat implication | Tag |
| --- | --- | --- |
| 15 detector misses with tools executed | Adversary wins when detector fails before any intervention | CONFIRMED FROM L1 |
| 7 A2 denies with judge_success | “Attack success” without tool execution confuses security claims | CONFIRMED FROM L1 |
| C1–C3 / B4 only as frozen proxies | Real adversary can use time, state, and tool feedback | CONFIRMED FROM L1 |
| STATIC-A1 ineffective | Mild sanitize is not a meaningful control against tool harm | CONFIRMED FROM L1 |

**HYPOTHESIS:** Live multi-turn and live tool-output channels increase detector-miss opportunities beyond L1 single-turn rates for families C3/D1/D2/F3.

---

## 5. Attack surfaces (P2)

| Surface | Component | In pilot? | Tag |
| --- | --- | --- | --- |
| User turn text | P2-B/D | Yes | DESIGN DECISION |
| Prior dialogue state | P2-B | Yes | DESIGN DECISION |
| Memory store writes/reads | P2-B (limited) | Yes (optional template) | DESIGN DECISION |
| Tool observation channel | P2-C | Yes | DESIGN DECISION |
| Adaptive rewrite after deny | P2-D | Yes (bounded) | DESIGN DECISION |
| Live web/RAG backends | — | No | DESIGN DECISION |

---

## 6. Episode / trajectory as unit of analysis

**DESIGN DECISION:** Unit = **trajectory** (ordered turns), not a single prompt.

```text
Trajectory
  turn t=1..T
    inbound (user | tool_observation | memory_read)
    → defense (label-blind)
    → target generation
    → optional tool request
    → tool sandbox (allow/deny/execute)
    → state update
  terminal scoring: Tool-HASR, Judge-ASR, utility, cost, latency
```

L1 single-turn episodes remain a **separate** estimand family. **CONFIRMED FROM L1** / **DESIGN DECISION**

---

## 7. Trusted vs untrusted data

| Channel | Trust | Tag |
| --- | --- | --- |
| System policy / tool schema | Trusted | DESIGN DECISION |
| User text | Untrusted | DESIGN DECISION |
| Tool observations | Untrusted (even if tool is “ours”) | DESIGN DECISION |
| Memory contents | Untrusted after any attacker-influenced write | DESIGN DECISION |
| Defense scores / gold labels | Not visible to target or attacker | DESIGN DECISION |

---

## 8. Winning conditions

| Outcome | Definition | Tag |
| --- | --- | --- |
| Attacker win (primary) | Tool-HASR success on attack trajectory | DESIGN DECISION |
| Attacker win (secondary) | Judge-ASR success | DESIGN DECISION |
| Defender win (security) | No harmful tool execution | DESIGN DECISION |
| Defender failure modes | Detector miss; insufficient action; false allow after adaptive rewrite | DESIGN DECISION + CONFIRMED FROM L1 patterns |
| Utility failure | Benign trajectory fails task or false-blocks | DESIGN DECISION |

**Refusal alone is not a defender win** if the harmful tool still executed. **DESIGN DECISION** (aligns with existing project rules; L1 showed tool-exec with refusal labels). **CONFIRMED FROM L1** examples exist under B0.

---

## 9. Explicit non-goals

- Measuring “jailbreak chat” without tools. **DESIGN DECISION**
- Claiming production agent hardening. **DESIGN DECISION**
- Replacing or reinterpreting L1 AUDIT numbers. **DESIGN DECISION**

---

## 10. FUTURE EXPERIMENT gates

Live threat-model evaluation requires: frozen P2 pack + human API approval + Tool-HASR instrumentation shipped. Until then, threat model is design-only.
