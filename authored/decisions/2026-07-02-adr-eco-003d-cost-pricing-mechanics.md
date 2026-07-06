---
title: "ADR-ECO-003d: Cloud cost — pricing mechanics (LiteLLM over stored usage)"
type: adr
status: proposed
owner: Andrei
updated: 2026-07-02
---

# ADR-ECO-003d: Cloud-`$` — pricing mechanics (LiteLLM library over stored usage)

**Status:** Proposed (2026-07-02, Andrei) — **implementation-contingent on 003a P2**
· **Date:** 2026-07-02
**Deciders:** Andrei (owner Maestro / arbiter / ATP)
**Scope:** ecosystem-wide — the ATP-benchmark reporting layer (not runtime, not proxy)
**Type:** Amendment to `decisions/2026-07-02-adr-eco-003c-broad-matrix-cost-axes.md` (D5)
**Related:** ADR-ECO-003c (local⟂cloud classes, `$` cloud only), ADR-ECO-003a
(P2 token-fix in `claude_code_shim.py`), ADR-ECO-003b (the catalog as the price contour)

> 003c fixed the **boundary**: the cloud class is measured in `$`, LiteLLM — as a library
> (not a proxy), cost is derived-not-stored. This amendment concretizes the **mechanics**:
> where the tokens come from (measured vs estimated), how they are priced, where the prices live,
> and how a comparable axis is computed. **Contingency:** the design relies on the `usage` from
> the shims carrying the cache classes after the 003a P2 fix. Until this is confirmed on real
> `benchmark_runs` rows the status is Proposed; ratification of the implementation — after P2
> settles (see the "Contingency" section).

---

## TL;DR

1. **Two LiteLLM functions answer two different questions.** `token_counter`/`encode`
   (how many tokens) ≠ `completion_cost`/`cost_per_token` (how much money). We use
   **both, but in different roles** — do not confuse them.
2. **The token source is measured-first.** The ground truth of "how much the run really cost" is
   the provider's `usage` (after 003a P2 — with the cache classes). LiteLLM here = a **pricer over
   the measured**, not a re-counter. Re-count with a tokenizer loses here: it approximates and
   loses the real `cache_read`/`cache_creation` split.
3. **Estimated-fallback — only where there is no usage.** Part of the open/local tail does not
   return `usage` → `token_counter` estimates prompt/completion. Estimated has **no
   cache-split** → systematically off for caching harnesses.
4. **Provenance is mandatory.** The flag `usage_source ∈ {measured, estimated}` in the row.
   Estimated and measured tokens **are not silently placed in one column** — that is a soft
   asymmetry, like runs=1.
5. **Pricing is on the reporting layer, derived-not-stored.** Raw usage is stored; `$`
   is computed at report time; a price change → re-derive without a re-sweep. The price is **not baked**
   into `benchmark_runs`.
6. **Prices — from one contour with discovery/catalog**, with a price-map version stamp in the
   row. `register_model()` closes map gaps for the open tail (mimo, glm-5.1,
   qwen3.6). We do not create a 4th source of truth for prices.
7. **The comparable axis is `$` or per-task, not raw tokens.** `token_counter` uses a
   **different tokenizer per model** → 1000 Claude tokens ≠ Qwen. Raw tokens remain a
   **per-model diagnostic**; cross-model we compare `$` (normalizes by price) or
   tokens/solved-case.
8. **Scope — cloud class.** We do not compute local `$` (003c D4). Proxy and pre-flight counting are
   out-of-scope (see D6).

---

## Context

### Where the task came from

The first broad slice (003c) showed: the token comparison is unfair. `claude_code=579k` vs
`anthropic_api=9k` on the **same** sonnet-4-6 — ×64 due to the prompt-caching of the agentic
harness, not due to the model. An honest cost axis requires (a) pricing the cache classes at
their reduced rate (`cache_read` ~10% of input at Anthropic), (b) not mixing the harness
architecture with the model's cost.

### What is already true (taken off the 2026-07-02 discussion)

| Fact | Consequence |
|---|---|
| `total_cost_usd` in the claude_code path is already correct (priced across all classes) | The bug was in `total_tokens`, not in `$`; P2 fixes the token accounting |
| the anthropic_api shim (raw API) gives a plausible ~9k — the cache classes are zero | measured usage is structurally different for caching vs non-caching harnesses |
| part of the open/local tail returns partial/empty usage | An estimated-fallback is needed, otherwise the cost axis is incomplete across the fleet |
| the LiteLLM price map is community-maintained, new/niche models may be absent | `completion_cost` returns 0 (a silent zero) or throws → `register_model` is needed |
| the routable harnesses are CLI agents (`claude -p`, codex) | The LiteLLM **Proxy** will not stand in front of them → a library, not a gateway (003c D5) |

---

## Decision

### D1. Two functions, two roles — do not mix

| LiteLLM function | Question | Role for us |
|---|---|---|
| `token_counter` / `encode` | how many tokens | **fallback source** of tokens when the shim did not return usage; separately — pre-flight (D6, out-of-scope here) |
| `cost_per_token` / `completion_cost` | how much money | **pricer** over any token source |

### D2. Token source precedence: measured → estimated

Per run:
1. There is `usage` from the shim → **measured** (with the cache classes after P2). We price it.
2. No `usage` → `token_counter` estimates (the provider count-API if available, otherwise
   tiktoken+safety-buffer) → **estimated**. Estimated has no cache-split.

Re-count when measured is present — forbidden (loses the real split, approximates blindly).

### D3. Provenance: `usage_source` in the row, separate columns

`benchmark_runs` carries `usage_source ∈ {measured, estimated}`. Leaderboard:
- measured and estimated **are not averaged in one column**;
- estimated is marked visually (no cache-split → for caching harnesses the estimate
  systematically underscores/distorts);
- when estimated dominates in a tier — the flag "cost unreliable", like the runs=1 variance flag.

### D4. Pricing — derived-not-stored, on the reporting layer

- The shim writes **raw usage by class** (`input`/`output`/`cache_creation`/`cache_read`) +
  `usage_source`. Nothing is priced at write time. *(Requires the `report_benchmark-v2`
  contract — v1 carries only `total_tokens`; see "Contingency".)*
- `$` is computed **at report time** via `cost_per_token(prompt_tokens=…,
  completion_tokens=…, cache_read_input_tokens=…, cache_creation_input_tokens=…)` —
  for measured we feed the cache-split, so that `cache_read` goes at the reduced rate.
- A price change → **re-derive the view without a re-sweep**. The price is not baked into
  `benchmark_runs`.

### D5. Prices — one contour with the catalog, `register_model` for the tail, version in the row

- Price-map gaps (the open tail: mimo, glm-5.1, qwen3.6) are closed by
  `litellm.register_model()` — the prices are taken **from the same discovery/catalog contour**
  (003a/003b), not from a 4th source of truth. Discovery, finding a model, refreshes the price too.
- The row gets a **price-map version stamp** (`price_map_version`), so the `$` view is
  reproducible and it is visible at what price it was computed.
- A silent zero (`completion_cost` returned 0 because the model is absent from the map) is
  **detected and flagged**, not averaged as "free".

### D6. Explicitly out-of-scope

- **LiteLLM Proxy** — the CLI harnesses will not stand behind it; this is org-FinOps infra
  (budgets, attribution by team, a spend DB). Revisit separately if governance of live traffic
  arises. Not a tool of the benchmark leaderboard.
- **Pre-flight counting** (budget gates, context-fit before a call) — this is **Maestro-runtime**,
  a different scenario (there counting is primary by definition). Orthogonal to the post-hoc cost
  axis; a separate track, a separate owner. Do not mix with the leaderboard.
- **Local `$`** — we do not compute it (003c D4). For local — throughput/VRAM/hardware.

### D7. arbiter consumption

The cost-normalized signal (cloud class) is computed on the ATP side, arrives in arbiter as a
number, a policy field (like `cost_per_hour`). Rust does not run LiteLLM; it receives the derived `$`.

---

## Data-flow

```
shim ─► raw usage by class (+ usage_source flag) ─► benchmark_runs
                                                        │  (report time — derived)
              LiteLLM cost_per_token  +  register_model(open-tail / catalog prices)
                        │ measured → with cache-split (cache_read at the reduced rate)
                        │ estimated → without split, marked
                        ▼
     cloud-$ view (+ price_map_version)  +  per-task norm. ─► leaderboard / arbiter cost signal
```

Principles: **store the raw — derive the cost**; **measured matters more than estimated** (a
fallback with provenance); **cost is not one currency** (cloud-`$` / per-task; local out of
scope); **a library, not a gateway**.

---

## Contingency (why Proposed, not ready for implementation)

> **Clarification 2026-07-03 (verified against the code and live data):** 003a P2 is **closed** —
> the shim returns all 4 classes in `ATPResponse.metrics` (atp-platform #213 + fields in the
> protocol model `Metrics`); the 2026-07-02 re-sweep confirmed it on a live run
> (`claude_code` total_tokens 1336 → ~575k). **But the class-split is lost at the
> shim→payload boundary:** the `report_benchmark-v1` contract carries only `total_tokens`
> (+ `tokens_used` per-task), and the arbiter `benchmark_runs` schema carries only
> `total_tokens`/`total_cost_usd`. The check "usage in `benchmark_runs` carries 4 classes"
> in its original formulation is **structurally infeasible under v1** — not because P2 did not
> work. The contingency moves from P2 to the **`report_benchmark-v2` contract** (action item
> №1 below).

The design relies on per-class usage reaching `benchmark_runs`. Until `report_benchmark-v2` exists:
- the cache-split is unavailable for measured pricing (D4) — it exists in the shim metrics,
  but not in the rows;
- it is impossible to calibrate how far estimated diverges from measured on caching harnesses (D3).

**Ratification order (corrected 2026-07-03):** ~~003a P2 fix → re-sweep 2 routable~~
(✅ done 2026-07-02) → **the `report_benchmark-v2` contract** (per-class usage +
`usage_source` + `price_map_version`) + migration of the `benchmark_runs` schema → a new
sweep/ingest under v2 → confirm the 4 classes in live rows → **then** implement the
pricing view per this ADR. Writing it now — so the design is fixed and not reinvented;
approving the implementation — on real usage.

---

## Consequences

**Upsides:** an honest cloud-`$` (cache classes at the reduced rate → "579k as ×14" collapses
into a real `$`); the cost axis is complete across the fleet (estimated-fallback) without lying
(provenance); re-derive on price changes without a re-sweep; prices do not spawn a source of truth.

**Downsides / cost:** two columns (measured/estimated) complicate the leaderboard;
`register_model` + a price refresh via discovery — new maintenance; `price_map_version` — an extra field.

**Risks:** (1) the price map goes stale → mitigation: a version stamp + a refresh from the
discovery contour; (2) estimated dominates in a tier and the cost rank misleads → mitigation: a
reliability flag; (3) a silent zero from an unregistered model → mitigation: detect+flag, do not
average; (4) P2 does not deliver the expected cache classes → the measured-pricing design is
revisited (that is what Contingency is for).

---

## Recommended actions

**atp-platform / ATP-benchmark**
- [x] ~~complete 003a P2, re-sweep~~ — ✅ 2026-07-02 (atp-platform #213; the re-sweep confirmed
  correct tokens in the shim metrics). The 4 classes did NOT appear in `benchmark_runs` as a
  result — the v1 contract does not carry them (see "Contingency").
- **№1 (a new pre-req, blocks D2–D5): the `report_benchmark-v2` contract** — the payload carries
  per-class usage (`input`/`output`/`cache_creation`/`cache_read`) + `usage_source` +
  `price_map_version`. Cross-repo work: the ATP reporter
  (`build_report_benchmark_payload`) + the arbiter `report_benchmark` tool/ingest +
  migration of the `benchmark_runs` schema. Version the contract explicitly (`payload_version`),
  v1 rows remain readable (fallback to `total_tokens`, without cache-split).
- Row schema: raw usage by class + `usage_source` + `price_map_version`.
- Reporting view: `cost_per_token` over stored usage (measured with split, estimated without),
  separate columns, a reliability flag.
- `token_counter`-fallback only for rows without usage.

**devtools**
- Discovery, finding a model, refreshes the price (the LiteLLM map as the source) and, on a gap,
  prepares a `register_model` record — from the same catalog contour (003a/003b), not a 4th source.

**arbiter**
- Accept `report_benchmark-v2` on its side: payload validation in the
  `report_benchmark` tool + migration of `benchmark_runs` (per-class columns /
  a usage json-field, `usage_source`, `price_map_version`).
- Consume the derived cloud-`$` as a number, a policy field; do not run LiteLLM.

**General**
- Ratify 003d **as a design** now; the implementation — after P2 settles (Contingency).
- On acceptance — update the status of 003c (D5 → "mechanics: see 003d") and ADR-003/003a with a reference.
- Pre-flight counting (Maestro-runtime) — run as a separate track, not in this ADR.
