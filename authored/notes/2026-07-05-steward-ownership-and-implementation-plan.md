---
title: steward — ownership & implementation plan
type: note
status: living
owner: Andrei
updated: 2026-07-05
---

# steward — ownership distribution and implementation plan

> Date: 2026-07-05 · Role: TPM/architect · Consolidates ADRs: consolidation, governance-layer, dogfood.
> "Team" = repo owner (today many = Andrei; contract seams matter even in solo).
> Separately — the runtime governance roles (CODEOWNERS).

## TL;DR — accepted ownership decisions

1. **DEC-006 closed:** `gate-check` and the entire governance layer are owned by the **new repo `steward`**, NOT
   spec-runner. steward imports SpecMeta from spec-runner — this is not a "second engine" (it reimplements
   nothing and does not duplicate formats), but a thin conductor layer.
2. **The two levels of "profile" are split across owners:** spec-runner owns the *within-spec stages*
   (C1: `lite`=req/design/tasks); steward owns the *inter-artifact DAG* (charter→…→decomposition).
3. **spec-runner does NOT grow into governance** — this is an ownership guardrail: it remains the engine
   of authoring+executing a single spec. Everything "team/multi-artifact" belongs to steward.
4. **Formats stay with their owners:** `tasks.md`+SpecMeta → spec-runner; `project.yaml` →
   Maestro; deploy → deployer; quality gates → atp. steward only *orchestrates them by delegation*.
5. **Debt is paid down by the owner:** the format duplicate in `Maestro/decomposer.py` is eliminated by the
   Maestro team (C4), not steward.

---

## Responsibility matrix (who owns / whom to ask / what it emits)

| # | Work item | Owner (repo) | Consulted | Output contract |
|---|---|---|---|---|
| C1 | STAGES → loadable profile (within-spec) | **spec-runner** | steward | Stage-profile + SpecMeta (stable) |
| C2 | SpecMeta extension: `owner_role` + human approver | **spec-runner** | steward | SpecMeta v-next |
| G1 | Rich artifact-DAG profiles (`lite`/`team`) | **steward** | spec-runner, @architects | DAG profile schema |
| G2 | `gate-check` linter (completeness/traceability/status↔git/stale) | **steward** | spec-runner (SpecMeta), infra (CI) | `gate-check` CLI + exit codes |
| G3 | git approval: CODEOWNERS + CI job + branch protection | **steward** + repo-infra | @tech-lead | Gate CI contract |
| E1 | Emitter `decomposition → project.yaml` | **steward** (emit) + **Maestro** (format) | — | `project.yaml` schema |
| E2 | Emitter `WS → spec-runner authoring` | **steward** (emit) + **spec-runner** | — | `tasks.md` + `plan --gated` CLI |
| C4 | Maestro decomposer → delegation (remove the duplicate) | **Maestro** | spec-runner, steward | Call to spec-runner authoring |
| V1 | Bundle status panel (read-only) | **dispatcher** | steward | on-disk artifact + status |
| Q1 | Gate 2/4 — quality/acceptance | **atp** | steward, @qa | Acceptance/DQ gate-ID |
| D1 | Gate 5 — deployment (author-not-execute) | **deployer** | steward, Ops | Deploy contract |
| M1 | Methodology/profile texts (from sdd) | **steward** | **sdd (Dmytro)** — license | License clearance |

---

## Contract seams (where teams are obliged to agree)

This is the main value of the distribution; each seam is versioned and covered by a golden test **at the
format owner**, and the consumer tests against it.

| Contract | Owner | Consumers | Risk on drift |
|---|---|---|---|
| **SpecMeta** (frontmatter, `spec_stage`, statuses) | spec-runner | steward, Maestro | gate-check and Maestro read the state differently |
| **`tasks.md`** format | spec-runner | Maestro, steward (E2) | Broken generation of the leaf spec |
| **`project.yaml`** schema | Maestro | steward (E1) | Emitter emits an invalid config |
| **`gate-check` CLI** (flags, exit 0/1/2, `--no-fs`) | steward | CI of all repos that adopted governance | Unstable gate in CI |
| **agent-id / approver** convention | ecosystem SSOT (atp `agents-catalog`) | all | Authorship/approval desync |

> Observation: Maestro already has seam discipline (`maestro/_vendor/obs.py` marker + pinned version
> in `maestro/spec_runner.py`) — extend the same pattern to SpecMeta/gate-check.

---

## Implementation plan (sequence by owner)

### Phase 0 — decisions and clearance (owner: Andrei/TPM)
- Approve the ownership matrix (this document).
- sdd license: request from **Dmytro Honcharuk** — until an answer, steward takes only the *idea* of the gates (M1).
- Pin DEC-006 in COWORK_CONTEXT (steward — new repo, role "spec governance").

### Phase 1 — spec-runner provides a stable foundation (owner: spec-runner)
- **C1**: STAGES → profile (`lite`=current 3, zero behavior change). Spec ready:
  `_cowork_output/spec-runner-c1-stages-profile/spec/`.
- **C2**: SpecMeta + `owner_role` + human approver.
- **Handoff → steward:** freeze the SpecMeta+stage-profile contract (version + golden).

### Phase 2 — steward MVP on a single pilot (owner: steward; depends: Phase 1)
- **G1** rich-DAG profiles; **G2** `gate-check` MVP (completeness+traceability+status↔git, `--no-fs`,
  CI); **G3** CODEOWNERS+branch protection on the pilot repo.
- G2 spec ready: `_cowork_output/spec-governance-dogfood/workstreams/WS-002-gate-check/spec/`.
- **Handoff:** stable `gate-check` CLI contract for the other repos.

### Phase 3 — close the loop and pay down the debt (owners: Maestro + steward; depends: Phase 1)
- **C4** (Maestro): decomposer delegates to spec-runner authoring, remove `SPEC_GENERATION_PROMPT`.
- **E1/E2** (steward): emitters; `decomposition→project.yaml` is already contract-checked
  (`_cowork_output/spec-governance-dogfood/emitter-contract-check.md`), `WS→spec-runner`.
- **On the side (Maestro):** fix `validate` — a dangling `depends_on` (I1).

### Phase 4 — ecosystem integration (owners: dispatcher/atp/deployer; depends: Phase 2)
- **V1** dispatcher: bundle status panel. **Q1** atp: quality gates. **D1** deployer: Gate 5.

---

## Runtime governance roles (CODEOWNERS)

Separate from build ownership — who *approves* which artifact in a team's work:

| Artifact | CODEOWNERS role |
|---|---|
| `charter`, `requirements` | `@product` |
| `requirements`, `design` | `@architects` |
| `acceptance` | `@qa` |
| `decomposition` | `@tech-lead` |
| leaf `task` specs | `@stream-owner` |
| deploy (Gate 5) | `Ops` |

**Solo mode:** the roles collapse into a single owner + `solo_auto_approve` (anti-ceremony).

---

## Ownership risks

1. **Most "teams" today = Andrei** → the distribution is notional for now. The value is in the
   contract seams: they prevent drift when/if a second pair of hands appears. Don't over-complicate
   the process while the team is one person.
2. **sdd — external author (Dmytro), license not confirmed** → M1 is blocked until clearance; this is
   the only external ownership dependency.
3. **Temptation to merge governance into spec-runner** (fewer repos) → consciously rejected: it would
   overload the executor. The guardrail — governance lives in steward.
4. **Contract drift between repos** → each seam: version + golden test at the format owner,
   pinned consumption (the `maestro/_vendor` pattern).

---

## Recommended actions

- **[Andrei/TPM]** Approve the ownership matrix and DEC-006; add steward to COWORK_CONTEXT as a repo
  with the role "spec governance", note the edges to spec-runner/Maestro/dispatcher/deployer/atp.
- **[Andrei→Dmytro]** Request the sdd-framework license (unblocks M1).
- **[spec-runner]** Phase 1: C1 (spec ready) → C2; freeze the SpecMeta contract for steward.
- **[Maestro]** Phase 3: C4 (delegation) + I1 (validator bug).
- **[steward]** Phase 2 after Phase 1: G1/G2/G3 on a single pilot.
- **[dispatcher/atp/deployer]** Phase 4: connect to the stable gate-check contract.
