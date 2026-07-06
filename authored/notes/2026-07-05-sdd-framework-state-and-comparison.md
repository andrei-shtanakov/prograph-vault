---
title: SDD framework — state & comparison
type: note
status: living
owner: Andrei
updated: 2026-07-05
---

# sdd-framework: current state and comparison with spec-runner / Maestro

> Date: 2026-07-05 · Mode: read-only · Author: Claude (TPM/architect)

## TL;DR

1. **sdd-framework is a methodology, not a runtime.** ~57 markdown files + 6 python scripts, zero services. It does not "execute" specs like spec-runner and does not orchestrate agents like Maestro — it defines a **process for writing specs and generating code from them** for data pipelines. The product = skill zones + templates + gates, not a CLI daemon.
2. **This is exactly where the "over-complicated scheme" lives.** Not 3 stages (like spec-runner), but **8 gates** (BR → FRD → 0a → 0b → 1 → 2 → 3 → 4 → 5) and **10 types of spec artifacts**. This is what you were recalling — not spec-runner and not Maestro.
3. **State — "skeleton + demo, no real runs."** 35 commits, last one 2026-07-01, author **Dmytro Honcharuk** (not you — this is the only project in the ecosystem with an external primary contributor). `generated_code/` is empty, there is no real product in `specs/` — only templates, the DQFramework, and a single demo dataset (`data/samples/pnl/`, 4 parquet files).
4. **The activation mechanism is original:** "skill zones" — each folder with a `SKILL.md` auto-activates the needed skill in Claude Code / Cursor / Windsurf when you work in it. Gates are enforced by text inside SKILL.md (a check for `Status: APPROVED` in the spec header), not by a validator in code.
5. **Overlap with spec-runner is conceptual, not code-level.** Both are "gated," both are spec-first. But spec-runner executes `tasks.md` and knows about frontmatter statuses programmatically; sdd-framework is about *how the author and the AI bring a spec to APPROVED*, and it ends with generated pipeline code rather than a task run.

---

## 1. What it is and where it sits in the ecosystem

| Parameter | Value |
|---|---|
| Path | `sdd-framework/` |
| Type | Methodology / framework (Spec-Driven Development for data pipelines) |
| Language | Markdown (specs/docs) + Python/PowerShell/Bash (demo-stack glue) |
| Version | not semver-versioned (—) |
| Git | 35 commits, branch `main`, last `62e3acc` 2026-07-01 |
| Primary author | **Dmytro Honcharuk** (external relative to the rest of the ecosystem) |
| Status in COWORK_CONTEXT | 🔨 Active (added to the registry only on 2026-07-05 during the freshness audit — hence it was "missed") |
| Working changes | working tree clean, `generated_code/` empty |

**Why you missed it:** the project was absent from the registry until today's edit (2026-07-05). Before this 43-day lag, COWORK_CONTEXT did not show it. The primary contributor is not you, so it never surfaced in your sessions.

---

## 2. Functionality — what sdd-framework actually does

### 2.1. Core: a gated lifecycle of 8 gates

A rigid chain, each gate being a hard dependency of the next (`sdd-framework/.claude/CLAUDE.md`):

```
Gate BR  Business Requirements   specs/requirements/{product}/BusinessRequirements.md   APPROVED
FRD      Functional Requirements specs/requirements/{product}/FunctionalRequirements.md APPROVED
Gate 0a  Platform Selection      specs/ingestion/{product}/PlatformSpec.md              APPROVED
Gate 0b  Source Assessment       {entity}/SourceSpec + DataModelSpec + STTM             APPROVED
Gate 1   Spec Stack              IngestionSpec + TransformSpec + ProvisioningSpec       APPROVED
Gate 2   DQ Baseline             DQSpec APPROVED + gate-IDs set on every criterion
Gate 3   Code Review             generated_code/ reviewed against the checklist
Gate 4   Testing                 all DQ gates PASS on sample/integration data
Gate 5   Deployment              deployment checklist + runbook signed off
```

### 2.2. Skill zones — the activation mechanism

Each directory with a `SKILL.md` = a "skill zone." You enter the folder, describe the task — the skill activates itself (`.claude/CLAUDE.md`):

| Directory | Skill | Skill product |
|---|---|---|
| `specs/requirements/` | requirements-spec | BusinessRequirements + FunctionalRequirements (from PDF) |
| `specs/ingestion/` | ingestion-spec | SourceSpec, DataModelSpec, STTM, IngestionSpec (per entity) |
| `specs/transform/` | transform-spec | TransformSpec (conformed/silver layer) |
| `specs/dq/` | dq-spec | DQSpec (quality gates) |
| `specs/provision/` | provision-spec | ProvisioningSpec (gold/presentation layer) |
| `platforms/cicd/` | cicd-spec | CI/CD pipeline config |
| `prompts/` | ai-prompt | Op A: PlatformContext; Op B: per-product code-generation prompts |

Skills are synced into `.claude/commands/*.md`. There is a **subagent mode**: the requirements skill spawns the ingestion skill for a single entity, which writes 4 files directly via Write and sets `Status: DRAFT` (never APPROVED — human review is mandatory).

### 2.3. 10 types of spec artifacts

Templates in `templates/specs/`: BusinessRequirements, FunctionalRequirements, PlatformSpec, SourceSpec, DataModelSpec, STTM, IngestionSpec, TransformSpec, ProvisioningSpec, DQSpec. Plus the shared `specs/dq/DQFramework.md`.

### 2.4. DQ model

6 dimensions (Completeness, Accuracy, Timeliness, Uniqueness, Validity, Consistency) with the gate-ID convention `{LAYER}-{DIM}-{SEQ}` (e.g. `ING-CPL-001`). Assertions — `tests/dq/dq_checks.sql` + `dq_suite.py`. Rule: every acceptance criterion of any spec must reference a DQSpec gate-ID before Gate 2 is closed.

### 2.5. Glue (not core, but present)

- Multi-platform: source (Parquet/CSV/DuckDB/PostgreSQL/Snowflake/REST), transform (dbt/Snowflake Tasks/SQL), CI/CD (GitHub Actions/GitLab/Azure DevOps/local runner). The stack is chosen in `PlatformSpec.md`, not hardcoded.
- Local demo stack: portable PostgreSQL without admin rights, `install/destroy/demo_run` for win+linux (`infrastructure/local-stack/`).
- MCP templates for Cursor/Windsurf/Claude Code (`infrastructure/ide/`), one-time `init.ps1/.sh`.
- End-to-end demo `examples/DemoScenarios.md` (acme_pnl, Gate BR→Gate 4) + example `examples/pdf-to-br/` (BR/FRD from PDF).
- Governance docs: Charter, SDD-Workflow, Retrospective, PlatformPitfalls, CodeReviewChecklist, DeploymentChecklist, Runbook.

---

## 3. Comparison: sdd-framework vs spec-runner vs Maestro

| Axis | **sdd-framework** | **spec-runner** | **Maestro** |
|---|---|---|---|
| Role | spec→code methodology for data pipelines | executor of tasks from a markdown spec | DAG orchestrator of coding agents |
| Artifact type | Framework (docs+skills+templates) | CLI service (Python 3.10+) | CLI/service (Python 3.12+) |
| What comes "out" | Generated pipeline code + DQ | Completed tasks from `tasks.md` | PRs from parallel worktree agents |
| Spec scheme | **8 gates, 10 artifact types** (BR→…→Gate 5) | **3 stages** (requirements→design→tasks) | no spec lifecycle; YAML workstream (DAG) |
| Statuses | `DRAFT/APPROVED` — as text in the header | `draft→approved→stale` — in frontmatter, programmatically | task statuses at runtime, not spec statuses |
| Gate enforcement | text in `SKILL.md` (the LLM reads `Status:`) | code (`spec.py`, `spec_governance: strict`) | pre-task validation commands |
| Activation | "skill zones" — automatic by folder | explicit CLI commands (`spec approve/status`) | `maestro run <yaml>` |
| Domain | narrow: data engineering (dbt/DWH/DQ) | general: any markdown tasks | general: coding tasks |
| Spec executability | human+AI bring it to APPROVED; AI generates code | the plan is built from the spec automatically | plan = DAG from YAML |
| Maturity | skeleton+demo, no real runs, `generated_code/` empty | Stable 2.0.0, R-04 closed | Stable Beta 0.4.0 |
| Primary author | Dmytro Honcharuk (external) | Andrei | Andrei |

### Key conclusion on the overlap

- **sdd-framework ↔ spec-runner** are conceptually misaligned but do NOT duplicate each other: spec-runner is an *engine* (validator+executor, gates in code), sdd-framework is a *process* (gates in the text of skills, domain-specific for data). sdd-framework could **use** spec-runner as the backend executor for its Gate 3/4, but there is no link right now — these are two independent worlds.
- **sdd-framework ↔ Maestro** barely overlap: Maestro is about running agents in parallel (DAG/worktree), sdd is about bringing a spec to APPROVED. The point of contact is hypothetical: Maestro could drive sdd skills as DAG nodes.
- The 3-stage scheme of spec-runner ⊄ the 8-gate sdd: you cannot reduce sdd to a spec-runner profile without losing domain specifics (source profiling, STTM, DQ gate-IDs, the platform layer). Conversely — spec-runner is NOT covered by sdd (sdd has no executing runtime).

---

## 4. Risks and misalignments

1. **Governance risk: the only project with an external primary author** (Dmytro Honcharuk). The entire rest of the ecosystem is yours. No contract vendoring, no link to the SSOT agents-catalog. Worth deciding: is this part of the ecosystem or a third-party fork of a methodology living in a checkout.
2. **`generated_code/` is empty, no real runs** — the framework has not been validated on a live product, only on the acme_pnl demo. The declared Gate 3–5 exist as docs but have not been passed end-to-end.
3. **Gates are not machine-enforced.** Unlike spec-runner (`spec_governance: strict` blocks a run in code), here a gate is an instruction in `SKILL.md` that the LLM is *supposed* to read. There is no hard stop: an agent can generate code with `Status: DRAFT` if the prompt is ignored.
4. **The notions "spec lifecycle" and "gate" are duplicated across three places** (sdd-framework, spec-runner, and sdd as a separate project in COWORK) without a shared vocabulary — a risk of terminological confusion (which is exactly what happened in your question).

---

## 5. Recommended actions

- **[COWORK_CONTEXT]** Record an explicit boundary in the registry: `sdd-framework` = **methodology (data domain, external author)**, `spec-runner` = **runtime executor (general)**. Add a line "do not duplicate: engine vs process" so the audit does not reopen the question.
- **[sdd-framework / decision]** Define the project's status in the ecosystem: (a) a third-party reference methodology, (b) a candidate for integration as a domain layer over spec-runner. If (b) — prototype: sdd's Gate 3/4 delegates execution to spec-runner (`tasks.md` + `spec_governance: strict`), gaining machine enforcement of gates instead of text-based enforcement.
- **[sdd-framework / maturity]** Run the acme_pnl demo end-to-end up to Gate 4 and commit the result into `generated_code/` — otherwise the framework remains unvalidated documentation.
- **[governance]** Clarify Dmytro Honcharuk's contribution: is this a single repo owner, is vendoring of cross-repo contracts needed (per the CLAUDE.md rule — "contracts are vendored inward, not referenced outward").

---

*Source files:* `sdd-framework/.claude/CLAUDE.md`, `sdd-framework/README.md`, `sdd-framework/templates/specs/`, `sdd-framework/specs/ingestion/SKILL.md`, `sdd-framework/specs/dq/DQFramework.md`, `sdd-framework/examples/`, `sdd-framework/infrastructure/local-stack/`; git log (35 commits, HEAD 62e3acc @ 2026-07-01).
