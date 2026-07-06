---
title: "ADR-ECO-003c: Broad benchmark matrix — breadth owner + cost axes"
type: adr
status: proposed
owner: Andrei
updated: 2026-07-02
---

# ADR-ECO-003c: Broad benchmark matrix — breadth owner + cost axes by model class

**Status:** Proposed (2026-07-02, Andrei) · **Date:** 2026-07-02
**Deciders:** Andrei (owner Maestro / arbiter / ATP)
**Scope:** ecosystem-wide (ATP-benchmark + arbiter + devtools)
**Type:** Amendment to `decisions/2026-07-02-adr-eco-003a-model-discovery-adoption.md`
and ADR-ECO-003 (`2026-07-01-adr-eco-003-agent-catalog.md`)
**Related:** ADR-ECO-003a (discovery→adoption, `tested`/`routable` planes),
ADR-ECO-003b (catalog distribution), R-07 (benchmark re-rank as tie-breaker)
**Amended by:** **ADR-ECO-003d** (cloud-`$` pricing mechanics — concretizes D5)

> ADR-003a decoupled `discovery` (automatic) from `adoption` (gated) and introduced the
> split "model in `tested`" vs "model `routable`". The first broad slice (11 models on
> two verticals, 2026-07-02) confirmed it empirically: open/local models are competitive,
> and in places they beat the frontier. This amendment fixes **who owns breadth**
> (so the slice stops being a heroic one-off) and **in what currency cost is measured** —
> with the key decision that `$` is computed only for the cloud class, while the
> local class is ranked on a different axis. The full pricing mechanics (LiteLLM,
> provenance) are moved to a future 003d, so that cost **does not gate** breadth.

---

## TL;DR

1. **Breadth is the `tested` plane, not routing.** The mechanism is already in the catalog (ADR-003a):
   the `tested` set is broad and auto-enrolled via discovery, the `routable` set is narrow and
   benchmark-gated. The "pair" is `routable`. The "eleven" is `tested`. The design is
   in place; it just was not run regularly.
2. **Diffusion of responsibility existed because breadth belonged to no one.** Each
   owned their own layer (catalog / shim / sweep / ingest / policy). Breadth is a
   cross-cutting concern, like discovery. **We assign an explicit owner: ATP-benchmark**, separate
   from routing decisions (arbiter/PM).
3. **Breadth is a scheduled job, not heroism.** A regular run of the `tested` matrix, fed by
   discovery (003a auto-enrolls new models into `tested`). There must be no one-off re-run.
4. **Validity is first-order, cost is second.** Publishing the leaderboard and expanding the
   matrix **must not be gated** on a cost model. Validity guardrails (runs≥3 for the top tier,
   corpus-fix, raw tokens = a per-model diagnostic) go ahead of `$`.
5. **Local ⟂ cloud — these are two classes with different axes, not two currencies of one axis.**
   Cloud: the `$`/task axis (market price, measurable). Local: the axis of **admissibility and
   throughput** (tok/s, peak VRAM, hardware class). **We do not compute `$` for local in the
   leaderboard** — the marginal cost of inference ≈ energy, and the decision is made on
   "fits / does not lag", not on "$ per run".
6. **Cloud-`$` = LiteLLM as a library-pricer over stored usage**, not a proxy, not a
   context-counter. Derived-not-stored. The mechanics (measured-first/estimated-fallback,
   provenance, `register_model`) are the subject of **003d**; here we fix only the boundary and the class.
7. **arbiter consumes a ready number.** Rust does not run LiteLLM; the routing cost signal is the
   cloud class, arriving as a policy field (like `cost_per_hour` already does).

---

## Context

### Trigger (2026-07-02)

Owner: "the assumption is that the most varied models are used, including open ones
(DeepSeek) and local ones; comparing only two models does not satisfy me in principle".
Expanding the matrix kept stalling — not from a lack of tools (the harnesses
`mimo/qwen/deepseek/opencode/pi/ollama` are already in the catalog, the shims are written),
but from **diffusion of responsibility**: "add a model" was perceived as one indivisible
cross-team change, where each step is "someone else's".

### What the first broad slice showed (11 models, runs=1)

- **Open models are competitive and in places lead.** On `code-review`, mimo-v2.5-pro
  (14/15), glm-5.1 (13/15), qwen3.6-plus tied with claude/codex. Several open models in the
  top band are harder to explain away as noise than a single outlier.
- **The suite genuinely discriminates.** A floor gradient `qwen2.5:3b > llama3.2:3b > llama3.2:1b`,
  a spread of rank 0.93→0.00. The frontier ceiling is saturation, not a loose grader.
- **The token comparison is currently unfair.** `claude_code=579k` vs `anthropic_api=9k` on the
  **same** sonnet-4-6 — that is ×64 due to agentic prompt-caching, not the model. Raw tokens are
  not a single currency (different tokenizers per model).
- **corpus-clean is a wiring artifact**, not capability: all 11 models fail on it
  identically (`run_pipe_check` does not mount `assets/`).

### What is already true in the catalog (ADR-003a)

`tested` (broad, all `active`) vs `routable` (narrow, benchmark-gated) — the fields already exist.
Discovery (003a D5, `devtools/discover_models.py`) auto-enrolls new models into `tested`.
What is missing is the **breadth owner** and the **regular run**, not the mechanics.

---

## Decision

### D1. Breadth owner is ATP-benchmark, separate from routing

| Responsibility | Owner | Rationale |
|---|---|---|
| **Breadth of the `tested` matrix** (which models run in the slice, completeness, regularity) | **ATP-benchmark** | Breadth is a cross-cutting measurement concern; ATP is already the authority on `rank_score` and holds `run_pipe_check`. Previously it belonged to no one → diffusion. |
| **Routing decision** (flip to `routable`, re-rank weight) | **arbiter / PM** | A deliberate gate (ADR-003a D5), not an automatism. |
| **Discovery** (auto-enrollment into `tested`) | **devtools** | Already fixed in 003a D5. |

The 003a decoupling ("enrollment into `tested` is automatic, promotion into `routable` is
gated") means: **you can test 11, promising to route nothing.** The broad slice is the payout
on that decoupling. The breadth owner is responsible for the completeness of `tested`, not for
routing.

### D2. Breadth is a scheduled job, fed by discovery

A regular run of the `tested` matrix on the pinned golden `suite_id` (the same as for the A/B in
003a D3). Discovery adds a new model to `tested` → the next scheduled run includes it
automatically. A heroic one-off re-run is an anti-pattern: breadth must not depend on someone
manually remembering to run 11 models.

### D3. Validity first-order; cost second. Do not gate breadth on cost

The leaderboard's authority rests on validity **before** the presence of a `$` axis. Order:

1. **Corpus-fix first.** `corpus-clean` is a wiring artifact (`run_pipe_check` does not mount
   `assets/`). Exclude the corpus cases from req-extraction **before** any ranking, or fix the
   wiring. Otherwise `bp→0` for everyone is meaningless.
2. **runs≥3 for the top tier** before asserting concrete ranks. n=1 across all models →
   single-case noise applies to all; large effects (open models are competitive) are robust,
   but the exact rank "mimo #1" is suggestive, not assertable.
3. **Raw tokens are a per-model diagnostic, not a comparable column.** The broad slice can be
   published **now** with this caveat; a `$` axis is not a precondition for the thesis "open
   models are competitive".

**Explicitly:** expanding the matrix and publishing are NOT blocked on the cost model. Cost is a
refinement on top of a valid board, not a gate (otherwise we reproduce the very stopper "not
ready yet").

### D4. Two model classes — two axes, not two currencies of one axis

Local and cloud answer **different questions**; gluing them into one cost column is a
categorical error.

| | Cloud class | Local class |
|---|---|---|
| Question | "how much will I pay" | "will it fit my hardware and at what speed" |
| Axis | `$`/task (market, measurable) | tok/s, peak VRAM, required GPU class |
| Nature | billing (opex, per-token) | capacity planning (capex already spent) |
| Tool | LiteLLM pricer (D5) | measuring throughput/footprint |
| `$` in the leaderboard | yes | **no** |

**We do not compute `$` for local.** The marginal cost of local inference ≈ energy
(pennies); in a corporate-local scenario the hardware is capex, and the decision is made on
"fits / does not lag". A single `$` axis would make local models "free" (a worst-case
distortion for the thesis) or would require a modeled compute price — **false precision**
(dependent on utilization/batch/hardware, which are absent). We rank **within the class**.

Compute-`$` (GPU amortization $/1M tok.) is admissible **only** as a separate scenario
calculator for the FinOps conversation "buy hardware or pay for the API", with explicit
assumptions — **not a number in the leaderboard**.

### D5. Cloud-`$` — a library-pricer over stored usage; proxy out-of-scope

For the cloud class:
- **LiteLLM as a library** (`cost_per_token`/`completion_cost`), not the Proxy. Rationale:
  the routable harnesses are CLI agents (`claude_code` invokes `claude -p`, codex similarly),
  the LiteLLM Proxy sits in front of `/chat/completions` and **will not stand in front of a
  CLI agent** → it would not uniformly capture exactly the routable set. The Proxy is
  org-FinOps infra, a separate conversation.
- **Derived-not-stored.** The shim writes raw `usage` by class (input/output/cache_*, after the
  003a P2 fix) into `benchmark_runs`; `$` is computed **at report time**, re-derived on a price
  change without a re-sweep.
- **The mechanics are concretized in ADR-ECO-003d** (Proposed, implementation-contingent on
  003a P2): measured-first → estimated-fallback via `token_counter` with the provenance flag
  `usage_source`; `register_model` for price-map gaps in the open tail; prices from the same
  contour as discovery. Here we fix only the boundary and the class, so that 003c remains
  shippable without a pricing implementation.

### D6. Consumption: arbiter receives a ready number

The cost-normalized routing signal (cloud class: on a quality tie, but ×N cheaper →
prefer the cheaper) is computed on the ATP side and arrives in arbiter as a policy field, a
number (as `cost_per_hour`/`avg_duration` already do). Rust does not run LiteLLM. For the local
class the routing signal is not `$` but admissibility/throughput (D4).

---

## Consequences

**Upsides:** breadth stops being heroism (an owner + scheduled); the "multi-model landscape"
thesis is published immediately with honest caveats, without waiting for a cost model; local
models do not collapse into a fake `$` and do not get false precision; cloud-`$` is honest
(cache classes) and derived. The organizational root ("no one owns breadth") is closed by an
explicit assignment.

**Downsides / cost:** ATP-benchmark gets a new permanent zone (a scheduled job, maintaining the
golden-suite); two cost classes complicate the leaderboard presentation (there cannot be one
"cost" column); corpus-fix and runs≥3 are work before "assertable" ranks.

**Risks:** (1) the scheduled matrix grows and becomes expensive → mitigation: a broad `tested`
at runs=1 as a screen, a narrow top tier at runs≥3; (2) the temptation to drag compute-`$`
into the leaderboard "for symmetry" → D4 forbids it explicitly; (3) the cost model (003d) drags
on and starts being perceived as a gate → D3 fixes it: breadth does not depend on it.

---

## Recommended actions

**ATP-benchmark (the new explicit breadth owner)**
- Take ownership of the completeness of the `tested` matrix; a scheduled job running on the
  pinned golden `suite_id`.
- Corpus-fix: fix/exclude `corpus-clean` in req-extraction (`run_pipe_check` does not mount
  `assets/`) **before** ranking.
- runs≥3 for the top tier before asserting concrete ranks; the broad `tested` — a runs=1 screen.
- Publish the first slice **now** with the caveat "raw tokens are a per-model diagnostic".
- Local class: measure and report tok/s + peak VRAM + hardware class (not `$`).

**devtools**
- Discovery (003a D5) auto-enrolls new models into `tested` → the scheduled run picks them up.

**arbiter**
- The routing cost signal (cloud class) — consume as a ready number, a policy field; local —
  admissibility/throughput, not `$`.

**General**
- Ratify 003c; on acceptance — update the status of ADR-003/003a with a reference.
- **Cost fork:** move the cloud-`$` pricing mechanics (LiteLLM library, provenance,
  `register_model`) into a separate **ADR-ECO-003d**, to be written **after** the 003a P2
  token-fix settles (so the design is exercised on real measured usage, rather than fixed blind).
