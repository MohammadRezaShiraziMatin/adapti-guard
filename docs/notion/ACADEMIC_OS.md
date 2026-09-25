# Academic OS (Notion)

Notion workspace provisioning for PhD applications, research, learning, and tasks.

## Prerequisites

1. Create a [Notion integration](https://www.notion.so/my-integrations).
2. Share the parent page with the integration (••• → Connections).
3. Set environment variables:
   - `NOTION_API_KEY` — integration secret
   - `NOTION_PARENT_PAGE_ID` — optional parent page ID or URL (required on first run if the integration has no searchable parent)

## Provision

```bash
cd scripts/notion
python3 setup_academic_os.py
```

Idempotent state is stored in `scripts/notion/.academic_os_state.json` (local only).

## Validate

```bash
cd scripts/notion
python3 validate_academic_os.py
```

## Layout

- **🏠 Academic OS** — dashboard with linked database views (no duplicate data stores).
- **15 source databases** — child pages under the root; relations connect universities → professors → positions → applications → documents, and research projects → questions → experiments → papers/concepts.

Initial seeded rows: research projects `ADAPTI-GUARD`, `Agent Injection Bench`; concept stubs for the AI Security learning list (titles only, no fabricated content).
