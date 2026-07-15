---
title: "ADR-ECO-003e: Runtime cost control — usage capture, price snapshots & budget enforcement"
type: adr
status: proposed
owner: Andrei
updated: 2026-07-15
---

# ADR-ECO-003e: Runtime cost control — usage capture, price snapshots & budget enforcement

**Status:** Proposed (2026-07-15, Andrei) · **Date:** 2026-07-15
**Deciders:** Andrei (owner Maestro / arbiter / ATP)
**Scope:** ecosystem-wide runtime — the orchestrators that *run* agents (atp-platform
runtime, Maestro, spec-runner, robin-runtime) and their delegated harnesses. **Not** the
benchmark/leaderboard reporting layer (that stays 003d), **not** the LiteLLM Proxy.
**Type:** Sibling to `decisions/2026-07-02-adr-eco-003d-cost-pricing-mechanics.md` — picks up
the runtime track that 003d **D6 explicitly deferred** ("pre-flight counting / budget gates →
Maestro-runtime, a separate track, a separate owner"; "org-FinOps → revisit separately if
governance of live traffic arises"). Does **not** supersede 003d.
**Related:** ADR-ECO-003d (reporting-layer pricing, derive-at-report), ADR-ECO-003c
(local⟂cloud classes), ADR-ECO-003a/003b (discovery→adoption, the catalog contour).

> 003d fixed how the leaderboard *reports* cost after the fact (derived-not-stored, no abort —
> aborting a benchmark run corrupts the measurement). This ADR fixes the opposite problem: how a
> runtime *controls* spend **while it happens** — capturing usage at a single mandatory seam,
> pricing it synchronously, and enforcing budgets with a real hard cap. The two share the
> `TokenUsage` classes of 003d but have different roles: **derive-at-report** (003d) vs
> **enforce-at-runtime** (this ADR).

---

## Root cause (thesis first)

The audit that motivated this ADR found "token accounting almost everywhere, control almost
nowhere," plus a set of concrete integration defects in atp-platform (a `track_response_cost`
hook defined but never called; adapters emitting `model="unknown"`; `cost_usd` never populated;
11 adapters not capturing tokens; two divergent price tables).

**These are not N independent bugs. They are one missing contract.** There is no single seam
every caller is *required* to pass usage through, and no *synchronous* pricer an enforcement
point can consult at decision time. "11 adapters don't capture tokens" is not 11 tasks — it is
one absent capture contract. "Two price tables drift" is not a reconciliation chore — it is one
absent single-source-with-snapshot. This ADR defines that contract; the individual defects
become adoption items under it.

> **Confidence of the motivating findings:** the "missing explicit wiring" claims above are
> **static-analysis-grade** (grep + read), not runtime-proven. In Python a call can route through
> a registry, string dispatch, reflection, or plugin registration. This ADR treats runtime
> confirmation as the **acceptance gate of the first implementation** (Action №0), not as a
> precondition for the architectural rationale — the rationale (no single seam, no synchronous
> pricer) holds regardless of whether one specific hook is reached.

---

## TL;DR

1. **The subject is a protocol, not a gate.** A single `check_budget()` cannot guarantee a hard
   cap: under parallel callers several read the same remaining budget and collectively overspend
   (TOCTOU). The unit of decision is a lifecycle: **estimate → reserve → execute → record → settle**,
   with an **atomic reservation** keyed by `call_id`.
2. **Two contracts, one data model.** `UsageCapture` (measured/estimated usage *after* a call)
   and `BudgetControl` (estimate/reserve/settle *around* a call) are separate interfaces that
   share the 003d `TokenUsage` classes. Both are **vendored** into each repo (the `obs.py` /
   catalog pattern), canon in one owner, pinned copies downstream.
3. **Enforcement is two-tier by capability, and honest about it.** Direct callers get a per-call
   hard cap; delegating callers (spawning `claude -p`/codex/harness) get a hard *stop between
   attempts/tasks*; the native `--max-budget-usd` flag is **defense-in-depth, not trusted**. The
   guarantee ladder is stated explicitly (D4).
4. **Budget is multi-dimensional and nested.** `scope` is a first-class taxonomy
   (attempt ⊂ task ⊂ run ⊂ day/org), money cascades across it, the tightest dimension trips
   first, and a `deny` has a named outcome (terminal fail / pause / degrade) (D5).
5. **Fail-safe invariant: `unknown ≠ free`, not `unknown → deny`.** An unknown price defaults to a
   **conservative ceiling rate** (not zero, not refusal), keeping the open tail *usable* while
   still charging against budget. A per-scope policy can escalate to `deny` only where the risk is
   owned (locked prod). A silent zero from an unrecognized model is treated as `unknown`, never as
   free (D6).
6. **One price source, one pinned snapshot.** Ownership chain:
   *provider/LiteLLM data → discovery/import → canonical catalog
   (`atp-platform/method/agents-catalog.toml`, the named SSOT) → versioned snapshot*. Runtime
   reads **only the pinned snapshot** (fast, deterministic, no LiteLLM in the hot path). The
   hardcoded System-A table (`atp/cost/models.py`) is **deprecated** (D7).
7. **Runtime CostView ≠ reporting CostView.** Runtime adds `estimated_cost_usd`,
   `reserved_cost_usd`, `actual_cost_usd`, and a tri-state `pricing_status ∈ {known, ceiling,
   unknown}` (so a real price is distinguishable from a conservative estimate). Reporting keeps
   003d's view (D8).
8. **Out of scope:** the leaderboard cost axis (003d, post-hoc, no abort), the LiteLLM Proxy as a
   gateway, and local-`$` (003c D4).

---

## Context

### What is already true

| Fact | Consequence |
|---|---|
| 003d owns the reporting layer: derive-at-report, no runtime abort, LiteLLM as a library | This ADR must not touch the leaderboard's post-hoc semantics — enforcement is a different seam |
| 003d D6 explicitly deferred pre-flight counting / budget gates as "a separate track, a separate owner" | This ADR *is* that track; the seam is legitimate, not a re-litigation of 003d |
| Reference enforcers already exist: spec-runner (per-attempt/per-task hard caps → `BUDGET_EXCEEDED`), robin-runtime (`guard.check()` pre-call, daily-$ + msg-quota) | The contract must generalize *both* granularities, not pick one — hence the two-tier model |
| atp-platform delegates to CLI agents that self-manage `max_tokens`; individual calls are not interceptable | A delegating caller cannot hard-cap mid-call; the honest guarantee is containment at the unit boundary + an untrusted native flag |
| Callers run concurrently (sweeps, fan-out) | A read-only `check` races; a hard cap requires an atomic reserve against shared state |
| The open tail (new / self-hosted / fine-tuned / local) is frequently absent from any price map | A hard `deny` on "not in the map" couples *usability* to *price coverage* — the pressure that makes people disable the gate entirely |

### The transferability caveat (why "just do it like spec-runner" is incomplete)

spec-runner and robin own a per-attempt / per-call loop and make the LLM call themselves. The
atp-platform adapter model *delegates* to an agent that decides its own `max_tokens`. The
contract therefore cannot assume the enforcer sees each call — it defines the seam at whatever
boundary each caller *does* control, and names the resulting guarantee precisely (D4). Where a
caller has no interceptable boundary finer than the task, the promise is a hard *stop between
tasks*, not a hard cap *inside* a task. Saying otherwise would be a guarantee the transport
cannot keep.

---

## Decision

### D1. The unit is a cost-control **protocol** (lifecycle), not a single gate

```
estimate ─► reserve(scope, call_id, projected) ─► execute ─► record_usage(call_id, measured) ─► settle(reservation_id, actual)
                    │ atomic against shared budget state                                                │ release the hold, reconcile projected↔actual
                    └─ returns Decision{allow|deny, reason} + reservation_id                            └─ idempotent on call_id / reservation_id
```

A hold is placed **before** the spend and reconciled **after**. `estimate` is advisory;
`reserve` is the authoritative, atomic decision; `settle` closes the loop with the measured (or,
for delegated units, best-known) cost and releases the difference.

### D2. Two contracts, one shared data model — vendored

- **`UsageCapture`** — `record_usage(call_id, provider, model, usage: TokenUsage)`. The single
  **mandatory** seam every caller passes usage through. This is the ecosystem-wide replacement
  for atp's unreached `track_response_cost` and for per-adapter ad-hoc capture.
- **`BudgetControl`** — `estimate` / `reserve` / `settle` from D1.
- Both reuse the 003d `TokenUsage` classes (input / output / cache_creation / cache_read +
  `usage_source ∈ {measured, estimated}`). Distribution follows the `obs.py` / catalog rule:
  **canon in one owner repo, a pinned vendored copy inside each consumer** (CLAUDE.md polyrepo
  vendoring). No repo references another repo's path.

`record_usage` carries `call_id` (not just `provider/model`): without it, usage cannot be
reliably tied to a reservation, a retry, or a concurrent run — capture would serve observability
but not enforcement.

### D3. Atomic `reserve → settle` is what makes the hard cap real

`reserve` performs a **compare-and-commit** against the scope's remaining budget in one atomic
step (single-writer DB transaction / row lock / equivalent), returns a `reservation_id`, and is
**idempotent** on `call_id` (a retried reserve with the same `call_id` returns the same
reservation, never double-holds). `settle` is idempotent on `reservation_id`. This is the
concurrency guarantee a bare `check` cannot provide.

### D4. Two-tier enforcement — the guarantee ladder, stated explicitly

| Caller class | Reserve/settle boundary | Guarantee |
|---|---|---|
| **Direct** (robin, atp LLM-judge, any caller that issues the LLM call) | per-call | **Hard cap per call** — reserve before the call, deny if the reservation would breach |
| **Delegated** (atp adapter → `claude -p`/codex; Maestro → harness) | per-attempt / per-task | **Hard stop between units** — reserve the *unit's* projected cost; refuse to start the next unit on breach |
| **Native budget flag** (`claude --max-budget-usd`, harness caps) | passed through | **Defense-in-depth only — not part of trusted enforcement.** Reduces overshoot; its value is never assumed correct |

Explicit promise for delegated callers: **the current unit may overshoot its scope's remaining
budget by at most the reservation ceiling** established at `reserve` time; enforcement is
guaranteed at the *unit boundary*, not inside the unit. This is containment, and the ADR names it
as such rather than calling it a mid-task hard cap.

### D5. Scope taxonomy — dimensions, nesting, cascade, deny-outcome

- **Dimensions** (nesting): `attempt ⊂ task ⊂ run ⊂ day/org`. A caller may implement a subset,
  but the ordering and containment are fixed by the contract so that limits compose predictably.
- **Cascade:** a reservation is checked against **every** enclosing scope; the **tightest binding
  scope trips first**, and its `reason` names which dimension bound.
- **Deny outcome-contract** (named per scope, not implicit): `terminal_fail` (record
  `BUDGET_EXCEEDED`, mark the unit failed/terminal — spec-runner's semantics), `pause` (halt,
  await operator resume), or `degrade` (fall back to a cheaper model/shorter budget). The default
  is `terminal_fail`; the outcome is a scope property so a delegated path is never left with an
  undefined "what happens on deny."

### D6. Fail-safe — `unknown ≠ free`, via a two-axis policy (not a global deny)

Two orthogonal policy axes, set **per scope**:

- `enforcement_mode ∈ {observe, soft, hard}` — how strict the scope is overall (observe = record
  only; soft = flag/alert on breach; hard = deny on breach).
- `unknown_price_policy ∈ {flag, conservative_ceiling, deny}` — how an unknown price is handled.

Rules:

1. **Default `unknown_price_policy = conservative_ceiling`.** An unknown model is priced at a
   configured `unknown_model_rate` (or the map's max rate) × known tokens — computable because
   for the open tail the *price* is unknown, not the *tokens* (usage is measured, or locally
   counted). The gate keeps working: the model runs and is charged expensively until budget
   runs out. Availability preserved, `no-silent-zero` invariant held.
2. **`deny` only for `hard` scopes when no conservative upper bound can be computed** (neither a
   ceiling rate nor measurable/countable tokens). If you cannot bound the cost from above, you
   cannot promise a hard cap — so a hard scope refuses. Locked prod scopes may set `deny`
   outright; experimental dev scopes use `flag` (runs, warns, no charge).
3. **Silent zero is an `unknown`, not free.** A `0` returned by the pricer for an *unrecognized*
   model is the most dangerous case — it looks like a valid answer and silently opens the cap.
   The snapshot lookup distinguishes "priced at 0" (a real free tier, `pricing_status = known`)
   from "unrecognized → 0" (`pricing_status = unknown`); the latter is routed through
   `unknown_price_policy`.
4. **Close the loop.** `pricing_status ∈ {ceiling, unknown}` is a first-class signal: it
   surfaces in reports so the open-tail model is visible and the canonical catalog gets updated.
   A price gap becomes a feedback loop, not a wall.

### D7. Price consolidation — one source, one pinned snapshot

Ownership chain (single direction, one SSOT):

```
provider / LiteLLM data ─► discovery / import ─► canonical catalog ─► versioned snapshot
                                                 (atp-platform/method/                (pinned, read by
                                                  agents-catalog.toml — SSOT)          runtime gates)
```

- The **canonical catalog is the SSOT** (per ADR-ECO-003/003b). Discovery *proposes/refreshes*
  entries but is **not** a second SSOT.
- From the catalog, a **deterministic snapshot** is generated offline, stamped with
  `price_map_version` (the field 003d already mandates). Runtime `BudgetControl` reads **only the
  pinned snapshot** — no LiteLLM import in the enforcement hot path, reproducible pricing.
- The reporting layer (003d) continues to derive-at-report from the **same source**, so runtime
  and reporting cannot disagree on the price map for a given `price_map_version`.
- The System-A hardcoded table (`atp/cost/models.py`, "public pricing as of early 2026") is
  **deprecated** and removed once the snapshot is the runtime source.

### D8. Runtime CostView is distinct from the reporting CostView

Shared: `TokenUsage` (003d classes). Runtime `CostView` additionally carries
`estimated_cost_usd`, `reserved_cost_usd`, `actual_cost_usd`, `pricing_status ∈ {known, ceiling,
unknown}`, `price_map_version`. Rationale: enforcement needs to distinguish a real price from a
conservative ceiling (a boolean `price_unknown` cannot), and to reconcile projected↔reserved↔actual
across the reserve/settle lifecycle. (Exact field-level schema in the Appendix — kept out of the
Decision body so adding a field is a contract revision, not an ADR amendment.)

### D9. Explicitly out-of-scope

- **Leaderboard / benchmark cost axis** — 003d, post-hoc, derive-at-report, **no abort**.
- **LiteLLM Proxy as a gateway** — org-FinOps infra (live-traffic budgets, team attribution,
  spend DB). Revisit separately if live-traffic governance arises (003d D6).
- **Local-`$`** — not computed (003c D4); for local models: throughput / VRAM / hardware.

---

## Consequences

**Upsides:** one mandatory capture seam collapses "N adapters don't capture" into one adoption
checklist; an atomic reserve/settle makes the hard cap real under concurrency (the property a
bare check silently lacked); the open tail stays usable under a hard cap (`conservative_ceiling`
default) instead of being blocked; one price source with a pinned snapshot ends the System-A/B
drift; runtime and reporting share `TokenUsage` and a `price_map_version`, so they reconcile.

**Downsides / cost:** a reserve/settle store is new stateful machinery (holds, idempotency keys,
release-on-crash reconciliation) — heavier than a stateless check; the two-axis policy
(`enforcement_mode` × `unknown_price_policy`) is more configuration surface; a snapshot-generation
step is added to the release/refresh workflow; runtime and reporting keep *distinct* CostViews
(shared `TokenUsage`, divergent cost fields) — a deliberate split to maintain.

**Deprecations:** **System-A hardcoded price table (`atp/cost/models.py`) is deprecated** and
removed once the snapshot pricer lands (traceability for the "two price systems" consolidation).

**Operational (not decisions):** discovery regenerates/refreshes the snapshot from the catalog
on a cadence; a stale snapshot is bounded by `price_map_version` visibility; a crashed caller's
dangling reservation is reclaimed by a settle-timeout/reaper.

**Risks:** (1) reserve/settle bugs (leaked holds, double-charge) → mitigation: idempotency on
`call_id`/`reservation_id` + a reconciliation reaper; (2) `conservative_ceiling` mis-tuned →
either over-blocks (rate too high) or under-charges (too low) → mitigation: ceiling is
configurable per scope and the `pricing_status=ceiling` signal makes it visible; (3) snapshot
staleness diverges from real provider prices → mitigation: `price_map_version` stamp + discovery
refresh; (4) delegated-path overshoot larger than expected → mitigation: the reservation ceiling
bounds it and is stated as the explicit guarantee, not hidden.

---

## Recommended actions

**№0 — Bounded exposure probe + runtime acceptance gate (do first; prioritize by `$`, not by maturity).**
Run **1–2 pre-limited** runs (hard per-run cap, no claim of full statistics) to (a) confirm at
runtime that the capture wiring is actually absent on the paths the static audit flagged
(`track_response_cost` unreached, `cost_usd` unpopulated, `model="unknown"`) — this is the
acceptance gate, separating "statically no explicit wiring" from "runtime-proven"; and (b)
measure how much `$` actually flows through the *uncovered* paths (bedrock / http / cli) vs the
covered ones (azure / vertex). Fix by money, not by which gap looks scariest. Note the
chicken-and-egg: measuring uncovered spend needs a minimal slice of the capture contract — hence
*bounded* probe, not a full rollout.

**atp-platform (runtime)**
- Implement `UsageCapture.record_usage` at the **adapter boundary** as the single mandatory seam;
  retire the unreached `track_response_cost`; fix `model="unknown"` (pass the real model id).
- Add token capture to the adapters that lack it (bedrock, http, cli, container, autogen, crewai,
  langgraph, mcp, sdk) — ordered by the Action-№0 `$`-exposure result.
- Implement `BudgetControl` (estimate/reserve/settle) over the pinned snapshot; wire the
  per-scope deny outcome into the orchestrator.
- Deprecate & remove `atp/cost/models.py` once the snapshot pricer is the source (D7).

**Maestro / spec-runner / robin-runtime**
- Vendor the contract; map existing enforcers onto it: spec-runner's `task_budget_usd` /
  `max_retry_cost_usd` → `task`/`attempt` scopes with `terminal_fail`; robin's daily-$ / msg-quota
  → `day`/`org` scopes; Maestro's spec-gen `--budget` → a `run` scope on the delegated path.

**devtools / discovery**
- Generate the versioned snapshot from the canonical catalog; on a price-map gap, prepare a
  `register_model`-style entry from the catalog contour (003a/003b) — not a second SSOT.

**arbiter**
- Consume the derived cost signal as today (`over_budget`, `get_budget_status`); align its
  advisory budget invariant with the runtime scopes so its signal and the runtime gate agree.

**General**
- Ratify 003e **as a design** now; approve each repo's implementation behind its own Action-№0
  runtime confirmation. On acceptance, add a back-reference from 003d ("runtime enforcement: see
  003e") and from ADR-ECO-003.

---

## Appendix — contract surface (indicative, not ADR-frozen)

> Field-level shape lives with the vendored contract module, versioned independently of this ADR.

```
# shared data model (003d classes)
TokenUsage      = { input, output, cache_creation, cache_read, usage_source ∈ {measured, estimated} }

# runtime cost view (this ADR)
CostView(runtime) = { estimated_cost_usd, reserved_cost_usd, actual_cost_usd,
                      pricing_status ∈ {known, ceiling, unknown}, price_map_version }

# UsageCapture
record_usage(call_id, provider, model, usage: TokenUsage) -> None      # mandatory seam; idempotent on call_id

# BudgetControl
estimate(scope, projected_usage) -> CostView                            # advisory
reserve(scope, call_id, projected_cost) -> Decision + reservation_id    # atomic; idempotent on call_id
settle(reservation_id, actual_or_estimated_cost) -> None                # idempotent; releases the hold

Decision        = { verdict ∈ {allow, deny}, reason, bound_scope? }
scope           = one of { attempt, task, run, day, org } (nested; tightest binds first)
policy(scope)   = { enforcement_mode ∈ {observe, soft, hard},
                    unknown_price_policy ∈ {flag, conservative_ceiling, deny},
                    deny_outcome ∈ {terminal_fail, pause, degrade},
                    unknown_model_rate }
```
