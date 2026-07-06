---
title: R-07 — instructions to the teams after the sweep-2026-06-21 run
type: note
status: archived
owner: Andrei
updated: 2026-06-21
archived: 2026-07-06
reason: historical status snapshot (bulk-archived on graduation from _cowork_output)
---

# R-07 — instructions to the teams after the sweep-2026-06-21 run

> Date: 2026-06-21
> Data source: `atp-platform/_cowork_output/r07-pipecheck/sweep-2026-06-21/` (13 payloads + `sweep.db`)
> Verify tool: `_cowork_output/devtools/gen_agents_toml.py`
> Related: `contracts/add-new-agent-runbook.md`, `decisions/2026-06-20-adr-harness-model-management.md`

## TL;DR

1. **The run is done, the ATP side is closed.** 13 agents, benchmark `code-review`. The payloads are on disk as files.
2. **🔴 Blocker #1 — the data isn't in `arbiter.db`** (`benchmark_runs` = 0 rows). The payloads need ingesting.
3. **🔴 Blocker #2 — key mismatch.** We ran `claude_code@claude-sonnet-4-6` and `codex_cli@gpt-5.5`, but arbiter is configured for `claude_code@claude-opus-4-8` and `codex_cli@gpt-5-codex` → both routable agents would get silent-None.
4. **An owner decision is required:** route on the **run** models (sonnet-4-6 / gpt-5.5), or was this the wrong set. Recommendation — align arbiter to the run models (see below), since the ATP side is closed and this is the only data we have.
5. **Only 2 of 13 are routable** (harnesses with a Maestro spawner: `claude_code`, `codex_cli`). The other 11 are data, not for routing.

---

## ⚠ The decision that must be made FIRST (owner)

The run benchmarked **sonnet-4-6 / gpt-5.5**, not **opus / gpt-5-codex** that arbiter is configured for. Options:

- **A (recommended):** align arbiter to the run models — re-key the routable sections to `claude_code@claude-sonnet-4-6` and `codex_cli@gpt-5.5`. The ATP side is closed, there's no other data; the join will work immediately.
- **B:** keep arbiter on opus/gpt-5-codex — then a new ATP run is needed for exactly those models (but ATP is declared closed), otherwise the re-rank for them is a forever no-op.

The instructions below assume **option A**. If B is chosen — the arbiter steps are the same, but the keys = opus/gpt-5-codex and a run for them is needed first.

> ⚠ Related point for Maestro: until D1 (model-passing, ADR-ECO-002) is done, Maestro executes the harness with the **default** model. For the executed model to match the run model, the harness default in Maestro must point to the same model (sonnet-4-6 / gpt-5.5) — see the Maestro instructions, item 2.

---

## 👥 arbiter team

1. **Ingest the payloads into `arbiter.db`.** Load the 13 `report_benchmark_*.json` from `sweep-2026-06-21/` into `benchmark_runs` via the contract path `report_benchmark` (ATP→arbiter). Verify: `SELECT COUNT(*) FROM benchmark_runs` = 13 rows (one code-review per agent).

2. **Generate the sections and the join report:**
   ```
   python3 _cowork_output/devtools/gen_agents_toml.py \
     --db atp-platform/_cowork_output/r07-pipecheck/sweep-2026-06-21/sweep.db
   ```
   The report already confirms: routable with data = `claude_code@claude-sonnet-4-6`, `codex_cli@gpt-5.5`; the current opus/gpt-5-codex — no data (silent-None).

3. **Re-key the routable sections in `config/agents.toml`** (option A). **Carry over** the policy fields from the current sections (they're model-independent), and set cost/duration by policy, NOT from a raw seed (n=1, benchmark-case scope — unrepresentative for prod tasks):
   ```toml
   ["claude_code@claude-sonnet-4-6"]
   display_name = "Claude Code (Sonnet 4.6)"
   supports_languages = ["python", "rust", "typescript"]
   supports_types = ["feature", "bugfix", "refactor", "docs", "review", "research"]  # "review" present — ok
   max_concurrent = 2
   cost_per_hour = 0.30        # policy (n=1 data is noisy); refine as it accumulates
   avg_duration_min = 18.0     # policy (bench-case ≠ prod task)

   ["codex_cli@gpt-5.5"]
   display_name = "Codex CLI (GPT-5.5)"
   supports_languages = ["typescript", "go", "python"]
   supports_types = ["feature", "bugfix", "refactor", "test", "review"]  # ⚠ ADD "review"
   max_concurrent = 3
   cost_per_hour = 0.20
   avg_duration_min = 12.0
   ```
   **⚠ Critical for the A/B:** the current `codex_cli` has **no `"review"`** in `supports_types` → on code-review tasks codex is filtered out of the candidates (`route_task.rs:250`) and its score isn't used. Without adding `"review"` an A/B between claude and codex on code-review is impossible — there will be one candidate.
   The old opus/gpt-5-codex sections — delete or keep (there's no data for them; on code-review routing they're silent anyway).

4. **Verify join before enabling:** re-run the gen script against `arbiter.db` (now with the ingest) — the report should have no routable keys without data.

5. **A/B in stages:**
   - `ARBITER_BENCH_WEIGHT=0` — run `route_task`, confirm: both agents pass the candidate filter, the choice is as before (re-rank no-op).
   - `ARBITER_BENCH_WEIGHT=0.15` — A/B; check the audit line `bench_adjust[...]` in `pred.path`; verify that claude (score 0.8) gets a boost vs codex (0.8) — on this data the scores are equal, delta ≈0, which is itself a signal (separating cases are needed).

---

## 👥 Maestro team

1. **Confirm spawner readiness.** `claude_code` and `codex_cli` — `is_available()` = true; the vendored pin is already current (`f3c955c`, `arbiter_client.py:65`). No new code for routing to these harnesses is required.

2. **Align the harness default model with the run model (until D1).** Since the model isn't passed to the spawner (`spawners/base.py:57`), Maestro will execute the harness with the default. For the executed model to match the one the decision is built on (sonnet-4-6 / gpt-5.5), set the harness defaults: `claude_code` → `claude-sonnet-4-6`, `codex_cli` → `gpt-5.5`. Otherwise arbiter routes by the sonnet score while Maestro launches opus — a decision/execution mismatch.

3. **Close the e2e loop.** With re-rank enabled: a task with `agent_type=AUTO` → `route_task` → spawn the chosen harness → `report_outcome` back to arbiter on real `benchmark_runs`. Verify that the outcome is written and adjusts `agent_stats`.

4. **Forward (ADR-ECO-002, NOT blockers of this run):**
   - **D1 (model-passing):** the spawner reads the model from `routed_agent_type` and passes it into the CLI → removes the need for item 2 (harness defaults) and unblocks multi-model routing.
   - **D2 (open the `AgentType` gate):** not needed for this run — there are no custom routable harnesses.

---

## 🔗 Joint step (arbiter + Maestro)

Agree on **who and when** sets `ARBITER_BENCH_WEIGHT>0` and launches the first e2e `route_task → spawn → report_outcome`. This is the first live confirmation of the loop on real data (previously it was only on a synthetic seed).

## Order (summary)

1. arbiter: ingest payloads → `benchmark_runs` (13 rows).
2. owner: confirm option A (route sonnet-4-6 / gpt-5.5).
3. arbiter: re-key sections + **add `"review"` to codex** + verify join.
4. Maestro: align harness defaults (sonnet-4-6 / gpt-5.5) + confirm spawners.
5. jointly: `WEIGHT=0` check → `0.15` A/B → e2e outcome.

## Recommended actions

- **arbiter (P0):** ingest + re-key + `"review"` in `codex_cli` supports_types (otherwise A/B on code-review = one candidate).
- **Maestro (P0):** align the harness default model with the run model, otherwise decision≠execution.
- **owner (P0):** confirm option A vs B (route the run models or re-run opus/gpt-5-codex).
- **both (P1):** assign an owner for the `ARBITER_BENCH_WEIGHT` flip and the e2e run.
