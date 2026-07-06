---
title: R-07 — benchmark #1 A/B executed (re-rank turned on)
type: note
status: archived
owner: Andrei
updated: 2026-07-02
archived: 2026-07-06
reason: historical status snapshot (bulk-archived on graduation from _cowork_output)
---

# R-07 — benchmark #1 A/B executed (re-rank turned on)

> Date: 2026-07-02 · From: arbiter
> Context: closes the last step of R-07 P0 — an actual A/B run with
> `ARBITER_BENCH_WEIGHT` > 0. The re-rank mechanism was coded earlier
> (PR #26 ingest, #27 determinism, #30 rank_score-tiebreaker), but until now
> it had never been run live with the weight enabled.
> Related: `2026-06-21-r07-benchmark2-request-to-atp.md` (request for separating data),
> `2026-06-13-r07-phase1-pipe-proof.md`.

## What was done

- Rebuilt `arbiter-mcp` (release).
- `scripts/ab_bench_rerank.py --db arbiter.db` — one `review` task twice:
  `ARBITER_BENCH_WEIGHT=0` (control) and `=0.15` (treatment).
- Data: 13 rows of `benchmark_runs` (benchmark_id=`code-review`), including both
  routable keys `claude_code@claude-sonnet-4-6` and `codex_cli@gpt-5.5`.

## Result

| | weight=0 | weight=0.15 |
|---|---|---|
| chosen_agent | `claude_code@claude-sonnet-4-6` | `claude_code@claude-sonnet-4-6` |
| confidence | 1.000 | 1.000 (delta clamped) |
| audit line in `decision_path` | none | `bench_adjust[claude_code@claude-sonnet-4-6]: code-review score=0.800 delta=+0.045` |

## Conclusion

- ✅ **Mechanism proven end-to-end.** `weight>0` → `apply_benchmark_rerank`
  reads `code-review` from `benchmark_runs`, applies `(score−0.5)·weight`,
  writes an auditable `bench_adjust[...]` into `pred.path`/`decision_path`.
- ✅ **No-op at weight=0** — byte-for-byte identical decision, no audit line.
- ✅ **Determinism** — the confidence tie is resolved by `agent_id` asc
  (`route_task.rs:85`), plus unit `rerank_orders_tied_scalar_agents_by_rank_score`.
- ⚠️ **Routing does not change** on the current data, for two independent reasons:
  (1) the winner's confidence is already 1.0 → the delta is clamped; (2) both routable agents
  are identical at 0.8 → equal delta, zero separation. This is the expected outcome
  of "one benchmark proves the mechanism" (CLAUDE.md). Validation of the *direction/value*
  of routing awaits benchmark #2 (separating data, the crossover/task-dependence gate) —
  the request to atp is already open (`2026-06-21-...`), acceptance criterion `|Δscore| ≥ 0.15`.

## Next

- R-07 P0 closed (the mechanism turns on and is auditable). Leave
  `ARBITER_BENCH_WEIGHT` as an opt-in env (default 0.0) until separating data arrives.
- Unblocked by benchmark #2 → then A/B will show a real flip and resolve the
  crossover/task-dependence gate.
