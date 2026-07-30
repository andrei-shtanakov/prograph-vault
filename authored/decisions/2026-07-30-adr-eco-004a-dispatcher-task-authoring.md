---
title: "ADR-ECO-004a: Dispatcher may originate task-authoring proposals — human-initiated, PR/issue-only, never a task SSOT"
type: adr
status: proposed
owner: Andrei
updated: 2026-07-30
---

# ADR-ECO-004a: Dispatcher's authoring authority

**Status:** Proposed (2026-07-30, Andrei) · **Date:** 2026-07-30
**Deciders:** Andrei (sole owner of the ecosystem today)
**Scope:** the read/control plane row of ADR-ECO-004 D1 — dispatcher only
**Type:** Amendment to `decisions/2026-07-18-adr-eco-004-governance-plane.md` (ADR-ECO-004)
**Related:** [[2026-07-28-adr-eco-006-cross-repo-issue-inbox]] (the issue channel this
authority uses), `authored/rules/repo-boundaries.md`, `authored/rules/git-workflow.md`,
dispatcher `#93`/`#94`/`#95` and github-checker `#14` (the S1 slice this builds on),
`prograph-vault#54` (the request)

> This amendment widens **D1's read/control-plane clause** so dispatcher may *originate*
> task-authoring proposals, not only show state and launch actions on work that already
> exists. It answers one owner question (2026-07-30): what exactly may the console do when
> the operator wants to turn a discussed idea into a routed task — and, more importantly,
> what it still may not do. D1's core claim is unchanged: dispatcher is never a second SSOT.

---

## TL;DR

Dispatcher may originate task-authoring proposals **only** through explicit human actions
and repository-owned PR/issue channels. It stores no authoritative task state, directly
edits no live working tree, merges nothing automatically, and executes no authored task.
The target repository remains the SSOT; repeated requests are idempotent or visibly
deduplicated; every attempt is audited.

---

## Context

ADR-ECO-004 D1 assigns dispatcher the read/control plane with the enforcement
"read-model only; PR-only actions", and closes with:

> dispatcher only *shows* and *launches PR-only actions* — it is a read-model, never a
> second SSOT (it carries `owner_role` as a pass-through string; steward validates it).

The merge-gate console (S1, shipped 2026-07-30) fits that clause without strain: merging
is a PR-only action taken on an explicit human click, delegated to `github-checker`, and a
human still merges. No amendment was needed and none was taken.

S2 — task authoring and routing — does not fit. Turning a discussed idea into an issue in
the target repo, or into a `TODO.md` item proposed as a PR, means dispatcher **originates**
work rather than acting on work that already exists. That is a different verb, and D1's
current wording does not cover it.

The alternative to amending is drift: shipping S2 and treating "launches PR-only actions"
as though it already meant "may create the thing being acted on". That reading is available
and would be wrong — the honest move is to widen the clause deliberately, with the limits
written down at the same time.

---

## Decision

### D1a-1. Authority: dispatcher may propose work, never accept it

Dispatcher may originate a task-authoring proposal — an issue in the target repo per
ADR-ECO-006, or a PR that adds a `TODO.md` item. It may **not** decide that the work is
accepted. Acceptance stays exactly where ADR-ECO-006 already puts it: in the target's own
`TODO.md`, written by the target's owner. A proposal that is never accepted is a normal
outcome, not a failure state.

### D1a-2. Human-click and PR/issue-only

Every authoring action requires an explicit human click in the UI, carries the existing
action token, and reaches the target only as a PR or an issue. No background trigger, no
scheduled authoring, no authoring under a coding session's identity. This is the same
boundary the whitelist mutations already observe (`core/actions.py`: explicit human action
only, one in-flight action per repo, an audit line for every attempt) — extended, not
loosened.

### D1a-3. SSOT stays in the target repository

The target repo remains the single source of truth for the task. Dispatcher stores no task
state of its own: it reads back what it wrote, the way the merge gate re-reads PR state
from `github-checker` rather than trusting a cached verdict. If dispatcher's view and the
target's `TODO.md` disagree, the target is right by construction.

### D1a-4. Audit and idempotency

Every attempt leaves an audit line — including rejected, refused and busy ones. Re-issuing
the same request must be idempotent or visibly deduplicated. ADR-ECO-006's `slug:` is the
natural join: a second request for an existing slug reports the existing issue rather than
opening a duplicate. Silent duplication would make the inbox unusable, which is the failure
mode ADR-ECO-006 exists to prevent.

### D1a-5. Non-execution

Dispatcher does not execute an authored task, in whole or in part. Running the work stays
with spec-runner / Maestro. This boundary is stated separately rather than folded into
D1a-1 deliberately: it is the one most likely to erode, because each individual step toward
it looks small, and a rule recorded only in the place it was decided is followed less
reliably than one repeated where it applies.

---

## Scope of S2, and what this amendment does not authorise

**Within S2:** a screen that turns a discussed idea into a routed request — `create-issue`
delegated to `github-checker` (the same shell-out boundary as every other mutation), or a
`TODO.md` item proposed as a PR; read-back of what was created; the audit and deduplication
of D1a-4.

**Explicitly excluded, and *not* authorised here:**

- executing an authored task, in whole or in part (S3 / spec-runner / Maestro);
- an agent that resolves review threads or writes code (S3);
- auto-merge in any form, including of dispatcher's own authoring PRs;
- any authoring not initiated by a human click;
- dispatcher holding task state the target repo does not hold.

A later slice wanting any of these needs its own amendment. That is the point of listing
them: the exclusions are load-bearing, not decorative.

---

## Consequences

**Upsides:** the seam between "we discussed an idea" and "it is a task in the right repo"
stops being crossed by hand; the request lands in the channel ADR-ECO-006 already defines,
so acceptance and its evidence stay where the ecosystem already looks for them; the limits
are written before the code, rather than inferred from it afterwards.

**Downsides / cost:** D1's read/control-plane row is no longer a single short phrase — the
clause now has five qualifiers, and every future reader must carry them. Justified: the
alternative is a boundary that exists only in the implementer's memory.

**Risks:** (1) *scope creep by adjacency* — authoring is one step from executing, and each
step looks small (mitigation: D1a-5 states non-execution separately, and the exclusion list
is explicit); (2) *the inbox fills with duplicates* if idempotency is implemented loosely
(mitigation: D1a-4 names `slug:` as the join, and ADR-ECO-006 already made it the identity);
(3) *dispatcher accretes task state* to make the UI smoother — a cache that becomes a second
SSOT by accident (mitigation: D1a-3 requires read-back, not caching).

---

## Recommended actions

**prograph-vault**
- Ratify this amendment; on acceptance — add
  `**Amended by:** ADR-ECO-004a (dispatcher task authoring)`
  to ADR-ECO-004's header, matching the pattern ADR-ECO-003 already carries.
- Close `prograph-vault#54` (the request) with a reference to the merged ADR.

**dispatcher**
- Do not begin S2 implementation until this amendment is accepted. If it is rejected, S2 as
  designed does not proceed and the console stays at S1 — a complete, shipped slice, not a
  stub.
- On acceptance: the S2 design doc links the **merged** ADR, not the request issue.
- Keep `@id:merge-gate-pr-listing` in scope for S2 rather than S1 — the design's own flow
  ("operator opens dispatcher → list of open PRs across all repos") begins there, and S1
  ships a manual PR-number entry point instead.
