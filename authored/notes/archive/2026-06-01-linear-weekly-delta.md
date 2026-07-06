---
title: 'Linear ↔ reality: weekly delta'
type: note
status: archived
owner: Andrei
updated: 2026-06-01
archived: 2026-07-06
reason: Linear tracking frozen — historical
---

# Linear ↔ reality: weekly delta

> Date: 2026-06-01 · Linear team: **Labs** (key `LABS`) · Source of truth: **git + roadmap** (`COWORK_CONTEXT.md`)
> Mode: read-only. Delta window: since the previous report `2026-05-25-linear-vs-reality-audit.md` (including its reconcile log).
> ⚠️ **Linear was not read in this run** — see below.

## TL;DR

1. **Linear requires re-authentication via OAuth** — it cannot be completed in a background scheduled run. A direct reconciliation against the actual state of the issues was not performed; the delta is built against the baseline from the previous report (the reconcile of 2026-05-25, where LABS-107…111 are already filed/updated). **Open the app and reconnect Linear**, then rerun the reconciliation (or say "reconcile").
2. **All the notable work this week is in `spec-runner`.** Maestro, arbiter and atp-platform are essentially static (0 functional commits; atp-platform has one chore). So for the epics filed last week (LABS-107…111, Maestro/Arbiter), there is **no** movement in the code — no new status discrepancies arose for them.
3. **`spec-runner` shipped four releases — v2.2.0 → v2.3.0** with a major "status & error handling" feature (the `error_kind`/`error_stage` taxonomy, `StageReporter`, detection of second-pass failures, new CLI adapters OpenCode/Pi Agent, a fix to the codex adapter). **Not a single R-XX/LABS tag in the commits, not a single issue in Linear.** This is a new "missing" layer.
4. **Registry drift widened:** `COWORK_CONTEXT.md` still writes spec-runner **v2.0.0** (in 4 places), reality — **v2.3.0**. The previous report recorded 2.0.0→2.1.0; over the week the gap grew to 2.0.0→**2.3.0**. The registry edit recommended last time has not been made.
5. **The unregistered repositories `prograph`/`appgraph`/`prograph-vault` are active** (commits May 27–28, "M8 workspace recursion", snapshot "17 projects, 28 edges"); they are neither in the `COWORK_CONTEXT.md` registry nor among the 6 Labs projects. atp-platform's single commit configures an exclude for `prograph` — i.e. integration is already underway, while there is no governance accounting.

---

## 0. Linear access status

`mcp__plugin_engineering_linear__authenticate` returned an authorization URL — in a background run OAuth cannot be completed, the user is absent. Therefore the step "pull issues by project" **was not performed**. Everything below is a git/roadmap delta against the expected Linear state per the previous reconcile (2026-05-25). After reconnecting Linear, the reconciliation should be run again to confirm the statuses of LABS-107…111.

---

## 1. Git activity over 7 days (by main projects)

| Project | Commits over 7d | Gist | Release |
|--------|:---:|------|-------|
| **Maestro** | 0 | no activity | — |
| **arbiter** | 0 | no activity | — |
| **atp-platform** | 1 | `3a7234a chore: configure prograph exclude for non-project sub-dirs` (config only) | — |
| **spec-runner** | ~50 | status & error handling, StageReporter, new adapters | **v2.2.0 → v2.3.0** |

> Maestro/arbiter "silence" is not a risk in itself: the epics LABS-107 (R-06b M5), LABS-108 (arbiter docs), LABS-109 (R-07), LABS-110 (obs M3) were filed last week as pending/in-progress and there has been no code for them yet. There are **no new** status discrepancies for them.

---

## 2. New discrepancies over the week

### 2.1. MISSING — work in git without an issue in Linear

| Topic | Where in reality | In Linear | Type | Recommendation |
|------|------------------|----------|-----|--------------|
| **spec-runner "status & error handling" (v2.3.0)** — `error_kind`/`error_stage` columns + migration, `ErrorPattern`/`classify()`, `StageReporter` + `STAGES`, detection of second-pass failures, `reset_failed_to_pending` | `spec-runner` `fe04424` (spec), `97a08c5` (plan, 28 TDD tasks), `a4920c4`/`56e12b5`/`604dc58`/`d36ca49 release: v2.3.0` | **No** | File an issue/epic "spec-runner v2.3.0 error-handling" (Done). This is a standalone feature line, an analog of R-XX |
| **New spec-runner CLI adapters** — auto-detect **OpenCode** and **Pi Agent** (`1ae1b06`), fix the codex adapter `codex exec` instead of `codex -p` (`0695e13`) | `spec-runner` `1ae1b06`, `0695e13` | **No** | Record: expands the agent matrix alongside the Maestro spawners (claude_code/codex/aider). Update the integration map |
| **spec-runner: git-automation OFF by default for subdir projects** (`002ca61`, `4fe7fce` `_detect_subdir_repo`) | `spec-runner` `002ca61`,`4fe7fce` | **No** | A default-behavior change — worth an issue/changelog note |
| **spec-runner releases v2.2.0 / v2.2.1 / v2.2.2** — CI off Node 20, fix of estimate-range parsing (decimal/en-dash), stderr progress mirror | `spec-runner` `42a88a7`,`7babd0a`,`8f6a153` | **No** | Optional (minor), but the releases are worth reflecting |

> R-XX/LABS tags in spec-runner commits over the week: **not a single one**. So this is a pure "miss", not a "status" (there is no commit claiming closure of a tracked task).

### 2.2. STALE DESCRIPTION — the registry contradicts the fact

| Where | In the text | Fact | Type |
|-----|----------|------|-----|
| `COWORK_CONTEXT.md:22`, `:85`, `:134`, `:213` | spec-runner **v2.0.0** | git: **v2.3.0** (tag `v2.3.0`, `pyproject.toml`) | Registry drift (widened from 2.0.0→2.1.0 a week ago to 2.0.0→**2.3.0**) |

### 2.3. Unregistered repositories (governance gap)

| Repo | Activity over the week | In the registry? | In Linear? |
|------|----------------------|:---:|:---:|
| **prograph** / **appgraph** / **prograph-vault** | `e383309` snapshot "17 projects, 28 edges, 9 mcp_call", `379cf3c` "M8 workspace recursion", `4f77ad2` validation of tasks.md (May 27–28) | **No** | **No** (Labs = 6 projects) |

> Already noted in memory (`project-new-unregistered-repos-2026-05.md`): appgraph overlaps with Maestro DAG. New this week — the repo is developing actively and **atp-platform is already adapting to it** (`3a7234a` prograph exclude). Time to decide: add to the registry or explicitly mark as an experimental sandbox.

---

## 3. What did NOT change (no new discrepancies)

- **Maestro ↔ Arbiter / ATP** — no code over the week; statuses R-05/R-06a/R-06b M1–M4 as in the roadmap. LABS-107…111 without movement, but that is expected (filed as pending).
- **LABS-108 (update arbiter docs for `report_benchmark`/protocol 1.1.0)** — arbiter without commits, the gap remains **genuinely open**, but this is carried over from last week, not a new delta.

---

## 4. Recommended actions

1. **Linear (infrastructure):** reconnect OAuth (open the Linear app → authorize), then rerun this reconciliation to confirm the statuses of LABS-107…111. Without it the weekly reconciliation runs "blind" relative to the live tracker.
2. **spec-runner:** file an issue/epic in Linear for the **v2.2–v2.3 "status & error handling" + new adapters** line (Done in code). This is the only notable untracked work of the week.
3. **COWORK_CONTEXT.md (registry, outside Linear, your zone — read-only for me):** update spec-runner **2.0.0 → 2.3.0** in lines `:22`, `:85`, `:134`, `:213`. Add the new spec-runner adapters (OpenCode, Pi Agent) to the integration map.
4. **prograph/appgraph/prograph-vault:** make a governance decision — add to the `COWORK_CONTEXT.md` registry (with a role and the link to Maestro DAG / atp-platform) or explicitly mark as experimental. Right now they are "invisible" to both the registry and Linear, while atp-platform is already tying itself to them.
5. **Reconcile in Linear:** if you decide to make the Linear edits through me — say "reconcile" and give the OK to write; I don't touch Linear or the repositories on my own.

---

> Sources: git history of `spec-runner` (`d36ca49 release: v2.3.0`, `1ae1b06`, `0695e13`, `002ca61`), `atp-platform/3a7234a`, `prograph/e383309`+`379cf3c`; registry `COWORK_CONTEXT.md:22,85,134,213`; baseline — `_cowork_output/2026-05-25-linear-vs-reality-audit.md`.
