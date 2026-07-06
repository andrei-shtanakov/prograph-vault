---
title: R-07 — resolution: benchmark re-rank is a tiebreaker (decision C)
type: note
status: archived
owner: Andrei
updated: 2026-07-02
archived: 2026-07-06
reason: historical status snapshot (bulk-archived on graduation from _cowork_output)
---

# R-07 — resolution: benchmark re-rank is a tiebreaker (decision C)

> Date: 2026-07-02 · From: arbiter (owner decision: Andrei)
> Continues: `2026-07-02-r07-benchmark1-ab-executed.md`,
> `2026-06-21-r07-benchmark2-request-to-atp.md`.
> Context: after the re-sweep (ATP #213 token-fix + #215 golden-suite lock) and
> arbiter PR #33, we have real `rank_score` for the first time. But the live A/B showed that
> routing does not move — and the cause turned out to be arbiter-side, not in the data.

## Finding

- Real but **narrow** data: `claude_code@claude-sonnet-4-6` rank_score
  0.705 vs `codex_cli@gpt-5.5` 0.781 (n=3). Gap **0.076** < the acceptance threshold of
  benchmark #2 (|Δ| ≥ 0.15). No crossover/task-dependence.
- **Architectural blocker:** `apply_benchmark_rerank` adds
  `delta=(score-0.5)*weight` to confidence and re-sorts. But the bootstrap-DT
  outputs a **dominant leaf 1.0** (on python/moderate review → claude 1.0;
  codex is a real candidate, but lower). `+0.03..0.04` does not override a leaf-1.0 at
  any sane weight. The "flip at w≳0.4" from PR #33 was computed on a synthetic
  base with a DT gap of 0.03, not on the tree's real output.

## Owner decision — path C

Re-rank stays a **tiebreaker by design**, not a DT override:

- It changes the outcome only when the DT leaves ≥2 routable candidates near-tie.
- A confident leaf (1.0) is deliberately NOT touched. Giving the benchmark the right to override
  the expert DT is a different mechanism (a weighted blend `α·DT + β·rank_score`),
  **deliberately not chosen** now.
- R-07 closes honestly as "historical performance breaks ties on ambiguous
  tasks". Documented in the doc-comment of `apply_benchmark_rerank`
  (`arbiter-mcp/src/tools/route_task.rs`).

## What this means for atp / benchmark #2

- Benchmark #2 is **no longer the "enabling" gate** for re-rank (the mechanism is enabled and correct
  as a tiebreaker). It is now needed to **demonstrate value**: a crossover
  (A>B on one slice, B>A on another) is the only way to show that the
  tiebreaker actually improves routing vs "always-best" on DT-ambiguous tasks.
- The priority of the crossover request can be lowered from "blocker" to "desirable for the demo".

## Open lever (not now)

If we later decide the empirics should steer more strongly — path A (blend) remains
available as a local edit to `apply_benchmark_rerank`. Path B (soft DT leaves) is
deprioritized (fragile, touches training + all DT tests).
