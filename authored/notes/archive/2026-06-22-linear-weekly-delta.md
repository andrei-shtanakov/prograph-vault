---
title: 'Linear ↔ reality: weekly delta'
type: note
status: archived
owner: Andrei
updated: 2026-06-22
archived: 2026-07-06
reason: Linear tracking frozen — historical
---

# Linear ↔ reality: weekly delta

> Date: 2026-06-22 · Linear team: **Labs** (key `LABS`) · Source of truth: **git + roadmap** (`COWORK_CONTEXT.md`)
> Mode: read-only. Delta window: since the previous report `2026-06-15-linear-weekly-delta.md` (2026-06-15 → 2026-06-22).
> ✅ **Linear was read** — for the first time in 5 runs OAuth was not required, the connected MCP responded.

## TL;DR

1. **The connected Linear MCP returned a practically empty tracker — and this contradicts the reconcile log of 2026-05-25.** The Labs team (workspace `linear.app/atp-platform`) returns **only 4 onboarding stubs** (`LABS-1..4`, all `Todo`, created 2026-04-04), **0 projects**. But memory/audit records that the 2026-05-25 reconcile **created `LABS-107..111` and closed `LABS-87/91/92/93/58`**. They are not in the output (even with `includeArchived=true`). ⚠️ Most likely — **this MCP connector points at a different Linear workspace/account** than the one the reconcile was applied to (`plugin:engineering:linear`). Don't change the substantive conclusion until this is clarified — see §0.
2. **arbiter and Maestro are active again** after zero commits last week: arbiter — 10 commits, Maestro — 9. `atp-platform` continues intensively (~22 commits, R-07). `spec-runner` — **0 commits** in the window.
3. **R-07 advanced in arbiter exactly where the roadmap pointed:** `fbc06aa` (#20) — "benchmark-aware routing Phase 1 (reader + re-rank + A/B)". This is precisely "`BenchmarkResult` as weighting input in DT inference". A clarification to the previous report: R-07 has **two arms** — the eval harness in `atp-platform` (data generation) + the routing consumer in `arbiter` (consumption). Last week's conclusion "R-07 went in a different direction" was incomplete.
4. **A new cross-repo convention `agent_id = <harness>@<model>`** landed in sync across all three cores over the week: `atp-platform` (#200), `arbiter` (#24, `f3c955c`), `Maestro` (#29, `bce7f0f`). A coordinated breaking-ish change of routing keys — **not reflected in the registry/contracts**.
5. **Version drift in `COWORK_CONTEXT.md` unchanged** (carry-over): spec-runner `2.0.0`→actual `2.7.0`, atp-platform `2.0.0`→`2.1.0`, arbiter `0.1.0`→`0.2.0`, the package `atp-method v0.1.0` still not in the map. No new version shifts over the week.

---

## 0. Linear access status — CHANGED

Unlike the 4 previous runs, the connected Linear MCP responded **without a repeat OAuth**. Pulled:

| Query | Result |
|--------|-----------|
| `list_teams(query="Labs")` | 1 team: **Labs** (`3696d35e…`, created 2026-04-04, updated 2026-04-15) |
| `list_projects(team=Labs)` and `list_projects()` | **0 projects** (empty) |
| `list_issues(team=Labs, limit=250, includeArchived=true)` | **4 issues**, all — Linear's default onboarding stubs |

Full list of issues in Labs:

| ID | Title | Status | Created |
|----|-----------|--------|---------|
| LABS-1 | Get familiar with Linear | Todo | 2026-04-04 |
| LABS-2 | Set up your teams | Todo | 2026-04-04 |
| LABS-3 | Connect your tools | Todo | 2026-04-04 |
| LABS-4 | Import your data | Todo | 2026-04-04 |

**⚠️ A contradiction that needs attention:** the audit `_cowork_output/2026-05-25-linear-vs-reality-audit.md` + memory record the reconcile of 2026-05-25, which **created `LABS-107..111`** (R-06b epic+M5, report_benchmark docs, R-07, observability M3) and **closed `LABS-87/91/92/93/58`**. None of these IDs are **present** in the current output (the query was with `includeArchived=true`, `limit=250`, `hasNextPage=false`). Two explanations:

- **(more likely) a different workspace/account.** The reconcile was applied via `plugin:engineering:linear` (OAuth). The current read is via an already-connected MCP connector pointing at `linear.app/atp-platform`. If these are different Linear accounts, then the "empty" tracker is simply not the one that was populated.
- (less likely) the issues were deleted/moved after 2026-05-25.

**Therefore I do NOT conclude "Linear was never populated".** The correct status today: the workspace `atp-platform` *accessible via the current connector* is empty (4 stubs); the tracker populated by the reconcile, if it exists, is in a different connection. The 6 expected projects in **this** workspace are not filed. The source of truth in any case is git + `COWORK_CONTEXT.md`.

---

## 1. Git activity over 7 days (2026-06-15 → 2026-06-22)

| Project | Commits in the window | Gist | Version (fact) |
|--------|:---:|------|------|
| **atp-platform** | ~22 | R-07: CLI/artifact corpus grounding (Path A, ADR-007), Tier-1/Tier-2 roster, code-review structured output + schema gate, ollama spawner, axis-sweep dashboard | v2.1.0 |
| **arbiter** | 10 | **reactivated.** R-07 benchmark-aware routing Phase 1, `<harness>@<model>` ids, ingest sweep-2026-06-21, deterministic tie-break, fix red Rust CI | v0.2.0 |
| **Maestro** | 9 | **reactivated.** Accept `<harness>@<model>` agent ids, pin harness model for R-07, migration of CodexSpawner to `codex exec`, bump arbiter pin `7aeb6b1→f3c955c`, deps | v0.4.0 |
| **spec-runner** | 0 | no activity in the window (the last burst was before 2026-06-15) | v2.7.0 |
| prograph / appgraph / prograph-vault / proctor-a | 0 | no commits | — |

Recognized task tags in the commit messages over the week: `R-07` (atp ×many, arbiter `#20/#26`), `#NN` GitHub PR. **Not a single `LABS-NN`** — which is consistent with the empty Linear.

---

## 2. New discrepancies over the week

### 2.1. KEY — the tracker is empty, all work is outside Linear (structural, not line-by-line)

Since Linear has not a single real issue, the classic "git closed → Linear still open" analysis is inapplicable: **there is nothing to open in Linear**. The correct formulation of the delta — confirmed by reading for the first time: the backlog R-05…R-10, R-06b M1–M5, R-07, LABS-87/88-90/108, observability M1–M3 **was never filed in Linear**. The decision on the tracker (populate vs. formally decommission) is an open question, see §4.

### 2.2. MISSING — notable work in git without an issue (new vs. last week)

| Topic | Where in reality | In Linear | Type |
|------|------------------|----------|-----|
| **R-07 benchmark-aware routing — Phase 1 in arbiter** (reader + re-rank + A/B; ingest `sweep-2026-06-21`; deterministic tie-break) | `arbiter`: `fbc06aa` (#20), `cb71b57` (#26), `e1881c7` (#27) | No | MISSING + closes the roadmap prediction R-07 |
| **Cross-repo convention `agent_id=<harness>@<model>`** (a synchronous breaking-ish shift of routing keys) | `atp-platform` `ccea815` (#200); `arbiter` `f3c955c` (#24) + docs `8b6bfec` (#25); `Maestro` `bce7f0f` (#29) | No | MISSING (no issue + not in contracts/registry) |
| **Maestro ↔ codex CLI 0.139.x: migration to `codex exec`** | `Maestro`: `6e1d4e3` (#33), `385dd90` (#32) | No | MISSING |
| **Maestro vendored-arbiter pin bump** `7aeb6b1 → f3c955c` (provenance-only) | `Maestro`: `b8de57d` (#30) | No | MISSING (the Maestro↔Arbiter contract point was updated) |
| **atp-platform R-07: Tier-2 roster + ADR-007 test-taxonomy + CLI corpus grounding (Path A)** | `atp-platform`: `0fc15b1` (#207), `cc82476` (#204), `6471e5e` (#203) | No | MISSING (a continuation of last week's R-07 line) |

### 2.3. STALE DESCRIPTION — roadmap diverges from the fact

| Where | In the roadmap text | Fact over the week | Type |
|-----|------------------|----------------|-----|
| `COWORK_CONTEXT.md:275` | **R-07** "🟢 unblocked … next: `BenchmarkResult` as weighting input in DT inference" | This "next" is **done** in arbiter `fbc06aa` (#20, Phase 1 re-rank + A/B). The line should move from "unblocked" to "🟡 in progress, Phase 1 ✅". Plus clarify the second arm — the eval harness in atp-platform | STALE DESCRIPTION |
| `COWORK_CONTEXT.md` (Maestro↔Arbiter contract, vendored SHA) | pin `861534e` / mentions of old SHAs | the actual Maestro pin = `f3c955c` (#30, 2026-06-19); the agent_id convention changed to `<harness>@<model>` | STALE DESCRIPTION (contract point) |

### 2.4. Carry-over (not new, no duplicates)

| Where | In the text | Fact | Status |
|-----|----------|------|--------|
| `COWORK_CONTEXT.md:22,85,134,213` | spec-runner `v2.0.0` | `v2.7.0` | carry-over (no movement over the week) |
| `COWORK_CONTEXT.md:19,234` | atp-platform `v2.0.0` | `v2.1.0` | carry-over |
| `COWORK_CONTEXT.md:20,117` | arbiter `v0.1.0` | `v0.2.0` | carry-over |
| ATP map | no `atp-method` package | `atp-method v0.1.0` (the tag exists) | carry-over |
| roadmap `LABS-108` (arbiter docs for `report_benchmark`/protocol 1.1.0) | "⚠ docs not updated yet" | over the week arbiter updated docs (`#23/#25`), but for `<harness>@<model>`, **not** for `report_benchmark` — the gap persists | carry-over |

---

## 3. What did NOT change

- **spec-runner** — 0 commits in the window; the v2.4–v2.7 release train (last week) added no new tags.
- **prograph / appgraph / prograph-vault** — without commits; the governance gap (not in the registry) persists, no decision made.
- **proctor-a** — the pause since 2026-04-16 continues.
- **Versions** atp/spec-runner/arbiter/Maestro — no shift over the week (the registry drift is pure carry-over).

---

## 4. Recommended actions

1. **First resolve the connector contradiction (priority, all_ai_orchestrators):** check **whether the current MCP is looking at the right Linear account**. Open `linear.app` under the working account and verify whether `LABS-107..111` are visible there (created by the reconcile of 2026-05-25). If they are in a different workspace — the scheduled task needs to be reconnected to the correct connector; if they are nowhere — the 2026-05-25 reconcile did not persist, and then the reconciliation has two paths: (a) **bootstrap-populate** the projects/epics again, or (b) **formally decommission Linear** and reconcile "git ↔ roadmap". I don't act blindly until it's clear which tracker is "real".
2. **arbiter / atp-platform (Linear, if path "a" is chosen):** file an epic **R-07** with two arms — `atp eval-harness` (corpus grounding, code-review, taxonomy ADR-007) and `arbiter benchmark-aware routing` (Phase 1 ✅, `fbc06aa`); mark Phase 1 as Done.
3. **COWORK_CONTEXT.md (registry — read-only for me):**
   (a) update the roadmap line **R-07** (`:275`): "Phase 1 (arbiter re-rank + A/B) ✅, atp eval-harness in progress";
   (b) record the new convention **`agent_id=<harness>@<model>`** in the Maestro↔Arbiter contract section and update the vendored pin → `f3c955c`;
   (c) carry over the versions: spec-runner `→2.7.0`, atp `→2.1.0`, arbiter `→0.2.0`; add `atp-method v0.1.0`.
4. **Maestro (registry):** note the spawner migration to `codex exec` (codex CLI 0.139.x) — may affect the integration docs.
5. **Reconcile:** I made **no** edits to Linear or the repositories (read-only). If you choose path "a" (populate Linear) — say "reconcile", and I'll give a proposed set of issues/epics for your confirmation; I write nothing without an explicit OK.

---

> Sources: Linear MCP — `list_teams`, `list_projects` (0), `list_issues(team=Labs)` = LABS-1..4 (onboarding stubs). Git history of the window: `Maestro` (`6e1d4e3`,`385dd90`,`b8de57d`,`bce7f0f`,`80af41f`), `arbiter` (`fbc06aa`,`cb71b57`,`f3c955c`,`8b6bfec`,`e1881c7`,`307cfca`), `atp-platform` (`0fc15b1`,`cc82476`,`6471e5e`,`ccea815`,`c31c413`). Versions: `arbiter/Cargo.toml=0.2.0`, `atp-platform/pyproject.toml=2.1.0`, `spec-runner/pyproject.toml=2.7.0`, `Maestro/pyproject.toml=0.4.0`. Registry: `COWORK_CONTEXT.md:19,20,22,85,117,134,213,234,275`. Baseline: `_cowork_output/2026-06-15-linear-weekly-delta.md`.
