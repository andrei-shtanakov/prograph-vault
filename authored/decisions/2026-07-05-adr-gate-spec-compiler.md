---
title: ADR: Consolidate gated spec authoring in spec-runner (Maestro delegates)
type: adr
status: proposed
owner: Andrei
updated: 2026-07-05
---

# ADR: Consolidate gated spec authoring in spec-runner (Maestro delegates)

> Date: 2026-07-05 · Status: **Proposed** (supersedes the same-day draft "standalone gate-compiler")
> Author: Andrei / Claude
> Related: [[idea-maestro-workstream-framework]] (2026-07-03), spec-runner gated-generation,
> sdd-framework (carrier of the gates idea), `maestro/_vendor/obs.py` (the vendoring pattern)

## TL;DR

1. **We do not build a separate engine.** Previously a standalone `gate-spec-compiler` with vendoring
   of `spec.py` was considered. Rejected: it creates **a third spec author** unaware of the two
   existing ones, and multiplies copies of the format.
2. **The coherence problem is already real.** `Maestro/maestro/decomposer.py` **itself** generates
   `tasks.md` via a built-in `SPEC_GENERATION_PROMPT` (a hardcoded copy of the format, one-shot, no
   gates). In parallel, spec-runner builds its own `plan --gated`. The two spec authors do not know
   about each other — exactly the risk Andrei articulated.
3. **The decision — consolidation into spec-runner as the single authoring engine.** We add
   configurable **gate profiles** there. Maestro's `decomposer` stops writing `tasks.md` itself and
   **calls spec-runner** per-workstream.
4. **The dependency is one-directional and acyclic:** Maestro → spec-runner (already the case; Maestro
   already shells into spec-runner and vendors its contracts). spec-runner stays Maestro-agnostic — it
   does not write "specs for Maestro", it writes a spec; Maestro lays out N of them.
5. **A net win, not a new coupling:** the format duplication (`FORMAT.md` ⟷ prompt string in
   decomposer.py) is removed rather than a third implementation being added. There is no need to vendor
   `spec.py`.

---

## Context: why standalone was rejected

Andrei wanted a utility that runs a spec through gates (inspired by sdd-framework) and outputs an
executable spec for spec-runner or Maestro mode 2. The first draft proposed a standalone engine with a
shared IR and vendoring of `spec.py`. Andrei objected on the merits:

> "then it will turn out that Maestro knows nothing about the fact that spec-runner writes specs, and
> spec-runner does not know that it also needs to write specs for Maestro… if we can avoid this, I'm
> for it — and not at all for a separate engine."

A code check confirmed that **the duplication already exists**:

| Fact | File | What it means |
|---|---|---|
| Maestro writes `tasks.md` itself | `maestro/decomposer.py:85` `SPEC_GENERATION_PROMPT` ("spec-runner parses this EXACT format") | A copy of the spec-runner format lives in a Maestro prompt string |
| Generates `req/design/tasks` one-shot | `decomposer.py:327` `generate_spec()` | Authoring without gates, in parallel to spec-runner's gated mode |
| spec-runner builds its own gated authoring | `spec-runner .../2026-07-01-gated-spec-generation.md` | A second, independent spec author |
| Maestro already vendors from spec-runner by discipline | `maestro/_vendor/obs.py` ("Do not edit locally… re-copy and bump marker"), `maestro/spec_runner.py` (pinned version, integration boundary) | The Maestro→spec-runner integration channel already exists |

Conclusion: adding a standalone engine would worsen the fragmentation. We need to **reduce it to a
single owner**.

---

## Decision

### The single authoring engine — spec-runner

spec-runner already owns `FORMAT.md` and builds `plan --gated`. We extend it:
- **Gate profiles** — generalize the hardcoded `STAGES=(requirements, design, tasks)` into a loadable
  profile (`gate-profile.yaml`: stage id, template, validation rule, upstream). Profiles:
  `generic-feature`, `refactor`, and optionally domain-specific ones (inspired by sdd, but with our
  own text).
- Everything else (frontmatter `draft/approved/stale`, atomic writes, validation, approval,
  stale-cascade) already exists — we do not touch it.

### Maestro delegates authoring downward

- `decomposer.generate_spec()` **no longer uses** the built-in `SPEC_GENERATION_PROMPT`. Instead it
  calls spec-runner in the workstream's directory (`spec-runner plan [--gated] --profile <p>`), just as
  it already calls it for execution.
- **The copy of the format is removed** from the Maestro prompt string → one format SSOT (spec-runner).
- **Decomposition stays in Maestro** (`decomposer.decompose()`): 1 project → N workstreams with
  scope/depends_on/branch. This is the `project.yaml` format — owned by Maestro.

### Gate hierarchy = altitude

```
[Maestro]      decomposition gate:   project.yaml → N workstreams   ← owner of project.yaml
                     │  per workstream: call downward
                     ▼
[spec-runner]  authoring profile:    requirements → design → tasks  ← owner of the spec format
                     │  (frontmatter state, validation, approval)
                     ▼
[spec-runner]  execution:            executes the approved tasks.md
```

One authoring run = one spec-runner spec = one workstream. Multi-stream is produced by the layout in
Maestro, not by "a second format" inside spec-runner.

### Boundary and vendoring

- The integration is a **subprocess call** to spec-runner (the ready mode-2 pattern), not an import of
  logic.
- Vendor **only the thin read contracts** (as already done: `_vendor/obs.py`, `spec_runner.py`). The
  authoring logic (`spec.py`) is **not** vendored — it stays with the owner.
- Contract updates follow the existing discipline: marker + re-copy + bump.

---

## Consequences

**Pros:**
- One spec-format SSOT; the existing duplication is removed (decomposer prompt ⟷ FORMAT.md).
- The Maestro → spec-runner dependency is one-directional, acyclic, and already exists.
- spec-runner stays Maestro-agnostic — correct layering, zero knowledge "upward".
- Gates are enforced by spec-runner code (machine enforcement), not by text (unlike sdd).
- No new project in the polyrepo.

**Cons / risks:**
1. **Regression risk in Maestro mode 2** when replacing `generate_spec()` with a subprocess call — we
   need contract tests that spec-runner authoring produces a tasks.md that the current Maestro
   execution pipeline parses. Golden files.
2. **The version pin** of spec-runner in Maestro (`maestro/spec_runner.py`) must also cover the
   authoring contract, not only the state reader.
3. **Gate profiles in spec-runner** — a risk of bloating spec-runner's scope; keep profiles as data
   (YAML + templates), not code.
4. **Decomposition as a gate** stays for now a one-shot Claude call in Maestro; making it gated
   (scope-overlap validation already exists in `preflight`/`validate`) is a separate phase.
5. **The sdd license** is not confirmed (there is no LICENSE in `sdd-framework/`) — we borrow only the
   *idea* of gates, not the skill texts, until confirmed with Dmytro Honcharuk.

---

## Recommended actions

- **[spec-runner]** Generalize `STAGES` into a loadable gate profile (data, not code). Start with the
  `generic-feature` profile = the current three stages — zero behaviour change, only extraction into
  config.
- **[Maestro]** Replace `decomposer.generate_spec()` + `SPEC_GENERATION_PROMPT` with a call to
  spec-runner authoring; remove the built-in copy of the format. Update the pin in
  `maestro/spec_runner.py`.
- **[contracts]** Golden tests: spec-runner authoring → `tasks.md` → the Maestro execution parser
  (`maestro/spec_runner.py` + spec-runner's `task.py`) — both green on the same file.
- **[phase 2]** Make the decomposition gate in Maestro gated (scope-overlap validation → approval of
  `project.yaml` before orchestrate; `maestro validate --strict` already exists as a basis).
- **[governance]** Clarify the sdd-framework license before borrowing any text.
- **[COWORK_CONTEXT / integration map]** Record the new edge: "Maestro decomposer → spec-runner
  authoring (subprocess)", mark the removal of the format duplication.

---

*Sources:* `Maestro/maestro/decomposer.py` (`SPEC_GENERATION_PROMPT`, `generate_spec`),
`Maestro/maestro/spec_runner.py`, `Maestro/maestro/_vendor/obs.py`, `Maestro/maestro/orchestrator.py`,
`spec-runner/spec/FORMAT.md`, `spec-runner/docs/superpowers/plans/2026-07-01-gated-spec-generation.md`,
`sdd-framework/.claude/CLAUDE.md`.
