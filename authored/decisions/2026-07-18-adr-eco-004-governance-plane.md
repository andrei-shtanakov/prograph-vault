---
title: "ADR-ECO-004: Governance plane — one canon → machine registry → checks/gates → status surface"
type: adr
status: accepted
owner: Andrei
updated: 2026-07-19
---

# ADR-ECO-004: Governance plane

**Status:** Proposed (2026-07-18, Andrei) · **Date:** 2026-07-18
**Deciders:** Andrei (sole owner of the ecosystem today)
**Scope:** ecosystem-wide *governance* — the rights/restrictions layer (what may and
may not happen) and the responsibilities layer (who owns what). **Not** a new rule text;
this ADR decides how existing canon is *owned, enforced, evidenced, and kept honest*.
**Related:** [[repo-boundaries]] (`authored/rules/repo-boundaries.md`),
`authored/rules/git-workflow.md`, `authored/rules/cowork-output.md`, the KB constitution
(`../../CLAUDE.md`), [[2026-07-05-adr-spec-governance-layer]] (steward gate layer),
[[2026-07-01-adr-eco-003-agent-catalog]] (contract-authority canon), the umbrella
`workspace-manifest.toml` (repo set + pins), and dispatcher (read/control plane).

> **Companion artifact:** `authored/registry/governance.yaml` — the machine-readable
> *declaration* this ADR governs. Declared intent lives in `authored/` (human, PR-gated);
> *observed* enforcement maturity is written by drift-CI into `derived/` and dispatcher
> renders the diff. This authored-vs-derived split is the KB constitution applied to
> governance itself.

---

## Root cause (thesis first)

The ecosystem does **not** lack rules. Git workflow, repo boundaries, and the KB
constitution are all canonical text. What is missing is that most rules have **no formal
enforcement owner, no evidence type, and no blocking check**, and there is **no drift
check** tying the prose to reality. The split between "text canon" and "what is actually
enforced" is invisible and has to be reconstructed by hand.

**These are not N independent gaps. They are one missing plane.** The fix is not another
regulation — it is a single *governance plane*:

```
canon (rules text)  →  machine registry  →  checks / gates  →  status surface
   KB / repos             governance.yaml      CI / runtime        dispatcher
```

The one place this is already done right is **arbiter**: `invariants.toml` (rule as
**data**) + `rules.rs` (**one** enforcer) + tests (**drift check**). That is the template.
Every other pillar is dragged up to it, rather than inventing a new mechanism per gate.

---

## Decision

### D1 — Ownership is partitioned, not centralised

Governance is not owned by one repo. It is partitioned by *plane*, each plane with a single
canonical owner, one enforcement point, and one evidence type:

| Plane | Canonical owner | Enforcement | Evidence |
|---|---|---|---|
| Repo set, pins, aliases | `ai-orchestrators-workspace` (umbrella) | manifest-drift CI (`check-release-drift --strict`) | manifest entry |
| Git workflow | KB (canon) + each repo (digest) | GitHub **rulesets** / CI | PR metadata, merge actor |
| Repo boundaries / scope | KB | vendored boundary CI gate | changed-path report |
| Cross-repo contracts | producing repo | vendored-contract check | version / hash / schema |
| Roles / gates / approvals / waivers | **steward** | steward gate-check, later Maestro DAG | typed evidence |
| Runtime safety | arbiter, atp-platform | runtime code | decision logs / 403 / fallback |
| Read / control plane | dispatcher | read-model only; PR-only actions | status snapshot |

steward owns the *semantics* of roles/gates/evidence — **not** ownership in general. KB owns
rule *text*; the umbrella owns *composition*; producing repos own *contracts*; arbiter/ATP own
*runtime*. dispatcher only *shows* and *launches PR-only actions* — it is a read-model, never a
second SSOT (it carries `owner_role` as a pass-through string; steward validates it).

### D2 — Every rule answers four questions

A policy is not "done" until it answers: **who owns it · where is it enforced · what is the
evidence · what is the exception/waiver path.** These are the required fields of every
`governance.yaml` entry. A rule missing any field is, by definition, `documented`-only debt.

### D3 — Enforcement maturity is a typed ladder, declared vs observed

Every rule carries `enforcement_maturity ∈ { documented | advisory | ci-blocking | runtime }`.
The **declared target** lives in `authored/registry/governance.yaml`; the **observed** value is
written by drift-CI into `derived/`. dispatcher renders `declared vs observed` so the
aspiration-vs-reality gap becomes a first-class, visible artifact instead of a manual audit.

### D4 — CODEOWNERS is a transport, not a source of truth

`CODEOWNERS` "require code owner review" is **structurally unsatisfiable for a solo repo** — the
sole owner cannot approve their own PR. We stop treating it as enforcement. Instead:

- **steward owns** the semantics of who/what may merge and under which evidence.
- **`solo-mode` is a config value, not a special case.** The approver set is always evaluated;
  solo-mode = the set has one member and self-approval is explicitly permitted **and logged as
  such** (`reason` / evidence recorded).
- **Merge is always human-only in the default mode, verified via PR metadata / merge actor**, not
  via a review requirement that cannot be met.
- **git-workflow is enforced via GitHub rulesets** (require PR + green required checks + human
  actor) — satisfiable solo — **not** via required-owner-review.
- `CODEOWNERS required` only where it is satisfiable (high-risk/prod paths with an external
  reviewer, or a recorded waiver).

### D5 — One vendored enforcer, meta-checked by the umbrella

Enforcement is distributed the same way contracts are: **one reusable governance CI workflow,
vendored as a pinned copy into each subproject** (boundary / path-scope, vendored-contract-hash,
name-alias-resolve, `no _cowork_output in runtime`). The umbrella
`check-release-drift --strict` becomes the **meta-enforcer**: it verifies each repo's vendored
copy matches the canonical pin. This dogfoods the ecosystem's own "pinned copy inside" model and
turns 14×N ad-hoc scripts into one pinned artifact.

### D6 — Investment stance: correctness-now, social-dormant

For a single-maintainer ecosystem, enforcement must be cheap to run and cheap to change, and must
not create team-only ceremony.

- **Correctness gates (catch real breakage even solo) → build now, `ci-blocking`.**
- **Social gates (approvals, role matrix, waivers) → wired but dormant.** The role model
  (`@product`/`@architects`/`@qa`/`@tech-lead`/`@stream-owner`) exists as config that lights up
  when a second accountable party arrives — it is **not** run as a daily gate today (that would be
  pure overhead / theater, since almost everything = Andrei).

### D7 — An agent merger relocates governance into runtime, it does not wake the social layer

If the future merger is an **agent**, not a human, that is a category shift, not "a second
contributor lighting up social gates." An agent is not an accountable, independent party — it is
prompt-injectable and **shares a failure mode** with the agent that wrote the code, so its
"approval" is not evidence of human accountability. The social layer does **not** flip. Instead an
agent merger does three things, all inside the (already healthy) runtime family:

1. **Correctness becomes a hard precondition.** With the human removed from the loop, green CI must
   move from *necessary* to *sufficient*. So **correctness gates must be `ci-blocking` and complete
   for the authorized change-class BEFORE any agent gets merge authority.** D6's "correctness-now"
   is therefore the *precondition* of agent-merge, not something it replaces.
2. **A new concern: merge authority / provenance.** The `human_merge` evidence type ("a merge
   exists, actor ∈ humans, checks green") is broken by design for an agent. It needs a distinct
   `agent_merge` class with stronger preconditions (below), routed through the receipted runtime
   path (ATP `receipt_chain`), never a raw `git push`.
3. **It lands in runtime, not social.** `agent_merge` is purpose-gating (arbiter/ATP phase)
   extended to the merge action; steward owns its semantics; dispatcher surfaces it. It is **not**
   the role matrix.

**Invariants for `agent_merge`** (all four are required; they are the safety argument, not polish):

- **I1 — Authority is scoped by change-class.** Gate completeness is asymptotic: no automatable
  check set is *provably* complete for semantic/architectural/security judgment. So agent merge
  authority is granted **only within enumerated change-classes where green CI genuinely is
  sufficient** (dependency bumps that pass tests; doc-only within a schema; regenerated files).
  The classification itself is a gate; everything else routes to `human_merge`.
- **I2 — The authority root is agent-immutable.** An agent may **not** modify the artifacts that
  define its own authority — `governance.yaml`, branch rulesets, required-check definitions, its own
  identity/scope. Those are the highest-class protected paths, changeable only via `human_merge`.
  This is the injection→privilege-escalation backstop and is **cheap enough to land in batch 1**,
  before any agent gets even automated PR-authority.
- **I3 — Agent review is a gate, not an approval; independence requires an adversarially-different
  verifier.** A same-model/same-prompt reviewer buys ~zero independence. A separate attestable
  identity buys **provenance and revocability, not a second independent judgment**. `agent_merge`
  therefore *trades independent review for blast-radius control* — acceptable only in change-classes
  where judgment is not the safety-critical variable (see I1). An adversarial verifier (different
  model, isolated prompt, refute-framing) may serve as one more required-check, never as the sole
  authority.
- **I4 — Revocation needs a detection loop, not just a kill-switch.** Authority is only "revocable"
  if something *watches* agent merges (dispatcher surfaces `agent_merge` events + anomalies) and can
  trigger revocation, ideally auto-revoke on gate-anomaly. A kill-switch never pulled is theater.

**Default mode:** an agent gets **PR-authority** (open/update PRs, answer Copilot review) — **not**
merge authority. Autonomous `agent_merge` is enabled only when I1–I4 hold. (Honesty note: even the
default is only protective while the human merge-review stays meaningful; a solo maintainer flooded
with agent PRs degrades to rubber-stamping — argue for low/batched agent PR volume, or gates good
enough that rubber-stamping is acceptable.)

---

## Consequences — sequencing (leverage × cost)

**Batch 1 — correctness-now, `ci-blocking` (catch real breakage even solo):**

1. **name/alias-resolve gate** — manifest names resolve to real dirs/remotes; dispatcher hardcodes
   match the manifest (closes "green PR ≠ working layout", `_cowork_output/2026-07-17-workspace-rename-risks.md`).
2. **boundary / path-scope gate** — the missing lever (c) of [[repo-boundaries]] §5: PR touches only
   its own repo; no `_cowork_output/` reference in runtime/shipped code; vendored contract == pinned
   hash. Shipped as the **vendored governance workflow** (D5).
3. **authority-root immutability (I2)** — authority-defining paths are agent-immutable protected
   paths. Cheap; foundational for any later automation.
4. **git-workflow on GitHub rulesets** (D4) + dedup the per-repo CLAUDE.md digest via generate+check.

**Batch 2 — visibility + drift:**

5. Extend `check-release-drift`: `[tools.*]` pin validation, `_cowork_output` graduation/duplicate
   gate.
6. Minimal `authored/registry/governance.yaml` → drift-CI writes observed maturity to `derived/` →
   dispatcher **governance view** (declared vs observed).

**Later — needs real build:**

7. `human_merge` typed evidence (GitHub API: merge exists, actor ∈ humans, checks green) → closes
   "human approval recorded not machine-expressible."
8. `agent_merge` evidence type in steward with I1–I4 + a narrow, revocable bot identity + per-merge
   receipt/provenance.
9. WS-006 gates-in-DAG on Maestro — **only if** merge becomes a DAG step, and then it consumes the
   same steward evidence types (`human_merge` / `agent_merge`), inventing no parallel model.

The full social apparatus stays dormant throughout.

---

## Non-goals

- A new rule text or a rewrite of existing rules' prose (only add the four required fields).
- Running the role matrix as a daily gate for a solo maintainer.
- Making dispatcher a second SSOT (it renders declared-vs-observed; it does not own truth).
- Enabling autonomous `agent_merge` before I1–I4 hold.

## Open questions

- Exact change-class taxonomy for I1 (what is "green-sufficient").
- Whether `human_merge` evidence is verified live against the GitHub API or captured at merge time
  into `receipt_chain`.
- Where the adversarial verifier (I3) lives — a dispatched ATP/arbiter check vs a dedicated agent.

---

## Status & rollout log (addendum 2026-07-19)

Status → **Accepted** (batch-1 shipped). This log is the record of record for "good enough vs
continue" so the call is made from the doc, not memory.

### Batch-1 — SHIPPED (advisory), enforcement pending

Vendored governance gate (D5) deployed fleet-wide. One reusable `governance-gate.yml` in the
umbrella (`ci/governance/` scripts) + a byte-identical thin caller in **13 runtime repos** and a
KB-config caller in prograph-vault, all pinned to the protected tag **`governance-v1`**. Gates live:
GOV-003 no-cowork-in-runtime, GAP-7 manifest name/alias resolve (umbrella `manifest-drift.yml`),
GOV-009/I2 authority-root guard (prograph-vault, advisory).

**advisory → required transition (the last mile).** The gate *runs* on every PR but does not *block*
until `governance / gate` is added as a **required status check** in each repo's branch ruleset
(GitHub UI). Enforcement rollout order: add required on ONE repo → land a deliberately-failing test
PR → confirm it blocks → roll out to the remaining 13. **Verified safe to enforce now:** CI checks
out only tracked files, `.claude/settings.local.json` is gitignored in every repo, and
`governance / gate` already ran green on all 14 merged caller PRs — GOV-003 is 0-hit on every
repo's tracked tree (checked 2026-07-19). The `.claude/` false positives are a *local working-tree*
artifact only; they never reach the CI checkout, so the batch-2 `ls-files` fix is **not** a
prerequisite for the required-check rollout.

### Batch-2 — scope (ordered)

1. **`ls-files` scan** — GOV-003 scans `git ls-files` instead of walking the working tree, so local
   runs match CI exactly (drops `.claude/`, `.venv`, build-dir false positives). Local-DX + belt-and-
   suspenders; independent of the required-check rollout.
2. **`strict`-split** — split `authority-strict` from `strict` so `strict` also governs the runtime
   path; retires the currently-dead `strict: true` on `authority-guard:false` callers (kept uniform
   deliberately, forward-compatible with this change).
3. **Meta-enforcer** — a `check-release-drift` companion that verifies every caller pins the
   *current* governance tag. **MUST NOT hardcode a version** (else a vN→vN+1 rollout makes the
   enforcer itself the source of false drift). It reads the current version from the SSOT below.
   Deferred until the versioning policy is exercised by a real v2.

### Tag versioning policy (governance-vN)

- **Immutable, protected tags.** Each batch that changes `governance-gate.yml` or `ci/governance/`
  scripts → a new `governance-vN` on the resulting umbrella `main` commit. Tags are never moved or
  deleted (audit trail); the `governance-*` tag ruleset enforces this. Superseded tags stay valid
  but unused.
- **Callers pin `@governance-vN`** (both the `uses:` ref and `umbrella-ref:`). Since all 14 callers
  are byte-identical (per config class), a version bump is a mechanical two-token change.
- **SSOT for "current version":** the active `governance-vN` is recorded in one place (the umbrella
  `workspace-manifest.toml` `[tools]` section is the intended home). Rollout and the future
  meta-enforcer both read it; nothing hardcodes a version.
- **Rollout shape (v2+):** the plumbing (`workflow_call` + cross-repo checkout) is proven, so no full
  pilot. Instead: **dry-run the new scripts against all tracked trees → 1-repo canary (bump + confirm
  green) → batch the remaining 13.** Green-by-construction because the dry-run precedes any bump.

### Deferred (point 3 of the roadmap)

Governance registry drift-CI + dispatcher declared-vs-observed view; `human_merge`/`agent_merge`
evidence types (steward, I1–I4); WS-006 gates-in-DAG on Maestro. Revisit after batch-2.
