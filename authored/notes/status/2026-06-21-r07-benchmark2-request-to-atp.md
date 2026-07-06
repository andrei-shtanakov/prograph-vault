---
title: 'R-07 — request to atp-platform: "benchmark #2" (separating data for routable agents)'
type: note
status: archived
owner: Andrei
updated: 2026-06-21
archived: 2026-07-06
reason: historical status snapshot (bulk-archived on graduation from _cowork_output)
---

# R-07 — request to atp-platform: «benchmark #2» (separating data for routable agents)

> Date: 2026-06-21
> From: arbiter · To: atp-platform
> arbiter context: the re-rank mechanism is closed (PR #26 ingest+re-key, PR #27 determinism). Right now, on the canonical `@model` keys, the data is degenerate → the A/B doesn't demonstrate the value of routing.
> Related: `2026-06-21-r07-team-instructions.md`, `2026-06-17-r07-task4-handoff-to-arbiter.md`, atp `TODO.md` R-07 (axes #2/#4/#5), atp `_cowork_output/r07-pipecheck/SUMMARY.md`.

## TL;DR — what we ask

Produce a **separating** `@model`-keyed run for arbiter's two routable agents and send the payloads via the contract `report_benchmark` (like sweep-2026-06-21). "Separating" = their scores **differ** enough that the re-rank changes the ranking (see the acceptance criterion below). **Any one** of the A/B/C paths is sufficient.

Routable keys (only these two are actually routed — Maestro spawners):
- `claude_code@claude-sonnet-4-6`
- `codex_cli@gpt-5.5`

## Why the current data isn't enough

In `sweep-2026-06-21` (what's ingested into arbiter `benchmark_runs`) both agents on `code-review` gave **0.8 / 0.8**:

| agent_id | benchmark_id | score |
|---|---|---|
| `claude_code@claude-sonnet-4-6` | code-review | 0.8 |
| `codex_cli@gpt-5.5` | code-review | 0.8 |

arbiter re-rank: `delta = (score − 0.5) × weight`. With equal scores the deltas are equal → zero separation → the choice is decided by tree-confidence, re-rank is a no-op. The mechanism is proven (the audit line `bench_adjust[...]` is written to `pred.path`), but **direction/value isn't validated** without diverging data.

NB: the pipe **can** distinguish agents — in the June 15–17 sweep the `crit_pass` spread was 0.00→0.90 (claude 0.90 / codex 0.62). So the problem isn't the pipe, it's that the single canonical `@model` run collapsed both into 0.8 (probably a re-baseline after array→object, see the open flags below).

## Acceptance criterion (what counts as "separating")

Any of:
1. **Global-bias:** on a single benchmark_id the scores of the two routable agents differ by **|Δscore| ≥ 0.15** (at `weight=0.15` this yields a delta ≥ ~0.022 — enough to shift close tree-confidences; the larger the gap, the cleaner the A/B), **or**
2. **Crossover (preferred — this is the deferred task-dependence gate):** agent A > agent B on one slice (language/type) and B > A on another, both with |Δ| ≥ 0.15. This proves that context-based routing beats "always-best".

Plus: ≥ 3 runs per agent per slice (so that 0.8 isn't an n=1 artifact).

## Paths (one is enough)

### Path A — re-run `code-review` after fixing the re-baseline
- Check the effect of the array→object migration on the signal (atp TODO 96–98): `output_contract` steers the prompt to `GENERIC_ENVELOPE`, losing the "senior code reviewer" persona. If that's why both collapsed to 0.8 — restore the separation and re-run both under `@model` keys.
- Cheap, if the root cause is in the prompt.

### Path B — run `code-review-correctness` (#2, already built) under `@model` keys
- A family of 7 cases (logic/spec/distractor/fp) already exists. Run it for both routable agents and send as a **new `benchmark_id`** (e.g. `code-review-correctness`).
- ⚠ Then a **paired edit on both sides** is needed (atp taxonomy + arbiter `route_task.rs::benchmark_id_for`), otherwise arbiter won't use the new benchmark_id in the re-rank. Right now only `Review → "code-review"` is mapped. Ready to add the pair — tell us the final benchmark_id name.

### Path C — #4 language axis (gives crossover, most valuable but pricier)
- The `agent-eval-case` schema has no `language`; we need to split scores by language and carry it into `benchmark_runs`. arbiter routes by language (`features.rs` f[1]/f[16]) — this is a direct input for task-dependent routing.
- This is the deferred crossover gate from arbiter's plan (Task 4 Step 4). It closes the "value of routing" perfectly, but it's the "not started — next axis" in your TODO.

## Data contract (unchanged — as in sweep-2026-06-21)

- Payload: `report_benchmark` v1.0.0 (fields `run_id`/`benchmark_id`/`agent_id`/`score`/`score_components`/`per_task`/…), idempotency by `run_id`.
- `agent_id` strictly in the form `<harness>@<model>` with the same keys that arbiter routes (`claude_code@claude-sonnet-4-6`, `codex_cli@gpt-5.5`). A key mismatch = silent-None in the re-rank.
- Ingest on the arbiter side is already automated: `scripts/ingest_benchmark_payloads.py` + verify via `_cowork_output/devtools/gen_agents_toml.py`.

## Open flags to confirm (may explain 0.8/0.8)

1. **per-task `score` = 0.0** with a high aggregate `critical_pass_rate` (SUMMARY item 4, TODO 72–73) — confirm that per-task carries a non-gating rubric (`mean_rubric=0`), not a slicing bug.
2. **Re-baseline risk** (TODO 96–98) — loss of the reviewer persona after array→object; check the effect on the signal.

## Definition of Done

- [ ] A `@model`-keyed run sent for `claude_code@claude-sonnet-4-6` + `codex_cli@gpt-5.5`, satisfying the acceptance criterion (global-bias |Δ|≥0.15 or crossover), ≥3 runs/slice.
- [ ] If a new benchmark_id (Path B/C) — the name agreed, the pair `benchmark_id_for` (arbiter) ↔ taxonomy (atp) set up.
- [ ] The open flags per-task=0.0 and re-baseline confirmed/closed.
- [ ] arbiter ingests, verify-join is green, the A/B at `ARBITER_BENCH_WEIGHT=0.15` shows a meaningful shift (not a tie).

## What arbiter will do on receiving the data

Ingest → verify join → A/B (`WEIGHT=0` no-op → `0.15`), and (for Path B/C) set up the `benchmark_id_for` pair. Ready to join synchronously for the first live e2e with Maestro.
