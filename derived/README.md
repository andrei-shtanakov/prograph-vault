---
title: derived/ — guardrail
type: rule
status: living
owner: prograph (auto)
updated: 2026-07-14
---

# derived/ — written by TOOLS

> ⚠️ **Do not edit by hand.** The contents are overwritten by tools. Manual edits will be lost. If you
> want to record knowledge — it goes in `../authored/`.

## Subfolders

| Folder | Written by | What |
|---|---|---|
| `graph/` | prograph | project structure: deps, contracts, MCP calls |
| `contracts/` | prograph / vendor scripts | contract **snapshots** for search (NOT authority — that is in the producing repo) |
| `projects/` | prograph | auto-facts per repo |
| `journal/` | kb-save skill | per-project activity log — **append-only, NOT regenerable** (the one exception; see ADR 2026-07-06) |
| `fleet/` | fleet agent (`devtools/fleet_report.py`) | dated fleet-state reports — **append-only, NOT regenerable**; delivered by PR only (ADR 2026-07-10-fleet-agent-role) |
| `snapshots/` | dispatcher publisher (`dispatcher publish-snapshot`) | `<host>.json` — per-host workspace sync snapshots (github-checker snapshot contract **v1**, `schema_version: 1`); one file per host, overwritten in place (latest state only, no history); scheduled (cron/launchd ≤ 1 h per machine); consumer: dispatcher sync verdict engine (Gate 1 Design DESIGN-203) |
| `digests/` | digest skills | claude-kb digests |

## Rules

- A tool writes **only** to its own `derived/` subfolder; writing to `../authored/` is forbidden.
- A contract snapshot is tagged with the source and the hash/version of the original (traceability to the owner).
- `derived/` is regenerated — do not store anything here that cannot be reproduced from the sources.
  **Exceptions:** `journal/` and `fleet/` are append-only narrative (kb-save / fleet agent); prograph
  must not touch them. Curation/archival is by `kb-curator`.
- `snapshots/<host>.json` follows the frozen github-checker snapshot contract v1
  (authority: `github-checker/contracts/snapshot/v1/`); a consumer must check `schema_version`.
  Staleness is data, not an error: consumers surface the file's `generated_at` age (a stale host
  must render as `stale`/`unknown`, never as "ok").
