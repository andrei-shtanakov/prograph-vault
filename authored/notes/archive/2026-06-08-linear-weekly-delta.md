---
title: 'Linear ↔ reality: weekly delta'
type: note
status: archived
owner: Andrei
updated: 2026-06-08
archived: 2026-07-06
reason: Linear tracking frozen — historical
---

# Linear ↔ reality: weekly delta

> Date: 2026-06-08 · Linear team: **Labs** (key `LABS`) · Source of truth: **git + roadmap** (`COWORK_CONTEXT.md`)
> Mode: read-only. Delta window: since the previous report `2026-06-01-linear-weekly-delta.md` (i.e. 2026-06-01 → 2026-06-08).
> ⚠️ **Linear was not read in this run** — OAuth requires a user, see section 0.

## TL;DR

1. **Linear again requires re-authentication via OAuth** — the third background run in a row goes "blind" relative to the live tracker. A direct status reconciliation was not performed. **Open the app, reconnect Linear and run "reconcile".**
2. **All the notable work of the week is in `atp-platform`** (8 commits June 5–6). Maestro, arbiter, spec-runner — zero commits in the window. So no new status discrepancies arose for the Maestro/Arbiter/spec-runner epics.
3. **A new missing layer (atp-platform): "EPAM demo" + Bedrock provider.** A notable feature line — `feat: Bedrock-hosted Claude provider for llm_judge` (#136) + a whole on-prem docker-compose demo stand (#135) + a 15-min runbook (#137). **Neither R-XX nor a LABS tag in the commits** → almost certainly no issue in Linear. This is new untracked work of the week.
4. **Two CVEs closed in atp-platform dependencies** (idna CVE-2026-45409, #133; starlette/fastapi CVE-2026-48710, #131/#134). Security work with no visible issue in Linear — worth tracking at least for the audit.
5. **Registry drift not fixed (carry-over, NOT a new delta):** `COWORK_CONTEXT.md` still writes spec-runner **v2.0.0**, reality — **v2.3.0**. The recommendation from the previous two reports has not been applied. `prograph`/`appgraph` without commits in the window — the governance gap persists, but without movement.

---

## 0. Linear access status

`mcp__plugin_engineering_linear__authenticate` returned an authorize URL — OAuth cannot be completed in a background run (the user is absent). The step "pull issues by the 6 Labs projects" **was not performed**. Everything below is a git/roadmap delta against the expected state per the previous report (2026-06-01). After reconnecting Linear, the reconciliation should be run again to confirm whether issues have been filed for the demo/Bedrock line.

---

## 1. Git activity over 7 days (by main projects)

| Project | Commits in the window | Gist | Release/version |
|--------|:---:|------|------|
| **Maestro** | 0 | no activity (last commit 2026-05-23) | — |
| **arbiter** | 0 | no activity (last commit 2026-05-23) | — |
| **spec-runner** | 0 | no activity in the window (last 2026-05-30, before the window) | v2.3.0 (unchanged) |
| **atp-platform** | 8 | EPAM demo, Bedrock llm_judge, 2 CVE bumps, dashboard fix | pyproject still `2.0.0` |

Full atp-platform list (all 2026-06-05/06):

| Commit | Type | Description |
|--------|-----|----------|
| `c692ff5` | fix | dashboard: `agent_id` Optional in `SuiteExecutionSummary` + plan for `/ui/executions` (#132) |
| `52a4557` | sec | idna 3.11 → 3.15, CVE-2026-45409 / GHSA-65pc-fj4g-8rjx (#133) |
| `8314472` | sec | starlette 0.50.0 → 1.0.1 (Dependabot, #131) |
| `e75b77b` | docs | TODO: remove the closed item about the starlette upgrade (#134) |
| `a00541a` | **feat** | evaluators: **Bedrock-hosted Claude provider for llm_judge** (#136) |
| `e251dd4` | **feat** | **on-prem docker-compose demo** (platform + HTTP agent) (#135) |
| `543ab6b` | docs | unified **EPAM demo runbook** + Act 1 driver `run_demo.sh` (#137) |
| `ac9387f` | fix | demo: remove the `working_dir` override that broke `uv run atp` in compose |

> The numbers `#131…#137` are **GitHub PRs**, not Linear LABS issues. The only explicit tracker reference is `LABS-54` in the body of `c692ff5` (problem background), not a claim of closure.

---

## 2. New discrepancies over the week

### 2.1. MISSING — work in git without an issue in Linear

| Topic | Where in reality | In Linear | Type | Recommendation |
|------|------------------|----------|-----|--------------|
| **EPAM demo: Bedrock provider for llm_judge** — `provider="bedrock"` via `AsyncAnthropicBedrock` + IAM, 4–5 new tests | `atp-platform` `a00541a` (#136); `atp-platform/docs/.../DEMO.md` (Act 2) | **No** (R-XX/LABS absent) | File an issue/epic "ATP EPAM demo + Bedrock judge" (Done in code). A standalone feature line, an analog of R-XX |
| **EPAM demo: on-prem docker-compose stand** — `examples/compose-demo/` (FastAPI agent over the HTTP contract, suite.yaml, dashboard) | `atp-platform` `e251dd4` (#135), runbook `543ab6b` (#137), fix `ac9387f` | **No** | The same epic: the demo as a deliverable (tied to the May ATP direction meeting) |
| **Security: 2 CVEs closed in dependencies** — idna CVE-2026-45409; starlette CVE-2026-48710 (via fastapi 0.128→0.136.3) | `atp-platform` `52a4557` (#133), `8314472` (#131), `e75b77b` (#134) | **No** | File a light security issue for the audit (Done) or note that the Dependabot flow doesn't require a Linear track |
| **Planned `/ui/executions` page** (CLI run history in the browser) — so far only a plan | `atp-platform` `c692ff5` → `spec/dashboard-execution-history.md`, tracked in `TODO.md` | **No (probably)** | If we run UI tasks in Linear — file an issue (Todo); right now it lives only in TODO.md |

> R-XX/LABS tags in atp-platform commits over the week: **not a single one** (except the background mention of `LABS-54`). So this is a "miss", not a "status".

### 2.2. STATUS — git claims closure, but Linear may be behind

| Issue | What's in git | Expectation in Linear | Check after reconnect |
|-------|-----------|-------------------|---------------------------|
| **LABS-54** (CLI persists `agent_id=NULL`, denormalized `agent_name`) | `c692ff5` fixes the derived 500 on `/api/suites` (agent_id made Optional) — the behavior for LABS-54 is now handled correctly | If LABS-54 was open — it is either closed or spawned a follow-up for `/ui/executions` | Yes |

### 2.3. STALE DESCRIPTION / registry (carry-over, not new)

| Where | In the text | Fact | Status |
|-----|----------|------|--------|
| `COWORK_CONTEXT.md:22,85,134,213` | spec-runner **v2.0.0** | git: **v2.3.0** (`spec-runner/pyproject.toml`) | Carried over from 2026-06-01 and 2026-05-25 — **not fixed** |
| `COWORK_CONTEXT.md` integration map | atp-platform as "framework-agnostic", llm_judge providers: OpenAI/Anthropic | added a **Bedrock** provider (`a00541a`) | New — worth adding to the map |

---

## 3. What did NOT change (no new discrepancies)

- **Maestro / arbiter / spec-runner** — zero commits in the window. Statuses R-05/R-06a/R-06b M1–M4, R-07 (unblocked), M5 (pending) — as in the roadmap. No new status discrepancies.
- **LABS-108** (update arbiter docs for `report_benchmark` / protocol 1.1.0) — arbiter without commits, the gap **remains open**, but this is a carry-over, not a new delta.
- **prograph / appgraph / prograph-vault** — without commits in the window (last 2026-05-28). The governance gap persists without movement; the registry decision still not made.
- **spec-runner v2.2–v2.3 "status & error handling"** — noted as a miss on 2026-06-01; no new activity, no duplicate needed.

---

## 4. Recommended actions

1. **Linear (infrastructure):** reconnect OAuth (open the Linear app → authorize), then "reconcile". The third run in a row without a live tracker — priority.
2. **atp-platform:** file in Linear an epic/issue for the **EPAM demo + Bedrock judge** (#135/#136/#137, Done in code) and, optionally, a security issue for the two closed CVEs (#131/#133). This is all the untracked work of the week.
3. **atp-platform:** at the next release — bump the version (pyproject is still `2.0.0`, even though the Bedrock feature and the demo stand were added). And file an issue for the planned `/ui/executions` page (plan in `spec/dashboard-execution-history.md`).
4. **COWORK_CONTEXT.md (registry, your zone — read-only for me):** (a) update spec-runner `2.0.0 → 2.3.0` in lines `:22,85,134,213` (carry-over from two previous reports); (b) add the Bedrock provider to the ATP integration map.
5. **Reconcile:** the Linear edits (new issues for demo/Bedrock, checking LABS-54) — only with your OK. Say "reconcile" and give the go-ahead to write; I don't touch Linear or the repositories myself.

---

> Sources: git history of `atp-platform` (`a00541a`, `e251dd4`, `543ab6b`, `c692ff5`, `52a4557`, `8314472`, `e75b77b`, `ac9387f`); versions `atp-platform/pyproject.toml:version=2.0.0`, `spec-runner/pyproject.toml:version=2.3.0`; registry `COWORK_CONTEXT.md:22,85,134,213`; baseline — `_cowork_output/2026-06-01-linear-weekly-delta.md`. Linear: not read (OAuth required).
