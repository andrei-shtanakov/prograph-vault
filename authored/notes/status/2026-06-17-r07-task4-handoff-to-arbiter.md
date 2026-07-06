---
title: R-07 Task-4 handoff → arbiter team
type: note
status: archived
owner: Andrei
updated: 2026-06-17
archived: 2026-07-06
reason: historical status snapshot (bulk-archived on graduation from _cowork_output)
---

# R-07 Task-4 handoff → arbiter team

**Date:** 2026-06-17
**Status: UNBLOCKED.** The atp-platform side has produced a reproduced, routable signal on `code-review`. Your re-rank mechanism (Tasks 1-3, commit `dba212a`, green) finally has real per-agent data to act on. This is the Task-4 (real-data A/B) handoff.

## The signal (what to expect the re-rank to do)

On `code-review`, **claude_code > codex_cli**, stable across 3 filter passes + an n=8 held-out:

| agent | code-review score (critical_pass_rate, aggregate) | routable? |
|---|---|---|
| claude_code | **0.93–0.96** | yes |
| codex_cli | **0.80** | yes |
| deepseek | 0.67 | **no — labeled baseline, do not route** |

Evidence it's capability, not noise (per-case, held-out n=8): `fp-deser-trusted` (codex *deterministically* over-flags pickle-on-trusted, gap +0.50, sd=0, 16/16) + `distractor-singlefile` (claude reliable / codex flaky under noise, gap +0.59 ≈3.4σ). malformed_rate ≈0 for both → not a format artifact. Full analysis: `2026-06-17-p2-filter-results.md`.

→ With `ARBITER_BENCH_WEIGHT > 0`, a Review-task re-rank should prefer `claude_code` over `codex_cli` (delta = (score−0.5)·weight → +0.43·w vs +0.30·w).

## Data to ingest (ready, v1-valid)

`atp-platform/_cowork_output/r07-pipecheck/p2-run-{1,2,3}/report_benchmark_{claude_code,codex_cli,deepseek}.json`
- Full `report_benchmark-v1` (`payload_version: 1.0.0`, `run_id`, `benchmark_id: code-review`, `agent_id`, `ts`, `score`, `score_components`, `per_task`, `per_task_total_count`, `per_task_truncated`, `total_tokens`, `total_cost_usd`, `duration_seconds`).
- Feed them through your `report_benchmark` MCP tool → `insert_benchmark_run` → `arbiter.db`. 3 passes available per agent; `get_benchmark_score` reads latest-ts, so ingest in pass order (or just the latest pass per agent).

**Alignment confirmed:** `agent_id` values `claude_code`/`codex_cli` match `config/agents.toml`; `benchmark_id: code-review` matches `benchmark_id_for(TaskType::Review)`. No id drift. `deepseek` is a labeled API baseline — ingest if you want the data point, but it is not in your routable registry.

## Task-4 steps (your side; mechanism already built)

1. Ingest the payloads (above) → `benchmark_runs`.
2. **A/B:** route a Review task with `ARBITER_BENCH_WEIGHT=0` (baseline) then `>0` (e.g. 2.0). Confirm (a) the chosen agent shifts toward `claude_code`, (b) the `bench_adjust` audit line fires in `decision_path`, (c) a non-Review task is unaffected (scoping). This mirrors your seeded `it_08` integration test, now on real scores.
3. Record the **mechanism gate** result (read→rerank works on real per-agent data — the first live confirmation).
4. Write the A/B report (`_cowork_output/status/2026-06-13-r07-phase1-ab.md` per your plan).

## Caveats / what's NOT covered

- **Narrow signal:** 2 separating cases. atp-platform can widen FP-discipline cases (codex over-flags deserialization — probe more safe-but-scary patterns) for ≥2-concordant robustness. Say if you want that before the A/B.
- **Cost/latency:** codex_cli is **faster** (142s vs claude's 254s/pass) at comparable tokens but lower review quality. Under a budget-aware weight codex could still win — worth modeling. codex `$` is unmeasured (codex emits no dollar figure; tokens ARE captured now → needs a token→price lookup).
- **Crossover gate (the full task-dependent thesis)** still needs a SECOND benchmark with a matching arbiter `TaskType`. `req-extraction` exists on the atp side but arbiter has no `req-extraction` TaskType (enum: feature/bugfix/refactor/docs/review/research/test) — that's a separate taxonomy decision / Phase-1b, not part of this Task-4.
- **Shelf-life:** the divergence is specific to current codex/claude versions; re-filter on a tool update.

## Pointers
- Matrix (9 agents × 2 benchmarks): `2026-06-17-r07-matrix-and-spend.md`
- P2 filter analysis: `2026-06-17-p2-filter-results.md`
- atp cases: `method/cases/code-review/case-code-review-correctness-*` (merged, PR #195)
