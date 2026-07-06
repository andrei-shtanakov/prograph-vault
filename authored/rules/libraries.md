---
title: Library choices (cross-cutting)
type: rule
status: accepted
owner: Andrei
updated: 2026-07-05
---

# Library choice rules (cross-cutting)

> The ecosystem's canonical stack (scan 2026-07-05). Deviation — only with a justification note in
> the repo's CLAUDE.md. Goal — a single set so knowledge/patterns carry across repos.

## Canon by role

| Role | Library | Note |
|---|---|---|
| CLI | **typer** (`>=0.12`) | dominant; `click` — only if typer clearly can't handle it |
| Models/validation | **pydantic** | boundaries, configs, schemas |
| Logs | **structlog** via `get_logger()` | not `logging.getLogger` directly |
| Async | **anyio** | structured concurrency; asyncio acceptable |
| HTTP service | **fastapi** | REST/dashboards |
| MCP server | **fastmcp** | MCP endpoints |
| TUI | **textual** (interactive) / **rich** (output) | see `tui.md` |
| Async SQLite | **aiosqlite** | state stores (spec-runner state) |
| YAML/configs/frontmatter | **pyyaml** | `safe_load` |
| Tests | **pytest** | `@pytest.mark.slow` for e2e |
| Env/deps | **uv** | not pip in prod |

## Rust

- `arbiter`, `prograph` — Rust (Cargo). Rust↔Python contracts — via pinned schemas
  (JSON-schema/serde), not ad-hoc.

## Rules

- **Pin versions** in `pyproject.toml` (a range with an upper bound for majors, like `typer>=0.12,<1`).
- **Do not add a new library** if canon covers the task. New = a note in the repo's CLAUDE.md +
  (if reusable) an update to this file via PR.
- **Cross-repo contracts** on boundary libraries (pydantic state models) — are vendored as a pinned
  copy (see `code-style.md`).
- ⚠️ *Current inconsistency:* several typer versions (`0.12`/`0.21`/`0.24`) — bring to a common lower
  bound on the next touch.

## Enforcement

`gate-check`/CI can check `pyproject.toml` against canon (Stage 3). prograph catches stack drift.
