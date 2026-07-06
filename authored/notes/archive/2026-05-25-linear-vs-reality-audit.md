---
title: 'Audit: Linear vs. the actual state of the ecosystem'
type: note
status: archived
owner: Andrei
updated: 2026-05-25
archived: 2026-07-06
reason: Linear tracking frozen — historical
---

# Audit: Linear vs. the actual state of the ecosystem

> Date: 2026-05-25 · Linear team: **Labs** (key `LABS`) · Source of truth: **git + roadmap** (`COWORK_CONTEXT.md`)
> Mode: read-only. Nothing was changed in Linear — this is an audit, not a sync.

## TL;DR

1. **Linear is "frozen" at roughly 2026-04-17.** For practically all open tasks, `updatedAt` = April 15–17. Since then, ~5 weeks of work have been closed in git (R-05, R-06a, R-06b M1–M4, R-10, arbiter#9, LABS-87, observability M2, protocol 1.1.0) — and almost none of it is reflected in Linear.
2. **At least 6 tasks with status `Backlog`/`Todo` are actually done** (there is a commit, and the roadmap marks them as closed). The clearest ones: `LABS-87`, `LABS-91`, `LABS-92`, `LABS-93`, `LABS-58`.
3. **A large body of work was never filed in Linear at all.** The entire Maestro↔ATP benchmarking line (**R-06b M1–M5**), arbiter `report_benchmark` + protocol **1.1.0** + the `benchmark_runs` table, **R-07** (eval-driven routing), observability **M2/M3** — not a single issue.
4. **Stale titles/descriptions:** `LABS-79` ("in progress, 7/32" — actually Done 32/32), `LABS-57` ("not implemented" — Done), `LABS-55` ("4 projects in Linear" — now 6), `LABS-56` (references COWORK_CONTEXT "2026-04-05", now 2026-05-23).
5. **Bonus — the drift is not only in Linear:** `COWORK_CONTEXT.md` itself writes spec-runner **v2.0.0**, while git already has release **v2.1.0** (`29d7f50`, 2026-05-23). The premise of task `LABS-56` (registry ≠ reality) is still alive, just with new details.

---

## 1. Statuses: tasks open in Linear but actually done

Cross-checked against commits in the repositories and the roadmap table in `COWORK_CONTEXT.md`.

| Linear | Project | Status in Linear | Fact (evidence) | Verdict |
|--------|--------|-----------------|-----------------|---------|
| **LABS-87** — Validation-failure path skips arbiter outcome reporting | Maestro | `Backlog` (High, `completedAt: null`) | `Maestro` commit `c403c08 fix(arbiter): LABS-87 — report outcome on validation failure`; roadmap `COWORK_CONTEXT.md:281` marks "✅ closed 2026-05-07" | **Close → Done** |
| **LABS-92** — route_task missing `metadata.decision_id` (= arbiter#9) | Arbiter | `Backlog` (Urgent) | `arbiter` `d1a8ecd feat(obs+#9): … surface decision_id`, `dc8368a … arbiter#9 closed`; roadmap `COWORK_CONTEXT.md:286` "✅ fixed 2026-04-25, both sides" | **Close → Done** |
| **LABS-91** — R-10 follow-ups: tag-release upload + pyrefly | Arbiter | `Backlog` (High) | `arbiter` `81fe183 ci: close R-10 … (closes #8)`, `8881ee6` (tag-release upload), `a15443d` (pyrefly); roadmap `:278` "R-10 ✅ closed". Both "still open" items of the task are closed | **Close → Done** |
| **LABS-93** — R-05 real-subprocess e2e (arbiter-mcp) | Maestro | `Backlog` | `Maestro` `f1f7d26` + `6b0d459` + `2b5c23d` (R-05 e2e/CI/scheduler-driven); roadmap `:270` "R-05 ✅ closed" | **Close → Done** |
| **LABS-58** — Integration gap Maestro ↔ ATP (verify step) "not implemented" | all_ai_orchestrators | `Backlog` | R-06a (`atp run` as `validation_cmd`) closed 2026-04-25 + R-06b M1–M4 (`5758dd8`/`290acde`/`a3e7aed`/`3066ded`). The description "No implementation" is no longer true | **Close → Done** (or refile as R-06b M5) |

> Note: `LABS-88/89/90` (Maestro, v0.3.0 chores) are correctly in `Backlog` — roadmap `:287` also keeps them `🟡 pending`. This is **not** a discrepancy.

---

## 2. Missing tasks: work exists in git/roadmap, but there is no issue in Linear

| Topic | Where in reality | Is it in Linear | Recommendation |
|------|------------------|------------------|--------------|
| **R-06b M1–M4** — Maestro↔ATP benchmarking (async runner, SpawnerResponder, live ATP SDK, arbiter wiring) | `Maestro` `5758dd8`, `290acde`, `a3e7aed`, `3066ded`; roadmap `:272–273` | **No** | File an epic "R-06b benchmark" with M1–M4 (Done) and **M5 CLI** (pending) |
| **arbiter `report_benchmark` + protocol 1.1.0 + `benchmark_runs`** | `arbiter` `aa72b40` (expose tool + bump 1.1.0), `db1e019` (docs); roadmap `:279` | **No** | File an issue (Done in code). ⚠ arbiter's own docs (README/CLAUDE/TODO/arbiter-spec) for the 6th tool **have not been updated yet** — a separate open task |
| **R-07** — eval-driven routing A/B (BenchmarkResult → DT inference) | roadmap `:275` "🟢 unblocked 2026-05-23" | **No** | File as a next-up task (Maestro/Arbiter) |
| **Observability M2 (done) / M3 (pending)** | `Maestro` `d474120` (M2); roadmap `:283–284`. In Linear only `LABS-95` (Plan 1 → M1) | Partially | Add M2 (Done) and M3 (pending, per-tick metrics + dashboards) |
| **spec-runner v2.1.0** + 5 Dependabot fixes | `spec-runner` `29d7f50`, `340f569` | **No** | Optional (minor), but the release is worth recording |

---

## 3. Stale titles and descriptions (status is correct, text is not)

| Linear | Problem in the text | What is actually the case |
|--------|-------------------|-------------------|
| **LABS-79** | Title "R-03 … (in progress, 7/32 tasks)" | Done; the description already says "SHIPPED 32/32 in v0.2.0". Bring the title into line |
| **LABS-57** | Title "Maestro ↔ Arbiter … not implemented" | Done (SHIPPED via R-03/v0.2.0). The title contradicts the status |
| **LABS-55** | "only 4 [projects] filed in Linear" | The Labs team now has **6** projects (proctor-a added). The inventory gap is effectively closed: `LABS-59` (proctor-a project) Done, `LABS-60` (open-prose without a separate project) Done, agents-for-game canceled (`LABS-61`). Candidate for **Done** |
| **LABS-56** | References "COWORK_CONTEXT.md (version 2026-04-05)", examples `executor`/`pylon` | COWORK_CONTEXT is now 2026-05-23: `executor`→`spec-runner`, `pylon` removed. The old examples are outdated — **but the premise is alive** (see §4) |
| **LABS-64** | "all three projects have an issue about GitHub Actions" | The preconditions are closed: `LABS-44` (Maestro CI) Done, `LABS-32` (Arbiter CI) Done, R-10 Done. The scope can be reassessed |

---

## 4. Additional observations

**Project statuses in Linear = `Backlog` for all six.** ATP Platform (Production), Maestro (Stable Beta), Arbiter (Stable), spec-runner (Stable) — all shown as `Backlog` at the project level. The field is apparently not maintained; if it is displayed to anyone on a dashboard, it is misleading.

**Drift in the registry itself (`COWORK_CONTEXT.md`), not in Linear.** The registry (`COWORK_CONTEXT.md:22`) records **spec-runner v2.0.0**, while git shows release **v2.1.0** (`spec-runner` `29d7f50`, 2026-05-23). This is exactly the "registry ≠ reality" class of drift described in `LABS-56` — i.e. the task is conceptually current, its specific examples are just outdated.

**Why this happened (hypothesis).** The workflow clearly moved to R-XX / git-driven tracking (the roadmap table in `COWORK_CONTEXT.md` + DOGFOOD_LOG + commits with `R-0x`/`LABS-NN` in the message). Linear remained an artifact of the initial planning on April 15–17 and has not been updated since. Before "fixing" statuses, it's worth deciding the strategic question (see below).

---

## 5. Recommended actions

**Strategically (choose one):**

- **(A)** Recognize `COWORK_CONTEXT.md` + git as the single source of truth, and Linear as an archive. Then mass "closing" of tasks is unnecessary; it's enough to mark the stale items once and stop breeding drift. Cheap, honestly reflects current practice.
- **(B)** Bring Linear back into service as a live tracker. Then a one-off reconcile is needed (below) + the discipline of "a commit closes an issue". More expensive, but gives a single place for status/priorities/SLA that the git table lacks.

> My assessment: if you work solo and git-first — (A) is more efficient; Linear as a mirror doesn't pay off. (B) is justified only if other participants appear or an external status dashboard is needed. A reasonable middle ground: close the obviously-done items (§1) and file the R-06b epic (§2), and leave the rest as is.

**Tactically (if we do a reconcile, mapped to project):**

1. **Maestro** — close `LABS-87`, `LABS-93`; fix the titles of `LABS-79`, `LABS-57`.
2. **Arbiter** — close `LABS-91`, `LABS-92`; file an issue "update arbiter docs for `report_benchmark`/protocol 1.1.0" (a real open gap, roadmap `:279`).
3. **Maestro/Arbiter** — file an epic **R-06b** (M1–M4 Done, M5 pending) and **R-07** (unblocked); add observability **M2 (Done)/M3 (pending)**.
4. **all_ai_orchestrators (umbrella)** — close/refile `LABS-58`; reassess `LABS-55`, `LABS-56`, `LABS-64` (the premises have changed).
5. **COWORK_CONTEXT.md** — update the spec-runner version **2.0.0 → 2.1.0** (this is outside Linear, but within your "registry coherence" zone).

> All edits in Linear and in `COWORK_CONTEXT.md` are up to you: I work read-only on the repositories and don't touch Linear without an explicit command. If you decide to do the reconcile through me — tell me which items, and I'll need your OK to write to Linear.

---

## 6. Reconcile log (done 2026-05-25)

Andrei confirmed the reconcile (all three buckets, without comments in the tasks). Changes were made via Linear MCP (Linear only; the repositories and `COWORK_CONTEXT.md` were not touched).

### §1 — closed (→ Done)

| Linear | Was | Became |
|--------|------|-------|
| LABS-87 | Backlog | **Done** |
| LABS-91 | Backlog | **Done** |
| LABS-92 | Backlog | **Done** |
| LABS-93 | Backlog | **Done** |
| LABS-58 | Backlog | **Done** |

### §2 — filed

| Linear | Project | Status | What it is |
|--------|--------|--------|---------|
| LABS-107 | Maestro | In Progress | Epic R-06b (M1–M4 done, M5 pending) |
| LABS-111 | Maestro | Backlog | R-06b M5: CLI `maestro benchmark` (sub of LABS-107) |
| LABS-108 | Arbiter | In Progress | report_benchmark + protocol 1.1.0 — update arbiter docs |
| LABS-109 | Maestro | Todo | R-07: eval-driven routing A/B |
| LABS-110 | Maestro | Backlog | Observability M3 (M2 done recorded in the description) |

### §3 — fixed

| Linear | Change |
|--------|-----------|
| LABS-79 | Title → "R-03: Arbiter MCP client integration" (removed "in progress, 7/32") |
| LABS-57 | Title → "… — closed (R-03/v0.2.0)" |
| LABS-55 | Title + description brought up to date; status → **Done** (inventory completed) |
| LABS-56 | Description updated: old examples (executor/pylon) removed, current drift spec-runner v2.0.0↔v2.1.0 added; left as Backlog |
| LABS-64 | Description updated: preconditions (CI) closed; left as Backlog as a candidate for defer/close |

### Remaining outside Linear (your zone)

- **`COWORK_CONTEXT.md:22`** — update the spec-runner version **2.0.0 → 2.1.0** (a registry edit, done in the repository — I don't write there per the read-only rules).
- Decide the fate of LABS-64 (defer or close) and LABS-56 (the format of the periodic reconciliation).
