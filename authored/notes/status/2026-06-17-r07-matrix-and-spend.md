---
title: R-07 — Agent matrix + spend (for arbiter team)
type: note
status: archived
owner: Andrei
updated: 2026-06-17
archived: 2026-07-06
reason: historical status snapshot (bulk-archived on graduation from _cowork_output)
---

# R-07 — Agent matrix + spend (for arbiter team)

**Date:** 2026-06-17
**Data:** `atp-platform/_cowork_output/r07-pipecheck/arbiter-stats.db` (54 rows, 9 agents × 2 benchmarks, **n=3**). Per-agent `report_benchmark-v1` payloads alongside.
**Shims merged:** ollama (#193), codex_cli + deepseek (#194). `codex_cli` agent-id matches `arbiter config/agents.toml` exactly. `deepseek` + `anthropic_api` are labeled **API baselines** (not routable).

## Decisive comparison — routable agents only

Among the 9 agents, P1 added exactly **one** routable agent: `codex_cli`. So the gate is `claude_code` vs `codex_cli`.

| vertical | claude_code (runs) | codex_cli (runs) | gap | sd |
|---|---|---|---|---|
| code-review | 1.00 (1,1,1) | 1.00 (1,1,1) | 0 | 0 |
| req-extraction | 1.00 (1,1,1) | 1.00 (1,1,1) | 0 | 0 |

**Verdict by your criteria:**
- **Saturation: YES.** Both routable agents = 1.0 on both verticals, sd=0.
- **Differentiation:** none (gap 0).
- **Crossover:** none among routable agents.
- **Noise-guard:** gap 0 ≪ 2·sd (sd=0) → trivially not significant.

→ Conclusion: **"benchmarks too easy → raise the ceiling (P2)"**, not "routing doesn't work." The re-rank mechanism (Tasks 1-3, green) has zero signal to act on between arbiter's routable agents on the current benchmarks.

## Full matrix (n=3, critical_pass_rate; sd from min–max)

**code-review:** codex_cli 1.00 · claude_code 1.00 · qwen2.5:14b 0.87 (0.8–1.0) · deepseek 0.87 (0.8–1.0) · anthropic_api 0.67 (0.6–0.8) · llama3.2:3b 0.20 (0–0.4) · qwen2.5:7b 0.13 (0–0.2) · qwen2.5:3b 0.07 (0–0.2) · llama3.2:1b 0.00
**req-extraction:** deepseek 1.00 · codex_cli 1.00 · claude_code 1.00 · anthropic_api 1.00 · qwen2.5:14b 0.75 · qwen2.5:7b 0.42 (0.25–0.5) · llama3.2:3b 0.42 (0.25–0.5) · qwen2.5:3b 0.25 · llama3.2:1b 0.08 (0–0.25)

**Task-dependent crossover exists, but only among non-routable agents:** `anthropic_api` (cr 0.67 / rx 1.00) ↔ `qwen2.5:14b` (cr 0.87 / rx 0.75) invert across verticals. Real direction signal — wrong agents for routing. (The earlier single-run qwen3b↔llama3b crossover was noise; gone at n=3 — confirms P3.)

## Spend / cost-per-score (routable)

| agent | code-review | req-extraction | cost measured? |
|---|---|---|---|
| claude_code | $2.29 / 153.5k tok | $1.88 / 109.5k tok | yes (`claude -p --output-format json`) |
| codex_cli | $0 / 0 tok | $0 / 0 tok | **no** — `codex exec --output-last-message` emits no usage block |

Both score 1.0, so cost/score can't separate them yet — and `codex_cli` cost is currently **unmeasured** (OpenAI billed, not captured). For budget-aware re-rank this is a gap: capture `codex exec --json` usage events (follow-up).

## Holes / follow-ups (your P1–P5)
- **aider** still not in the run → third routable agent missing; needed for the full direction gate. Not a blocker for this run.
- **P2 (binding):** raise code-review difficulty above `very_severe` until `claude_code`/`codex_cli`/`deepseek` diverge. This unblocks the real Task-4 A/B.
- **P3:** n=3 + min–max already here; making it the export default + emitting mean±sd is next.
- **P4:** unify `benchmark_id↔task_type` (Python `atp_method.taxonomy` vs Rust `route_task`) as a versioned cross-repo artifact; arbiter has no `req-extraction` TaskType yet.
- **P5:** round-trip through arbiter's real `report_benchmark` binary (not the local mock table).
- **codex_cli token/cost capture** (above) for budget-aware routing.

## Net
Pipe is technically complete and honest; the task-dependent signal is real but lives on non-routable agents, and the routable pair saturates. **Highest-leverage next step is P2** — without a higher ceiling, arbiter routing between its agents can't change regardless of mechanism.
