---
title: Agent-id convention — ATP confirmation
type: contract-snapshot
status: living
source: _cowork_output/contracts/2026-06-19-agent-id-convention-atp-confirm.md
sha256: 91ee776ad5c3d24a3e08beb8c62857965d2a594f6c23d38cc99cb60a45ef0d18
updated: 2026-07-06
---

# ATP confirmation: model-id strings for `<harness>@<model>` join

**From:** ATP (R-07)
**To:** arbiter team
**Date:** 2026-06-19
**Re:** `contracts/2026-06-19-agent-id-convention-ack.md` (your ACK + model-id request)

> **⚠️ AMENDED 2026-07-01 — both routable keys below were re-keyed after signing.**
> The original table (opus / gpt-5-codex) is **superseded** and kept struck-through
> for provenance only. Both models named on 2026-06-19 are now dead:
> - `codex_cli@gpt-5-codex` → **`codex_cli@gpt-5.5`** — `gpt-5-codex` rejected on a
>   ChatGPT account (`contracts/2026-06-20-codex-model-rekey.md`).
> - `claude_code@claude-opus-4-8` → **`claude_code@claude-sonnet-4-6`** — arbiter
>   R-07 sweep re-keyed onto the swept models, the only ids carrying code-review
>   benchmark data (`arbiter/config/agents.toml:5,13`, 2026-06-21).
>
> **Live routable join keys (source of truth as of 2026-07-01):**
>
> | agent_id ATP emits (`run_pipe_check.py`) | arbiter registry key (`agents.toml`) | match |
> |---|---|---|
> | `claude_code@claude-sonnet-4-6` | `claude_code@claude-sonnet-4-6` | ✅ exact |
> | `codex_cli@gpt-5.5` | `codex_cli@gpt-5.5` | ✅ exact |
>
> Runtime join is correct today (verified `method/run_pipe_check.py:76-89`). This
> amendment closes the *documentation* drift where the signed table still named the
> dead keys. Future re-keys MUST update this file in the same PR.

## ~~Confirmed — both routable ids match your registry keys~~ (superseded — see amendment above)

| ~~agent_id ATP emits~~ | ~~your registry key~~ | ~~match~~ |
|---|---|---|
| ~~`claude_code@claude-opus-4-8`~~ | ~~`claude_code@claude-opus-4-8`~~ | ⚠️ dead key |
| ~~`codex_cli@gpt-5-codex`~~ | ~~`codex_cli@gpt-5-codex`~~ | ⚠️ dead key |

~~Codex was previously unpinned; ATP pins `CODEX_MODEL=gpt-5-codex` for the sweep and registers `("codex_cli", "gpt-5-codex")`, so the emitted id is exactly `codex_cli@gpt-5-codex`. **No re-key needed — the join works on first run.**~~ (superseded 2026-06-20)

## Non-routable rows you'll also receive (FYI, no action)

ATP also sweeps these; they land in `benchmark_runs` (opaque key) but are not in your routable set — expected:
- `anthropic_api@claude-opus-4-8` — labeled "harness vs raw API" baseline (same model as `claude_code`, raw Anthropic Messages API). By design it never substitutes the CLI agent in routing.
- `deepseek@deepseek-chat`, `ollama@llama3.2:1b|3.2:3b|qwen2.5:3b|7b|14b` — local/API breadth for the deterministic signal.

(Exact extra-model set may grow for the weekend sweep; none affect routing — only the two confirmed keys above do.)

## Acknowledged on our side
- Fused-format + start-fresh (no historical migration) — agreed.
- Maestro `chosen_agent` value-change coordination is your track; does not block the ATP→arbiter `report_benchmark` direction.

**Net: you are clear — both routable join keys are confirmed exact.**
