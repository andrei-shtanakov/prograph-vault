---
title: 'Linear ↔ reality: weekly delta'
type: note
status: archived
owner: Andrei
updated: 2026-07-06
archived: 2026-07-06
reason: Linear tracking frozen — historical
---

# Linear ↔ reality: weekly delta

> Date: 2026-07-06 · Linear team: **Labs** (key `LABS`) · Source of truth: **git + roadmap** (`COWORK_CONTEXT.md`)
> Mode: read-only. Delta window: since the previous report `2026-06-22-linear-weekly-delta.md` (**the 06-29 run was skipped → 2-week window: 2026-06-22 → 2026-07-06**).
> ⚠️ **Linear was NOT read in this run** — the connector `plugin:engineering:linear` requires a repeat OAuth authorization, and the session is background/non-interactive. See §0.

## TL;DR

1. **Linear requires re-authorization — open the app and reconnect `plugin:engineering:linear`.** The tracker could not be read in this run. But per the 06-22 report, the connected workspace `atp-platform` was empty anyway (only onboarding stubs `LABS-1..4`, 0 projects), so the substantive delta is computed along the **git ↔ roadmap** axis regardless.
2. **R-06b M5 is CLOSED in code, but the roadmap still says "pending".** Maestro `2857ee7` (#45) "feat(cli): maestro benchmark — R-06b M5". `COWORK_CONTEXT.md:304` keeps `R-06b M5 (CLI) 🟡 pending` → a **STATUS discrepancy**, requires a roadmap edit.
3. **The dominant theme of the two weeks is the `ADR-ECO-003 (a/b/c)` epic: catalog-driven agent roster + `opencode@glm-5.1` as the first open model in routing.** It landed in sync across all three cores (atp-platform, arbiter, Maestro). **Completely absent from the roadmap snapshot** (it is dated 2026-05-23 and was intentionally not updated in the 07-05 freshness audit).
4. **An explosion of activity in the auxiliary projects:** proctor-a (TaskRouter M4 shipped + Phase 3 worker-registry/NATS dispatch), deployer (4 PRs: MVP→Facts v2→verify-timeouts→CLI-hardening), dispatcher (Stage 2 TUI + Stage 3 VSCode extension), steward (bootstrap, first commit), spec-runner (v2.8.0/2.8.1, gated spec generation). Not a single `LABS-NN` in the commits — Linear remains out of the loop.
5. **A positive since last time:** the 07-05 registry freshness audit closed the governance gap — deployer/dispatcher/sdd-framework/steward/ecosystem-kb were entered into the registry, the false "pause" label removed from proctor-a. But **the version drift and the roadmap snapshot remained untouched** (see §2.3).

---

## 0. Linear access status — NOT READ (re-authorization needed)

| What | Result |
|-----|-----------|
| Connection `plugin:engineering:linear` | requires a repeat OAuth; cannot be completed in a background run |
| `list_teams` / `list_projects` / `list_issues` | not performed |

User action: open Claude → connector settings (or an interactive session) and reconnect Linear. Until then the reconciliation runs only on git + `COWORK_CONTEXT.md`.

A reminder from the 06-22 report (unchanged, but not confirmed in this run): the workspace `linear.app/atp-platform` accessible to the connector contained only `LABS-1..4` (onboarding stubs, `Todo`), 0 projects. The open question "populate Linear again vs. formally decommission" remains unresolved.

---

## 1. Git activity over the window (2026-06-22 → 2026-07-06)

Practically all the work is concentrated in the last week (the slice 06-22→06-29 is empty across all cores).

| Project | Commits (7d) | Gist | Version (fact) |
|--------|:---:|------|------|
| **atp-platform** | ~22 | ADR-ECO-003 roster (#211), **opencode@glm-5.1 → routable** (#223), retired dead keys (#214/#2b7ce32), golden-suite lock (#215), Path A CLI corpus grounding (claude_code/codex_cli/opencode/pi #227-230), severity ladder (#231), R-07 rank_score+bp_ordinal (#210) | v2.1.0 |
| **arbiter** | 14 | **routable-flip benchmark-evidence gate** (ADR-ECO-003a D4, #41), user-config catalog loader+CLI (#39), promote opencode@glm-5.1 (#38), vendor SSOT sync (#37), R-07 consume rank_score tiebreaker (#30) + rerank flips code-review→codex (#33) | v0.2.0 |
| **Maestro** | 12 | **maestro benchmark — R-06b M5** (#45), maestro models init/list/discover/update (ADR-ECO-003b D3, #44), opencode cost-from-log (#43), wire opencode spawner (ADR-ECO-003c, #42), maestro init+validate (#41), catalog-driven model defaults (#38), open AgentType gate (#35) | v0.4.0 |
| **spec-runner** | ~12 | **release v2.8.0 → v2.8.1**, gated spec generation (#28), VSCode read-surface contracts (#30), C1 stages-profile gated spec | v2.8.1 |
| **proctor-a** | ~40 | **TaskRouter M4 shipped** ("Phase 2 complete", #28), Phase 3: WorkerRegistry + NATS remote dispatch + reaper/fencing (#30), docs sync | v0.1.0 |
| **deployer** | ~50 | MVP loop (#1) → Facts v2 sysdep hints (#2) → verify timeouts (#3) → CLI hardening (#4). Active research bench | v0.1.0 |
| **dispatcher** | ~55 | Stage 2 Textual TUI (4 tabs) + Stage 3 **VSCode extension** (scaffold→trees→CI) | v0.1.0 |
| **steward** | 1 | `aa83867 first commit` — bootstrap spec-governance-layer (ADR 07-05) | v0.1.0 |

Recognized tags in the commits: `R-06b M5`, `R-07`, the series `ADR-ECO-003a/b/c`, `#NN` (GitHub PR). **`LABS-NN` — zero**, which is consistent with the unavailable/empty Linear.

---

## 2. New discrepancies over the window

### 2.1. STATUS — closed in git, but the roadmap still says "pending"

| Topic | Where in git | In the roadmap | Type |
|------|-----------|-----------|-----|
| **R-06b M5 (CLI `maestro benchmark <id> --agent ...`)** | Maestro `2857ee7` (#45) | `COWORK_CONTEXT.md:304` and `:235` = "🟡 pending" | **STATUS** (closed → time for ✅) |

### 2.2. MISSING — notable work with no issue and outside the roadmap

| Topic | Where in reality | In Linear / roadmap | Type |
|------|------------------|--------------------|-----|
| **Epic ADR-ECO-003 (a/b/c): catalog-driven agent roster** (SSOT `atp-platform/method/agents-catalog.toml`) | atp `#211/#214/#215`; arbiter `#37/#39`; Maestro `#38` | No / absent from the 05-23 snapshot | MISSING (the largest epic of the window) |
| **`opencode@glm-5.1` — the first open model in routing** (routable) | atp `690428a` (#223); arbiter `f11bb17` (#38); Maestro `ae72a8b` (#42, spawner) | No | MISSING (an expansion of the routing roster) |
| **Routable-flip benchmark-evidence gate** (ADR-ECO-003a D4 — model promotion only on benchmark evidence) | arbiter `6a1fbb2` (#41) | No | MISSING (a new gate policy) |
| **Model lifecycle: `maestro models` CLI (init/list/discover/update)** — discovery(auto)→benchmark-gated adoption | Maestro `b2216a1` (#44, ADR-ECO-003b D3) | No | MISSING (implements memory `idea-model-lifecycle-adr-003a`) |
| **spec-runner: gated spec generation + v2.8.x** | spec-runner `592528f` (#28), `85278a7` (v2.8.1) | No | MISSING |
| **proctor-a: TaskRouter M4 + Phase 3 worker-registry/NATS dispatch** | proctor-a `8806953`, PR #28/#30 | No | MISSING (a major step, the roadmap map shows only "M4 in progress") |
| **deployer / dispatcher / steward — active development** | deployer PR#1-4; dispatcher Stage 2-3; steward bootstrap | No (entered into the registry 07-05, but not into the roadmap/Linear) | MISSING |

### 2.3. STALE DESCRIPTION — roadmap/registry diverge from the fact

| Where | In the text | Fact | Type |
|-----|----------|------|-----|
| `COWORK_CONTEXT.md:293` (Roadmap snapshot) | dated **2026-05-23**, deliberately untouched in the 07-05 audit | Lags ~6 weeks behind: no ADR-ECO-003 epic, opencode-routing, model-lifecycle, R-06b M5, R-07 progress | **STALE** (the whole snapshot) |
| `COWORK_CONTEXT.md:304` | `R-06b M5 (CLI) 🟡 pending` | Shipped (Maestro #45) | STALE |
| `COWORK_CONTEXT.md:305` | `R-07 🟢 unblocked … next: BenchmarkResult as weighting` | In progress: rank_score+bp_ordinal is emitted (atp #210) and **consumed** in arbiter (#30), rerank flips code-review→codex (#33) | STALE (time for "in progress") |
| Version table `COWORK_CONTEXT.md:26-29` | atp `2.0.0`, arbiter `0.1.0`, spec-runner `2.0.0`, Maestro `0.4.0` | atp `2.1.0`, arbiter `0.2.0`, spec-runner `2.8.1`, Maestro `0.4.0` | STALE (the registry was edited 07-05, the versions not synced) |
| Maestro↔Arbiter integration map (`:211-213`) | pin `861534e`, old agent_id | The convention `agent_id=<harness>@<model>` + catalog-SSOT; the 07-05 freshness audit explicitly **did not** touch the integration map | STALE (a contract point, carry-over from 06-22) |

### 2.4. Carry-over (not new, no duplicates)

| Where | In the text | Fact | Status |
|-----|----------|------|--------|
| `COWORK_CONTEXT.md:309` | arbiter `report_benchmark`/protocol 1.1.0 docs "⚠ not updated yet" | over the window arbiter updated docs, but for catalog/ADR-ECO-003, **not** for report_benchmark — the gap persists | carry-over |
| Open Linear question (populate vs. decommission) | — | Not resolved; in this run it was also not even read | carry-over |
| overlap triad dispatcher ↔ prograph ↔ appgraph ↔ Maestro | — | Not sorted out | carry-over |

---

## 3. What did NOT change / positive shifts

- **Positive:** the 07-05 registry freshness audit closed the previous governance gap — deployer/dispatcher/sdd-framework/steward/ecosystem-kb entered into the registry; the false "pause" on proctor-a removed. The previous 06-22 notes about "projects outside the registry" are **cleared at the registry level** (but not at the roadmap/Linear level).
- **Unchanged:** the roadmap snapshot (05-23) and the integration map — stale; the version table in the registry — out of sync; Linear — out of the loop.

---

## 4. Recommended actions

1. **Linear (priority, all_ai_orchestrators):** reconnect the connector `plugin:engineering:linear` in an interactive session/settings — otherwise reconciling the tracker is impossible. After that, resolve the old open question: populate Labs again or formally decommission it (reconcile "git ↔ roadmap").
2. **COWORK_CONTEXT.md — roadmap (registry read-only for me):**
   (a) `:304`/`:235` — move **R-06b M5** to `✅ closed` (Maestro #45);
   (b) `:305` — **R-07** → "🟡 in progress": rank_score tiebreaker is emitted (atp #210) and consumed in arbiter (#30/#33);
   (c) add a **new epic ADR-ECO-003 (a/b/c)** to the roadmap: catalog-driven roster + opencode routable + benchmark-evidence gate + model-lifecycle CLI;
   (d) sync the version table (`:26-29`): atp `→2.1.0`, arbiter `→0.2.0`, spec-runner `→2.8.1`.
3. **Integration map (COWORK_CONTEXT.md, a separate pass):** update the Maestro↔Arbiter section — record `agent_id=<harness>@<model>`, the catalog-SSOT (`atp-platform/method/agents-catalog.toml`) and the current vendored pin; the 07-05 audit deliberately skipped it.
4. **proctor-a / deployer / dispatcher / steward:** active projects with no reflection in roadmap/Linear — if "populate Linear" is chosen, file epics for them; add progress lines to the roadmap (proctor-a Phase 3, deployer research bench, dispatcher Stage 3 VSCode, steward bootstrap).
5. **Reconcile:** I made **no** edits to Linear or the repositories (read-only; Linear is also unavailable). If, after reconnecting, you choose to populate Linear — say "reconcile", and I'll prepare a proposed set of issues/epics for your confirmation.

---

> Sources — git history of the window: Maestro (`2857ee7`,`b2216a1`,`042fc22`,`ae72a8b`,`7277700`,`048a530`,`745f012`), arbiter (`6a1fbb2`,`6a966a0`,`f11bb17`,`4f242a0`,`3c307ad`,`eec1879`), atp-platform (`a6cdac9`,`690428a`,`2b7ce32`,`f8c99f5`,`c912532`,`8aba0e5`,`227-231`), spec-runner (`592528f`,`0566b1b`,`85278a7`), proctor-a (`8806953`,`09d5fba`,`e93d92e`), deployer (PR#1-4), dispatcher (Stage 2-3), steward (`aa83867`). Versions: `arbiter/Cargo.toml=0.2.0`, `atp-platform/pyproject.toml=2.1.0`, `spec-runner/pyproject.toml=2.8.1`, `Maestro/pyproject.toml=0.4.0`. Registry/roadmap: `COWORK_CONTEXT.md:26-29,235,293,304,305,309,211-213`. Linear: NOT read (re-auth). Baseline: `_cowork_output/2026-06-22-linear-weekly-delta.md`.
