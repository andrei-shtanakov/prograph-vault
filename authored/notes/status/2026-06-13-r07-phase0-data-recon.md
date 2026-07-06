---
title: R-07 Phase 0 — ATP data calibration recon
type: note
status: archived
owner: Andrei
updated: 2026-06-13
archived: 2026-07-06
reason: historical status snapshot (bulk-archived on graduation from _cowork_output)
---

# R-07 Phase 0 — ATP data calibration recon

> Date: 2026-06-13. Context: `arbiter/2026-06-13-r07-thin-slice.md` (+ the review of the same day).
> Phase 0 goal: before writing any code, check whether a real
> per-agent / per-task_type benchmark sample exists in atp-platform on which an A/B slice would be **valid**
> (see review R1). Gate: "no meaningful `task_type→benchmark` mapping → an early
> honest kill-signal without a single line of code".

## Result: the gate tripped — there is no data for a valid A/B

Three independent blockers, each on its own sufficient to make the thin slice
(Phases 1–3) currently **not entitle us to a go/no-go on the direction**.

### Blocker 1 — agent_id do not match the arbiter taxonomy
arbiter routes `claude_code` / `codex_cli` / `aider`. In the real ATP outputs
there are no such agent_id:
- `demo/results/comparison.json` → agents `openai`, `anthropic` (provider adapters).
- `examples/compose-demo/results/method-results.json` → models `qwen7b/14b/3b`, `llama3b`.
- `results/experiment/` → game-theoretic strategies (`tit_for_tat` etc.) — irrelevant.
- `.atp-dashboard.db` → **empty** (all tables 0 rows), contrary to the note's assumption
  "atp-platform is hot, there are real runs".

### Blocker 2 — no coverage by task_type
The only coding comparison (`comparison.json`) is broken into suites
`functional / quality / smoke` — these are **axes of code evaluation**, not the 7 arbiter task_types
(`feature/bugfix/refactor/test/docs/review/research`). There are no benchmarks for bugfix, refactor,
test, docs, review, research at all. There is nothing to build a `task_type→[benchmark_id]` that
**distinguishes agents across task classes** (the R1 premise) out of.

### Blocker 3 — no task-dependent signal even where data exists
Per-suite (openai vs anthropic), `comparison.json`:

| suite      | n | openai | anthropic |   Δ   | winner |
|------------|---|--------|-----------|-------|--------|
| functional | 3 | 92.18  | 90.75     | +1.44 | openai |
| quality    | 3 | 90.46  | 88.45     | +2.01 | openai |
| smoke      | 3 | 99.98  | 99.39     | +0.59 | openai |

openai wins **all** suites (8/9 per-test). This is a monotone global rank
(openai > anthropic everywhere) — exactly the "global per-agent bias" that the review (R1)
flagged as an **invalid** test of the direction. There is no crossover (agent A leading in task_type X,
agent B — in Y).

### Confirmation of R2 (calibration) on real numbers
The scores cluster in 90–100 (two outliers ~73–77). The openai−anthropic gap = 1.35 points
on a scale of 100 ≈ **0.013 on [0,1]**. With centering and `weight≤0.15` the confidence shift
is on the order of 1e-3 — orders of magnitude smaller than `PREFERRED_AGENT_BOOST=0.1`. The effect would
drown in noise, exactly as R2 predicted.

## Interpretation (important: this is NOT the kill R1 warned against)

Two conclusions must be distinguished:
- **"We ran a valid A/B → the route does not move"** — this would be an honest kill of the direction.
  We did NOT observe this.
- **"The inputs for a valid A/B do not exist"** — this is the observed fact. The
  benchmark-aware routing direction **is not falsified, it is not supported by data.**

The key conclusion for the strategy: the thin slice was conceived as a "cheap experiment BEFORE
reviving Maestro". Phase 0 shows that a cheap experiment **cannot be
valid** without real runs of three agents (claude_code/codex_cli/aider) across
differentiating task_types — and that is precisely R-06b M5 (the full loop) that the slice tried
to bypass. So the slice in its current form **does not de-risk the direction**, it would only generate
a misleading globally-biased signal.

## Fork (decision — up to the owner)

- **A. Pause/kill at the data level.** Record R-07 as paused: "no per-agent ×
  per-task_type data"; do not write Phases 1–3. Cheap, honest, reversible.
- **B. Data first (R-06b M5).** Close the Maestro CLI `maestro benchmark
  <id> --agent ...`, run real claude_code/codex_cli/aider across several
  task_types, then re-run Phase 0 with valid inputs. More expensive, but the only
  path to a real go/no-go.
- **C. Synthetic seed just for wiring the code.** Use
  `atp-platform/tests/fixtures/comparison/leaderboard.py` (a generator of realistic
  per-agent scores with skill-level 0.3–0.95 and crossover) → seed differentiated
  **synthetic** data to validate that the re-rank mechanics (Phase 1 code +
  golden R4/R5) work. Explicitly NOT a test of the hypothesis — only "the mechanism is wired".

Reviewer's recommendation: **A now + B as a precondition of any future return to R-07**.
C is justified only if there is an independent need to close the engineering debt of "the reader is wired"
(revive the dead `benchmark_runs`) without waiting for Maestro — but that is engineering, not a signal.

## Artifacts inspected in Phase 0
- `atp-platform/.atp-dashboard.db` — empty (schema present, 0 rows in all tables).
- `atp-platform/demo/results/comparison.json` — openai/anthropic × 9 tests (functional/quality/smoke).
- `atp-platform/examples/compose-demo/results/method-results.json` — qwen/llama, req-extraction, scores 100.0 (zero variance).
- `atp-platform/results/experiment/` — a game-theory tournament (irrelevant to routing).
- `atp-platform/tests/fixtures/comparison/leaderboard.py` — a synthetic generator (fallback for path C).
- arbiter: `benchmark_runs` schema (db.rs:903), `report_benchmark-v1.schema.json`, `TaskType` ×7 (types.rs:50).
