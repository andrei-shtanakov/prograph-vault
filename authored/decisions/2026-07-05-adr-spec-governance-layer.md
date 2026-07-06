---
title: ADR: Spec Governance Layer — multi-artifact gated authoring
type: adr
status: proposed
owner: Andrei
updated: 2026-07-05
---

# ADR: Spec Governance Layer — multi-artifact gated authoring for complex/team tasks

> Date: 2026-07-05 · Status: **Proposed**
> Author: Andrei / Claude
> Builds on: [[project-gated-spec-authoring-consolidation]] (the lower layer, same day)
> Related: [[idea-maestro-workstream-framework]], [[reference-scope-linter-oss]],
> [[idea-deployer-subproject]], sdd-framework (donor of the gate set)

## TL;DR

1. **A new layer on top of execution specs.** spec-runner/Maestro today cover the simple
   "one spec → execution". For complex/team tasks we need a **governance layer**: N artifacts, each
   with an approval gate, upstream dependencies, and traceability.
2. **The gate set — from sdd, stripped of the data domain.** The 8 sdd gates map 1:1 onto generic
   software and — importantly — **onto the existing ecosystem projects** (Maestro=decomposition,
   spec-runner=leaf tasks, deployer=deployment, atp=quality reference). The governance layer
   *conducts* them, it does not execute — thin glue, not a monolith.
3. **Approval and roles — on git, not bespoke.** Approval = PR review+merge; roles = CODEOWNERS
   (the architect owns `specs/architecture/`, QA owns `specs/test/`); enforcement = branch protection +
   CI. Frontmatter `Status: APPROVED` is a machine-readable mirror of git state. No own
   identity/RBAC/locks — we reuse battle-tested team infrastructure.
4. **"New code" is minimal:** (a) the artifact-DAG profile as data; (b) a CI **gate-checker**
   (completeness/traceability/stale linter — built on codeowners-validator/repolinter, see
   [[reference-scope-linter-oss]]); (c) compilation of the approved bundle downward — by delegation to
   spec-runner/Maestro (already decided in the consolidation ADR). The state core is spec-runner's
   SpecMeta, generalized from "stages" to "a graph of artifacts".
5. **The main risk is ceremony.** 8 gates for everything would kill speed. Therefore the DAG is
   **depth-profileable**: `lite` (req→design→tasks) for simple work, `team` (the full sdd-derived set)
   for complex work. The sdd set is the `team` profile, not the only mode.

---

## Problem

Andrei: the value of sdd is that a spec passes through a **broad** set of stages, each of which must be
**approved**; this is not just design+tasks. The current authoring (spec-runner `req→design→tasks`,
Maestro one-shot decomposer) is fine for the relatively simple. The goal is complex tasks and
**teamwork**: several roles author/approve different artifacts, and a gate is a handoff between people,
not just validation.

Neither spec-runner nor Maestro provides this: they have no roles, no human approval, no
multi-artifact lifecycle. We need a layer **above** execution.

---

## Decision

### Layering (governance builds on top, does not replace)

```
[GOVERNANCE]  artifact-DAG (profile) + approval gates (git-PR/CODEOWNERS) + tracing
      │  approved bundle
      ▼  compilation downward = DELEGATION (consolidation ADR)
[EXECUTION-SPEC]  spec-runner (tasks.md)   ·   Maestro (project.yaml)
      ▼
[EXECUTION]  spec-runner exec · Maestro orchestrate · deployer · ...
```

### The gate set: sdd → generic software → owner in the ecosystem

| sdd gate | Generic-software artifact | Approved by (CODEOWNERS role) | Execution delegated to |
|---|---|---|---|
| Gate BR | **Charter** — problem, scope, success criteria, stakeholders | Product / Lead | — |
| FRD | **Requirements** — functional + non-functional, acceptance with IDs | Product + Architect | — |
| Gate 0a | **Tech/Platform Selection** — stack, ADR decisions | Architect | — |
| Gate 0b | **System Assessment** — current code/interfaces/constraints (analogue of source-assessment) | Architect / Tech Lead | — |
| Gate 1 | **Design Stack** — Architecture + Interface/Contract specs + Data model | Architect + component owners | — |
| Gate 2 | **Test & Acceptance Baseline** — test strategy, quality gates with IDs (analogue of DQ) | QA | atp-platform (quality reference) |
| — (new) | **Decomposition** — split into workstreams (scope/deps) | Tech Lead | **Maestro** (`project.yaml`) |
| — (new) | **Task Spec** (per workstream) — req→design→tasks | stream owner | **spec-runner** (`tasks.md`) |
| Gate 3 | **Code Review** — PR review against the spec | Reviewers (CODEOWNERS) | git-PR |
| Gate 4 | **Testing** — CI green, acceptance pass | QA | CI + atp |
| Gate 5 | **Deployment** — author-not-execute, arbiter-gated | Ops | **deployer** ([[idea-deployer-subproject]]) |

Conclusion: the governance layer is a **conductor of gates**, and each gate is executed by its natural
owner. This reinforces "thin glue", not a second engine.

### Approval/roles/enforcement on git

- **An artifact** = file(s) in the spec-repo/`spec/` with frontmatter (`spec_stage`, `status`,
  `owner_role`, `approved_by`, `traces_to`).
- **Approval** = a PR reviewed by the CODEOWNERS role of the given artifact → merge into `main`.
- **Roles** = `CODEOWNERS` (`specs/architecture/ @architects`, `specs/test/ @qa`, ...).
- **Enforcing upstream-before-downstream** = a CI job `gate-check` on each PR: a downstream artifact
  does not pass until all upstreams are `APPROVED` (merged). + branch protection on downstream folders.
- **Stale cascade** = when a change to an approved upstream artifact is merged, CI marks downstream
  stale (reopen/flag) — a generalization of spec-runner's stale mechanics onto a graph.
- **Frontmatter Status** = a machine-readable mirror of git: an approved artifact must be on `main` and
  have an approval record. spec-runner already has SpecMeta (`approved_by/at`) — we extend it with
  `owner_role` + a human approver alongside the agent-id.

### What we actually write (minimum)

1. **The artifact-DAG profile** (data): node = artifact (template, owner_role, upstream, validation
   rule). Profiles `lite` and `team`. sdd-derived = `team`.
2. **The `gate-check` linter** for CI: DAG completeness, traceability (each downstream criterion
   references an upstream ID), Status↔git consistency, stale detection. Base —
   codeowners-validator / repolinter / MegaLinter ([[reference-scope-linter-oss]]).
3. **Compilation downward**: approved bundle → delegation (Maestro decompose + spec-runner authoring),
   as in the consolidation ADR. The governance layer does **not** write `tasks.md`/`project.yaml`
   itself.

### Where it lives (open point for implementation)

The state core (SpecMeta, validation, stale) already belongs to spec-runner — so it is logical to make
`gate-check` and the DAG profiles **an extension of spec-runner's governance part** (not the execution
part), reusing the frontmatter machine. The alternative is a thin separate linter repo that reads
spec-runner's SpecMeta. Decide when writing the implementation spec; in any case, do **not** spawn a
second state engine.

---

## Alternatives considered (per Andrei's choices)

| Axis | Chosen | Rejected and why |
|---|---|---|
| Approval mechanism | git-PR + CODEOWNERS + CI | Bespoke frontmatter (reinventing RBAC/locks; the gate is enforced by an LLM, not code). Issue tracker (Linear frozen ~2026-04-17, external dependency) |
| Artifact set | Start from sdd (8 gates, de-domained) | A fixed generic set (less flexible); a clean config-DAG from scratch (no ready "rich" example) |

---

## Consequences

**Pros:** closes the gap "complex + team", which no one has; approval/roles on battle-tested git
infrastructure; each gate is executed by its natural owner; traceability and stale cascade are
machine-driven; reuses SpecMeta + OSS linters; not a monolith.

**Cons / risks:**
1. **Ceremony.** 8 gates for a trifle is the death of speed. The `lite` profile and the rule "depth by
   task size" are mandatory; otherwise we repeat the main failure of SDD processes.
2. **CODEOWNERS roles require a real team.** Solo mode degenerates into self-approval — then the gates
   must collapse (the `lite` profile, auto-approval with a single owner).
3. **A stale cascade over a graph is harder than over a linear chain** — we need a careful DAG traversal
   and contract tests for the linter.
4. **A dual source of approval truth** (git PR ⟷ frontmatter Status) — CI must reconcile them,
   otherwise they desync. git is primary, frontmatter is the mirror.
5. **The sdd license is not confirmed** (LICENSE is absent) — we borrow *the gate structure as an idea*,
   not the template texts, until confirmed with Dmytro Honcharuk.

---

## Recommended actions

- **[phase 0 — skeleton]** Define the `team` profile (sdd-derived, the table above) and `lite` as data;
  describe the artifact frontmatter schema (an extension of SpecMeta: `owner_role`, a human approver).
- **[phase 1 — enforcement]** The `gate-check` linter (completeness + traceability + Status↔git) on top
  of repolinter/codeowners-validator; wire it as a CI job + branch protection on downstream folders.
  Start with a single pilot project.
- **[phase 2 — compilation downward]** Link the approved bundle to the consolidation ADR:
  Decomposition→Maestro, Task Spec→spec-runner (by delegation). Golden contract tests.
- **[phase 3 — visibility]** dispatcher: a lifecycle state panel (who is stuck on whose approval) — it
  already reads on-disk artifacts read-only.
- **[governance]** Clarify the sdd-framework license before borrowing template texts.
- **[COWORK_CONTEXT]** Register the governance layer; note the edges: governance→Maestro,
  governance→spec-runner, governance→deployer (Gate 5), governance→atp (Gate 2/4).

---

*Sources:* `sdd-framework/.claude/CLAUDE.md` (8 gates), `spec-runner/spec/FORMAT.md`,
`spec-runner .../2026-07-01-gated-spec-generation.md` (SpecMeta), `Maestro/maestro/decomposer.py`
(decomposition), memory [[reference-scope-linter-oss]], [[idea-deployer-subproject]],
[[project-gated-spec-authoring-consolidation]].
