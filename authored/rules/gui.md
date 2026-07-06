---
title: GUI / web rules (cross-cutting)
type: rule
status: accepted
owner: Andrei
updated: 2026-07-05
---

# GUI / web rules (cross-cutting)

> Applies to web interfaces and HTTP/MCP surfaces (prograph browser UI, Maestro dashboard,
> MCP servers). Stack: **fastapi** (HTTP) + **fastmcp** (MCP). No heavy frontend framework is
> mandated in the ecosystem.

## Tool choice

- **HTTP API / dashboard** → **fastapi**. Server-rendered (Jinja2 templates, like Maestro dashboard v2)
  is preferred over SPA until there is a clear need for client-side state.
- **MCP endpoint for agents** → **fastmcp**.
- Serve the same domain to both humans (UI) and agents (MCP) — but through **separate adapters over a
  shared read-model** (like prograph: the graph in browser UI and in MCP).

## Architecture

- **Presentation is thin.** No business logic in the router/template — only over a service/core.
- **API contracts are schemas**, not ad-hoc JSON: JSON-schema/pydantic models (see
  `spec-runner/schemas/*.json`, `maestro/schemas/*.json`). The schema is part of the contract (see
  vendoring in `code-style.md`).
- Separate the read-model (queries) from actions (commands); for reads — cacheability.

## Rules

- **No secrets in code/templates** — env/secret manager.
- Errors — typed, with codes; do not expose tracebacks in the UI.
- Static assets and templates — separate from logic; extract inline HTML/JS into templates (like the
  Maestro dashboard refactor).
- For machine integration there is always a `--format json` / JSON endpoint alongside the
  human-readable one.

## Enforcement

API schemas are versioned as contracts; a contract test/prograph catches schema-vs-consumer drift.
