---
title: Codex model re-key
type: contract-snapshot
status: living
source: _cowork_output/contracts/2026-06-20-codex-model-rekey.md
sha256: 2dd05df8c8625aef0341ae3c723296224f583881cffcb07ae15498f99c528b90
updated: 2026-07-06
---

# Heads-up: codex routable key changed — `gpt-5-codex` → `gpt-5.5`

**From:** ATP (R-07)
**To:** arbiter team
**Date:** 2026-06-20
**Re:** `contracts/2026-06-19-agent-id-convention-atp-confirm.md` (where we confirmed `codex_cli@gpt-5-codex`)

## What changed

On the 2026-06-20 weekend sweep, `codex exec -m gpt-5-codex` returned
`400 invalid_request_error: "The 'gpt-5-codex' model is not supported when using
Codex with a ChatGPT account."` The available models are `gpt-5.5` (codex's
configured default), `gpt-5.4`, `gpt-5.4-mini`.

ATP now pins **`gpt-5.5`** and therefore emits the routable id **`codex_cli@gpt-5.5`**
(was `codex_cli@gpt-5-codex`). Shipped in atp-platform PR #202 (merged → main).
Verified live: codex on gpt-5.5 produced a real result (`critical_pass_rate ≈ 0.80`
on code-review, vs the bogus `0.0` infra-failures under the unavailable model).

## Action for arbiter (one line, NOT urgent)

Update the codex routable key in `config/agents.toml`:

```
- codex_cli@gpt-5-codex
+ codex_cli@gpt-5.5
```

**Timing:** not blocking. Your R-07 re-rank is gated off in prod
(`ARBITER_BENCH_WEIGHT=0.0` → no-op), so nothing breaks today. But the key must
match byte-for-byte **before you enable R-07 routing on real `benchmark_runs`**,
or `get_benchmark_score("codex_cli@gpt-5-codex", "code-review")` returns `None`
and codex's re-rank becomes a silent no-op.

The other routable key, `claude_code@claude-sonnet-4-6`, is unchanged.

## Context: full Tier-1 roster ATP now emits (code-review)

Routable (yours): `claude_code@claude-sonnet-4-6`, `codex_cli@gpt-5.5`.
Non-routable (land in `benchmark_runs`, opaque keys, by design):
`anthropic_api@claude-sonnet-4-6`, `deepseek@deepseek-chat`,
`mimo@mimo-v2.5-pro`, `qwen@qwen3.6-plus`, `ollama@{llama3.2:1b,3.2:3b,
qwen2.5:3b,7b,14b}`. opus fully retired.

**Reply: ack the codex re-key (gpt-5.5), or tell us if you'd prefer a different
available model (gpt-5.4 / gpt-5.4-mini) and we re-pin.**
