---
title: 'Linear ↔ reality: weekly delta'
type: note
status: archived
owner: Andrei
updated: 2026-06-15
archived: 2026-07-06
reason: Linear tracking frozen — historical
---

# Linear ↔ reality: weekly delta

> Date: 2026-06-15 · Linear team: **Labs** (key `LABS`) · Source of truth: **git + roadmap** (`COWORK_CONTEXT.md`)
> Mode: read-only. Delta window: since the previous report `2026-06-08-linear-weekly-delta.md` (i.e. 2026-06-08 → 2026-06-15).
> ⚠️ **Linear was not read in this run** — OAuth requires a user, see section 0.

## TL;DR

1. **Linear requires re-authentication via OAuth — the fourth background run in a row goes "blind".** A direct status reconciliation was not performed. **Open the app, reconnect Linear and run "reconcile".**
2. **A busy week in `atp-platform` (34 commits) and `spec-runner` (a release train v2.4.0→v2.7.0).** Maestro and arbiter — zero commits in the window (both last on 2026-05-23). No new status discrepancies for the Maestro/Arbiter epics.
3. **A new untracked workstream in atp-platform: "eval-results / grader spine" (ADR-006).** A new task nomenclature appeared — **SP-1/SP-3/SP-4** and **Phase A-1/A-2**, plus active implementation of **R-07** (code-review eval, 7 commits). The roadmap describes R-07 as "🟢 unblocked, next: BenchmarkResult as weighting input" — the actual work went in **a different direction** (code-review eval harness + unified CaseVerdict). The roadmap's R-07 description is stale.
4. **Two releases with no visible LABS issues: `atp-platform v2.1.0` (#163) and `spec-runner v2.7.0`.** spec-runner shipped **five** releases over the week (v2.4.0, v2.4.1, v2.5.0, v2.6.0, v2.7.0) — doctor-probe, CLI presets (qwen/copilot), cost-tracking fix, orphan recovery. Not a single spec-runner commit over the week has **any LABS/R-XX tags** → almost certainly no issue in Linear.
5. **Registry drift got worse (carry-over + degradation):** `COWORK_CONTEXT.md` writes spec-runner **v2.0.0** (reality **v2.7.0**), atp-platform **v2.0.0** (reality **v2.1.0**), arbiter **v0.1.0** (reality **v0.2.0** since 2026-05-23). The new sub-package **`atp-method` v0.1.0** (a separate PyPI tag) is absent from the registry entirely.

---

## 0. Linear access status

`mcp__plugin_engineering_linear__authenticate` again returned an authorize URL — OAuth cannot be completed in a background run (the user is absent). The step "pull issues by the 6 Labs projects" (Maestro, Arbiter, ATP Platform, spec-runner, proctor-a, all_ai_orchestrators) **was not performed**. Everything below is a git/roadmap delta against the expected state per the previous report (2026-06-08). After reconnecting Linear, the reconciliation should be run again to confirm whether issues have been filed for the SP-/Phase-/R-07 line and the two releases.

---

## 1. Git activity over 7 days (2026-06-08 → 2026-06-15)

| Project | Commits in the window | Gist | Release/version (fact) |
|--------|:---:|------|------|
| **Maestro** | 0 | no activity (last 2026-05-23) | v0.4.0 (unchanged) |
| **arbiter** | 0 | no activity (last 2026-05-23) | **v0.2.0** (the bump was 2026-05-23, outside the window) |
| **spec-runner** | ~33 | release train v2.4.0→v2.7.0: doctor, CLI presets, cost-fix, orphan recovery | **v2.7.0** |
| **atp-platform** | ~34 | R-07 code-review eval, grader spine (ADR-006, SP-/Phase-), atp-method plugin, Terraform IaC, dashboard | **v2.1.0** (+ `atp-method-v0.1.0`) |

Task tags encountered in atp-platform commit messages over the week (recognized):
`R-07` ×7, `Phase A-1` ×2, `Phase A-2` ×1, `SP-1`/`SP-3`/`SP-4` ×1, `R-006`/ADR-006 ×1. For spec-runner — **not a single** tracker tag.

---

## 2. New discrepancies over the week

### 2.1. MISSING — notable work in git without an issue in Linear

| Topic | Where in reality | In Linear | Type | Recommendation |
|------|------------------|----------|-----|--------------|
| **"eval-results / grader spine" — a new workstream** (ADR-006 "unified capability test types", canonical dimensioned store, taxonomy registry, dashboard leaderboard) | `atp-platform`: `3c59903` (#175, ADR-006), `c97cdab` (#176, CaseVerdict), `c57f79c` (#177, taxonomy), `99b8f01` (#179, store), `682f3cf` (#180, leaderboard), `5f35692` (#181, schema) | **No** (new SP-/Phase- numbering, not LABS) | File an epic "ATP eval-results architecture (ADR-006)" and subtasks SP-1/3/4 + Phase A-1/A-2. Mapping of the internal SP-/Phase- numbering ↔ LABS is missing |
| **R-07 code-review eval — actual implementation** (thin slice → deterministic findings_match → strict Finding validation → full 5-level breakpoint sweep + harness) | `atp-platform`: `c75c004` (#171), `472f323` (#172), `b78bc94` (#173), `3bb88fd` (#174), `98a89ec` (#182), `e83648e`/`22f7c94` (#183) | **No/stale** | See 2.2 — this is both a STATUS (the roadmap description of R-07 is stale) and work without a LABS issue |
| **Release `atp-platform v2.1.0`** (#163, 2026-06-12) + a new PyPI package **`atp-method` v0.1.0** (plugin: AgentEvalCaseEvaluator, agent-eval-case loader) | `atp-platform`: `167ba2d` (#163), `26f4481` (#146), `5b97452` (#145), `d55e13d` (#144), `b84ef96` (#165) | **No** | File a release issue v2.1.0 (Done) and a separate track for the sub-package `atp-method` |
| **spec-runner: five releases v2.4.0→v2.7.0** (doctor-probe #14, CLI presets qwen/copilot #20/#21, cost-tracking fix #16, orphan recovery #18, plan --from-file #17, pi-loop templates) | `spec-runner`: `2c43cc2` (v2.7.0), `c3e97e2` (v2.6.0), `44f4543` (v2.5.0), `41e00f8` (v2.4.0), `79d4607` (#14), `1df077a` (#18) | **No** (0 LABS tags) | File an epic "spec-runner v2.4–v2.7" or confirm that spec-runner releases aren't tracked in Linear |
| **AWS Bedrock demo: Terraform IaC** replaced the manual `examples/aws-cloud`; a continuation of last week's EPAM/Bedrock line | `atp-platform`: `ec085c0` (#167), `8d7d057` (#153), `737cd42` (#152), EPAM overview `5517460` (#155) | **No** | Extend last week's "ATP EPAM demo + Bedrock" epic with the IaC item |

> Confirmation of the "miss": over the week atp-platform has not a single `LABS-NN`; in spec-runner — no tracker tag at all. The internal SP-/Phase- numbering is apparently GitHub-PR planning, not Linear.

### 2.2. STATUS / STALE DESCRIPTION — roadmap diverges from the fact

| Where | In the roadmap text | Fact over the week | Type |
|-----|------------------|----------------|-----|
| `COWORK_CONTEXT.md:275` | **R-07** "🟢 unblocked … next: `BenchmarkResult` as weighting input in DT inference" | R-07 is being actively implemented as a **code-review eval pipeline** (cases + claude_code shim + report_benchmark reporter + 5-level sweep). The direction differs from what's recorded | STALE DESCRIPTION |
| `COWORK_CONTEXT.md:19,234` | atp-platform **v2.0.0** | git: **v2.1.0** (`atp-platform/pyproject.toml:version`), tag `v2.1.0` 2026-06-12 | STATUS/version |
| `COWORK_CONTEXT.md` (ATP map) | packages: `atp-platform-sdk`, `atp-games` | added **`atp-method` v0.1.0** (a new plugin package, tag `atp-method-v0.1.0`) | MISSING from the map |

### 2.3. STALE DESCRIPTION / registry (carry-over, not new)

| Where | In the text | Fact | Status |
|-----|----------|------|--------|
| `COWORK_CONTEXT.md:22,85,134,213` | spec-runner **v2.0.0** | git: **v2.7.0** (`spec-runner/pyproject.toml`) | Carried over from 2026-05-25/06-01/06-08; **the drift grew** (was 2.3.0 → became 2.7.0) |
| `COWORK_CONTEXT.md:20,117` | arbiter **v0.1.0** | git: **v0.2.0** (`arbiter/Cargo.toml`, bump `aa72b40` 2026-05-23) | Not explicitly noted before; carry-over |
| roadmap `LABS-108` (arbiter docs for `report_benchmark`/protocol 1.1.0) | "⚠ arbiter docs not updated yet" | arbiter without commits in the window — the gap **persists** | Carry-over, no movement |

---

## 3. What did NOT change (no new discrepancies)

- **Maestro / arbiter** — zero commits in the window. Statuses R-05/R-06a/R-06b M1–M4, M5 (pending), Maestro M3 observability (pending) — as in the roadmap. No new status discrepancies.
- **prograph / appgraph / prograph-vault** — without commits in the window (last common `4f77ad2` 2026-05-28). The governance gap persists without movement; the registry decision not made.
- **proctor-a** — no activity (the pause since 2026-04-16 continues).
- **LABS-108** (arbiter docs) and the general question of registering the SP-/Phase- nomenclature — carried over, no duplicates needed.

---

## 4. Recommended actions

1. **Linear (infrastructure, priority):** reconnect OAuth (open the Linear app → authorize), then "reconcile". The fourth run in a row without a live tracker.
2. **atp-platform (Linear):** file an epic **"ATP eval-results architecture / ADR-006"** with subtasks SP-1/SP-3/SP-4 and Phase A-1/A-2; update/close **R-07** with its real content (code-review eval, not "BenchmarkResult weighting"); a release issue **v2.1.0** + a track for the sub-package **atp-method**.
3. **spec-runner (Linear):** decide — do we track spec-runner releases in Linear; if yes, file an epic **"spec-runner v2.4–v2.7"** (doctor, CLI presets, cost-fix, orphan recovery).
4. **COWORK_CONTEXT.md (registry, your zone — read-only for me):** (a) spec-runner `2.0.0 → 2.7.0` (`:22,85,134,213`); (b) atp-platform `2.0.0 → 2.1.0` (`:19,234`); (c) arbiter `0.1.0 → 0.2.0` (`:20,117`); (d) add the package `atp-method` v0.1.0 to the ATP map; (e) update the roadmap line R-07 (`:275`) to the actual code-review eval.
5. **Reconcile:** any Linear edits (new SP-/Phase-/R-07 epics, release issue) — only with your OK. Say "reconcile" and give the go-ahead to write; I don't touch Linear or the repositories myself.

---

> Sources: git history of `atp-platform` (`3c59903`, `c97cdab`, `c57f79c`, `99b8f01`, `682f3cf`, `5f35692`, `98a89ec`, `c75c004`, `472f323`, `167ba2d`, `26f4481`, `ec085c0`) and `spec-runner` (`2c43cc2`, `c3e97e2`, `44f4543`, `41e00f8`, `79d4607`, `1df077a`); versions `atp-platform/pyproject.toml:version=2.1.0`, `spec-runner/pyproject.toml:version=2.7.0`, `arbiter/Cargo.toml:version=0.2.0`; tags `v2.1.0`, `atp-method-v0.1.0`, `v2.7.0`; registry `COWORK_CONTEXT.md:19,20,22,85,117,134,213,234,275`; baseline — `_cowork_output/2026-06-08-linear-weekly-delta.md`. Linear: not read (OAuth required).
