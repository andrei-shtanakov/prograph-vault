---
title: R-07 Phase 1 — pipe-check proof (2026-06-13)
type: note
status: archived
owner: Andrei
updated: 2026-06-13
archived: 2026-07-06
reason: historical status snapshot (bulk-archived on graduation from _cowork_output)
---

# R-07 Phase 1 — pipe-check proof (2026-06-13)

> Scope: **pipe-check only**, NOT a benchmark. Question answered: *does the
> code-review eval trube pass a real signal end-to-end with a live agent + judge?*
> Answer: **yes.**

## Setup
- Agent under test: live `claude` CLI (`claude-opus-4-8`) via `method/spawners/claude_code_shim.py`, `--adapter=cli`, `agent_id=claude_code`.
- Judge: `qwen2.5:14b` via local Ollama (`ATP_JUDGE_PROVIDER=openai`, `base_url=localhost:11434/v1`).
- Cases: `method/cases/code-review/` (clean + moderate, SEC-011). `--runs=1`.

## Result
| case | score | reading |
|---|---|---|
| clean (compliant diff) | **92.0** | agent correctly reported zero violations; judge graded quality high |
| moderate (planted SEC-011) | **0.0** | `critical_check` failed (hard-gate) |

Scores **differ per case (92 vs 0)** → the pipe carries a real, case-discriminating
signal end-to-end: shim runs live claude → review artifact → LLM judge → critical_check
hard-gate → materialized score. Pipe-check **PASS**.

## Key finding (the reason to run a check)
**`inherit_environment=true` is REQUIRED** in the CLI adapter-config for the claude_code
shim. The CLIAdapter's default minimal env (`PATH/HOME/LANG/TERM` only) makes `claude`
exit non-zero with empty stderr (auth/Node env missing) → "empty/failed, no artifacts",
both cases fail in ~2.5s. With `inherit_environment=true` the run succeeds (18s / 48s).
The shim itself is correct in isolation (verified directly). Baked into the plan's run command.

Bonus: claude correctly **ignored a prompt-injection** string that leaked into the diff
payload ("SessionStart hook…") and limited itself to the review — good agent behavior.

## Caveat → motivates Phase-1b axis #1
`moderate=0` on a single run with an LLM judge grading prose is **non-deterministic**:
the agent may have missed line-12 / flagged a distractor, OR the qwen judge mis-graded
the NL `critical_check`. This is exactly why the top Phase-1b upgrade is **structured
JSON findings + a `programmatic` critical_check** (deterministic recall/precision), per
the 2026-06-13 design review. The pipe-check validated both the trube AND the upgrade rationale.

## Not a go/no-go on routing
Single agent, 2 cases, one language, LLM-judged — this proves the *mechanism*, not a
per-agent routing signal. Crossover/route-shift validity needs Phase-1b (3 spawners,
5-level sweep, structured grading) + a second benchmark (arbiter plan D5 note).

## Next
Phase-1b via brainstorm: #1 (structured + programmatic), #4 (language axis + schema/contract),
#2 (correctness family). #3 (linter usage) explicitly skipped. Tracked in atp-platform `TODO.md`.
