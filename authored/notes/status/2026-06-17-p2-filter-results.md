---
title: 'R-07 P2 — Filter results: harder code-review cases (for arbiter team)'
type: note
status: archived
owner: Andrei
updated: 2026-06-17
archived: 2026-07-06
reason: historical status snapshot (bulk-archived on graduation from _cowork_output)
---

# R-07 P2 — Filter results: harder code-review cases (for arbiter team)

**Date:** 2026-06-17
**Outcome: A — separation confirmed.** The `code-review` benchmark now contains ≥2 cases where the routable agents diverge, reproduced on held-out. Direction: **claude_code > codex_cli** on review.
**Data:** `atp-platform/_cowork_output/r07-pipecheck/p2-filter.db` (n=3, 15 cases × 3 agents) + `p2-heldout.db` (n=8, 3 candidates × routable). Cases: `method/cases/code-review/case-code-review-correctness-*` (10 new) + 5 SQLi.

## Kept cases (reproduced, ≥0.34 absolute floor, not malformed-explained)

| case | capability | claude (n=8) | codex (n=8) | gap | note |
|---|---|---|---|---|---|
| `fp-deser-trusted-001` (F2) | **fp-discipline** | 1.00±0.00 | 0.50±**0.00** | **+0.50** | codex **deterministically over-flags** `pickle.loads` on a provably in-process source (16/16 runs). Bulletproof (sd=0). |
| `distractor-singlefile-001` (D3) | **distractor-recall** | 0.97±0.08 | 0.38±0.48 | **+0.59** | claude reliably finds an off-by-one buried in a 30-line refactor; codex wildly inconsistent (sd 0.48, ≈3.4σ). |

## What did NOT separate (the honest part)

- **The cross-file hypothesis failed.** The triage had pointed at cross-file/multi-hop taint (claude appeared to miss the very-severe cross-file SQLi). On the proper n=3 + held-out runs: the cross-file distractors **D1 (+0.11) and D2 (tie)** did not separate, and the **seeded anchor (very-severe SQLi) reverted to a tie** (both 1.0). That lead was the **intermittent ~7% malform flak**, not a stable capability gap — we treated it as selection-side and did not build on it (vindicated by the held-out).
- **S2 (pagination) washed out:** first-pass +0.33 was codex variance; n=8 collapsed it to +0.12 (below floor). The held-out did its job filtering noise.
- All 5 SQLi, S1, L1, L2, F1, F3, D1, D2 are **ties** at the frontier (both ≈1.0) — they remain valid graded-difficulty content (they separate the *local* models per the 2026-06-17 matrix, and serve as saturation controls), but they do not separate this routable pair.

**The real separating axes are FP-discipline and needle-in-noise recall-consistency — not cross-file detection.** An empirical surprise; the point of the filter.

## Cost / latency (routable, n=3, 15 cases)

| agent | tokens/pass | cost/pass | latency/pass | quality (cpr) |
|---|---|---|---|---|
| claude_code | 262.6k | **$3.13** (measured) | 254s | 0.96 |
| codex_cli | 237.3k (now captured) | unmeasured ($; codex emits no $) | **142s** (faster) | 0.80 |
| deepseek | 5.1k (terse) | unmeasured | 31s | 0.67 |

codex token capture now works (Task 0, `codex exec --json`). codex is the **faster** routable agent at comparable tokens but lower review quality → a real **quality-vs-latency** tradeoff for budget-aware routing. ($ for codex still needs a token→price lookup.)

## Recommendation for arbiter (Task-4)

The benchmark now carries a reproduced routable signal: **claude_code beats codex_cli on review** (FP-discipline F2 + needle-in-noise D3). This is enough to run the **Task-4 A/B on `code-review`**: with `ARBITER_BENCH_WEIGHT` on, a review-task re-rank should prefer `claude_code` over `codex_cli`, and the audit line should fire. The mechanism (Tasks 1-3, green) finally has a real per-agent score to act on.

Caveats: (1) two cases is a narrow signal — widen by authoring more FP-discipline cases (codex over-flags deserialization; probe other safe-but-scary patterns) for ≥2-concordant-same-capability robustness. (2) Signal is version-specific (re-filter on codex/claude updates). (3) If latency/cost matters more than the modest quality gap, codex (faster) may still win under a budget-aware weight — capture codex $ to decide.

## Spend
Filter n=3 (15 cases × 3 agents): claude ~$9.4 measured + codex/deepseek (unmeasured $). Held-out n=8 (3 cases × 2 agents): ~$2-3. Plus Task-0 scout (~$2). Total order ~$13-15 measured + codex unmeasured.
