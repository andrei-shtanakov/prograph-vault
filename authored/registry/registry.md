---
title: Ecosystem project registry + integration map
type: registry
status: living
owner: Andrei
updated: 2026-07-16
---

# Ecosystem registry — AI Orchestrators

The project registry (COWORK_CONTEXT) and cross-repo integration map. **Human-curated overview**;
machine-detected structure is owned by prograph (`../../derived/graph/`, `../../derived/projects/`) —
this doc references it, it is not the authority for edges/contracts.

> Snapshot basis: prograph index 2026-07-08 + `git` state of each repo. Detailed narrative lives in
> [`../notes/status/2026-07-08-1228-status.md`](../notes/status/2026-07-08-1228-status.md),
> [`../notes/ecosystem-roadmap.md`](../notes/ecosystem-roadmap.md), and
> [`../notes/status/2026-07-08-logging-audit.md`](../notes/status/2026-07-08-logging-audit.md).

## Projects (14 top-level repos)

| Repo | Lang | Role | Status |
|---|---|---|---|
| **atp-platform** | python | Agent-evaluation platform (core, 11 sub-packages). Source of contracts: `report_benchmark-v1`, `observability-contract/v1`, `agent-eval-case`. | 🟢 dominant core |
| **proctor** | python | Distributed autonomous agent runner (microkernel; NATS / Docker workers / DAG). Repo/dir `proctor`, obs service-id `proctor-a` (ADR 2026-07-07). | 🟢 most active new |
| **spec-runner** | python | Task/spec execution backend (v2.9.0). Owns spec-runner schemas + the canonical `obs.py` emitter. | 🟢 active |
| **maestro** | python | Maestro DAG orchestrator (v0.4.0). MCP client to arbiter; CLI backend = spec-runner `plan --full`. Repo/path lowercased 2026-07-16; product name remains `Maestro`. | 🟢 active |
| **arbiter** | rust (mixed) | MCP policy/routing engine; agent catalog; benchmark-evidence gate. Announces MCP proto `1.1.0`. | 🟢 active |
| **dispatcher** | python | Read-only monitoring dashboard; consumes obs `.jsonl`. | 🟢 stabilizing |
| **deployer** | python | Deploy-authoring agent bench. | 🟡 young |
| **spec-runner-vscode** | js | VSCode thin client over spec-runner. | 🟡 thin client |
| **prograph** | rust (mixed) | Cross-project structure mapper. Produces this KB's `derived/`. | 🟢 new tooling |
| **prograph-vault** | docs | **This KB** (Ecosystem KB). | 🟢 new |
| **robin-toolkit** | docs | Team-knowledge toolkit (derivative of Team OS). | 🟡 new |
| **steward** | python | Spec governance layer (DRAFT spec). Declared "above spec-runner/Maestro" but not yet wired. | 🟡 intent-only |
| **robin-runtime** | python | Robin (AI chief of staff) runtime. M0 scaffold. | 🔴 nascent |
| **libretto** | docs/python | Language for AI sessions (spec-as-VM) plus deterministic verification tooling. Renamed from `open-prose` on 2026-07-16; canonical repo/path `libretto`, legacy `openprose.*` artifacts remain readable. | 🟢 active |

> Removed since earlier snapshots: `github-checker` (role absorbed by prograph + dispatcher).

## Integration map (verified via prograph edges)

**Package dependencies**
- `maestro → atp-platform-sdk (atp-sdk) >=2.0.0` (actual 2.0.0 — aligned).
- `arbiter → spec-runner >=0.1.1` ⚠️ and `atp-platform → spec-runner >=0.1.4` ⚠️ — **stale pins** (real spec-runner is 2.9.0).
- arbiter internal: `arbiter-cli → arbiter-core`, `arbiter-cli → arbiter-mcp`, `arbiter-mcp → arbiter-core`.
- atp-platform internal sub-package graph (atp-core, atp-sdk, atp-adapters, atp-method, atp-dashboard, atp-games, game-environments).

**Runtime / protocol**
- `maestro → spec-runner` via `plan --full` CLI — versioned (`SPEC_RUNNER_REQUIRED_VERSION` in `maestro/spec_runner.py`) + contract tests. ✅
- `maestro → arbiter` via MCP — handshake `protocolVersion 1.1.0`, `MIN_ARBITER_PROTOCOL (1,1)`. ✅
- `atp-platform → atp-dashboard` MCP calls (`make_move`, `get_current_state`).

**Shared contracts** (single content-hash each — no drift; authority in producing repo)
- `report_benchmark-v1` — owners: Maestro, arbiter, arbiter-mcp, atp-platform, method.
- `observability-contract/v1` (log-schema) — owners: Maestro, arbiter, arbiter-core; emitter `obs.py`/`obs.rs`; consumer: dispatcher.
- spec-runner schemas (`costs`, `json-result`, `spec-frontmatter`, `status`) — spec-runner + spec-runner-vscode.
- `agent-eval-case` — method + atp-platform.

**Not yet connected (0 graph edges):** robin-runtime, robin-toolkit, prograph, prograph-vault, deployer, libretto, steward. (Normal for the KB/tooling and read-only dispatcher; intent-only for steward; libretto is a spec/tooling repo whose downstream contract migration is tracked separately.)

## Known cross-cutting misalignments (pointers, not authority)

These are tracked in the status/roadmap notes; listed here so the registry stays honest:

1. **spec-runner version-pin skew** — consumers pin `>=0.1.x` vs real 2.9.0. → roadmap P1.
2. **`obs.py` vendoring drift** — 3 divergent copies; proctor & atp-platform not on the obs contract. → [logging-audit](../notes/status/2026-07-08-logging-audit.md).
3. **proctor ↔ Maestro role overlap** — both do DAG orchestration; boundary undecided. → roadmap P2.
4. **`arbiter-mcp` protocolVersion `"1.1.0"`** is not MCP's date-string format. → roadmap P4.
5. **steward** declared but not wired into the graph.

## Maintenance

Refresh on the kb-curator freshness audit (or when repos change). Structure/edges: re-run prograph
(`derived/graph/`). This file records the human-facing map + status; it defers to derived/ for
machine facts and to producing repos for contract authority.
