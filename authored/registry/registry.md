---
title: Ecosystem project registry + integration map
type: registry
status: living
owner: Andrei
updated: 2026-07-18
---

# Ecosystem registry — AI Orchestrators

The project registry (COWORK_CONTEXT) and cross-repo integration map. **Human-curated overview**;
machine-detected structure is owned by prograph (`../../derived/graph/`, `../../derived/projects/`) —
this doc references it, it is not the authority for edges/contracts.

> Snapshot basis: workspace docs refresh 2026-07-18 after the Libretto/Maestro rename pass,
> github-checker `propose-pr`, dispatcher config-editor slices, and prograph M12 declared edges.
> Older narrative remains in
> [`../notes/status/2026-07-08-1228-status.md`](../notes/status/2026-07-08-1228-status.md),
> [`../notes/ecosystem-roadmap.md`](../notes/ecosystem-roadmap.md), and
> [`../notes/status/2026-07-08-logging-audit.md`](../notes/status/2026-07-08-logging-audit.md).

## Projects (tracked ecosystem repos)

| Repo | Lang | Role | Status |
|---|---|---|---|
| **ai-orchestrators-workspace** | toml/bash | Team umbrella: `workspace-manifest.toml` is the SSOT for repo set + pins; bootstrap and manifest-drift CI. | 🟢 active |
| **atp-platform** | python | Agent-evaluation platform (core, 11 sub-packages). Source of contracts: `report_benchmark-v1`, `observability-contract/v1`, `agent-eval-case`. | 🟢 dominant core |
| **proctor** | python | Distributed autonomous agent runner (microkernel; NATS / Docker workers / DAG). Repo/dir `proctor`, obs service-id `proctor-a` (ADR 2026-07-07). | 🟢 most active new |
| **spec-runner** | python | Task/spec execution backend (v2.10.0). Owns spec-runner schemas + the canonical `obs.py` emitter. | 🟢 active |
| **maestro** | python | Maestro DAG orchestrator (v0.4.0). MCP client to arbiter; CLI backend = spec-runner `plan --full`. Repo/path lowercased 2026-07-16; product name remains `Maestro`. | 🟢 active |
| **arbiter** | rust (mixed) | MCP policy/routing engine; agent catalog; benchmark-evidence gate. Announces MCP proto `1.1.0`. | 🟢 active |
| **dispatcher** | python | Ecosystem dashboard/control plane: sync read-model via github-checker, guarded `pull`/PR actions, spec-runner config editor via PR-only propose-pr. | 🟢 stabilizing |
| **github-checker** | python | Git/GitHub fleet utility: TUI, `snapshot --workspace` with vendored schema v1, whitelist actions, and `propose-pr --edit` for isolated PR creation. | 🟢 active support tool |
| **deployer** | python | Deploy-authoring research bench: facts + `deploy_target` → Dockerfile authoring, deterministic static/Docker verification, authoring-vs-execution separation. | 🟡 young |
| **spec-runner-vscode** | js | VSCode thin client over dispatcher/spec-runner action/read contracts. | 🟡 thin client |
| **prograph** | rust (mixed) | Cross-project structure mapper. M12 declared file edges; produces this KB's `derived/`. | 🟢 active tooling |
| **prograph-vault** | docs | **This KB** (Ecosystem KB). | 🟢 new |
| **robin-toolkit** | docs | Team-knowledge toolkit (derivative of Team OS). | 🟡 new |
| **steward** | python | Spec governance layer above spec-runner/Maestro. Shipped bootstrap tools: `gate-check`, `steward-compile`, risk classifier. | 🟡 active bootstrap |
| **robin-runtime** | python | Robin (AI chief of staff) runtime. KB-grounded answer plus Telegram/web/voice contours; reads KB/repos read-only. | 🟡 bootstrap runtime |
| **libretto** | docs/python | Language for AI sessions (spec-as-VM) plus deterministic verification tooling. Renamed from `open-prose` on 2026-07-16; canonical repo/path `libretto`, legacy `openprose.*` artifacts remain readable. | 🟢 active |
| **discovery-toolkit** | docs/python | Discovery/elicitation skill bundle + `discovery-brief` contract/gate-checker; upstream of governance. | 🟢 active |
| **discovery** | python | Runtime scaffold for discovery interviews and brief authoring; implementation still placeholder. | 🔴 scaffold |
| **devtools** | bash/python | Workspace fleet tooling and drift/conformance checks. | 🟢 active support tool |
| **sdd-framework** | markdown | Spec-driven development methodology for data pipelines. | 🟡 methodology |

## Integration map (verified via prograph edges)

**Package dependencies**
- `maestro → atp-platform-sdk (atp-sdk) >=2.0.0` (actual 2.0.0 — aligned).
- `arbiter → spec-runner >=0.1.1` ⚠️ and `atp-platform → spec-runner >=0.1.4` ⚠️ — **stale pins** (real spec-runner is 2.10.0).
- arbiter internal: `arbiter-cli → arbiter-core`, `arbiter-cli → arbiter-mcp`, `arbiter-mcp → arbiter-core`.
- atp-platform internal sub-package graph (atp-core, atp-sdk, atp-adapters, atp-method, atp-dashboard, atp-games, game-environments).

**Runtime / protocol**
- `maestro → spec-runner` via `plan --full` CLI — versioned (`SPEC_RUNNER_REQUIRED_VERSION` in `maestro/spec_runner.py`) + contract tests. ✅
- `maestro → arbiter` via MCP — handshake `protocolVersion 1.1.0`, `MIN_ARBITER_PROTOCOL (1,1)`. ✅
- `atp-platform → atp-dashboard` MCP calls (`make_move`, `get_current_state`).
- `dispatcher → github-checker` via `snapshot`, `pull`, `open-pr`, and `propose-pr --edit` subprocess contracts. ✅
- `prograph → prograph-vault/derived` via declared write/export path. ✅

**Shared contracts** (single content-hash each — no drift; authority in producing repo)
- `report_benchmark-v1` — owners: Maestro, arbiter, arbiter-mcp, atp-platform, method.
- `observability-contract/v1` (log-schema) — owners: Maestro, arbiter, arbiter-core; emitter `obs.py`/`obs.rs`; consumer: dispatcher.
- spec-runner schemas (`costs`, `json-result`, `spec-frontmatter`, `status`) — spec-runner + spec-runner-vscode.
- `agent-eval-case` — method + atp-platform.

**Likely sparse/intent-only graph coverage until the next full prograph export:**
robin-runtime, robin-toolkit, deployer, libretto, steward, discovery. Some are
methodology/spec/tooling repos by design; file-based edges should now be declared
in manifests instead of maintained only in this registry.

## Known cross-cutting misalignments (pointers, not authority)

These are tracked in the status/roadmap notes; listed here so the registry stays honest:

1. **spec-runner version-pin skew** — consumers pin `>=0.1.x` vs real 2.10.0. → roadmap P1.
2. **`obs.py` vendoring drift** — 3 divergent copies; proctor & atp-platform not on the obs contract. → [logging-audit](../notes/status/2026-07-08-logging-audit.md).
3. **proctor ↔ Maestro role overlap** — both do DAG orchestration; boundary undecided. → roadmap P2.
4. **`arbiter-mcp` protocolVersion `"1.1.0"`** is not MCP's date-string format. → roadmap P4.
5. **steward** has shipped local governance tooling; Maestro/spec-runner delegation edges still need graph/contract evidence.

## Maintenance

Refresh on the kb-curator freshness audit (or when repos change). Structure/edges: re-run prograph
(`derived/graph/`). This file records the human-facing map + status; it defers to derived/ for
machine facts and to producing repos for contract authority.
