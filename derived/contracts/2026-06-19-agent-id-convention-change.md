---
title: Agent-id convention — change
type: contract-snapshot
status: living
source: _cowork_output/contracts/2026-06-19-agent-id-convention-change.md
sha256: aec59d08dfd90d0013895c3fb4021327df5e721814d8eb1cdd8d71cdf0e764df
updated: 2026-07-06
---

# Proposal: `report_benchmark` `agent_id` → `<harness>@<model>` convention

**From:** ATP (R-07)
**To:** arbiter team
**Date:** 2026-06-19
**Status:** ACKED by arbiter 2026-06-19 — arbiter is updating their side + informing Maestro; ATP implementing. (Original: PROPOSAL pending ack.)
**ATP-side design:** `atp-platform/docs/superpowers/specs/2026-06-19-agent-id-convention-design.md`

## Why

In the `report_benchmark-v1` payloads ATP emits (and the dashboard/store mirror), `agent_id` today conflates two axes inconsistently:
- cloud/CLI agents are named by **harness only** — `claude_code`, `codex_cli`, `anthropic_api`, `deepseek` — with the model implicit (pinned to `claude-opus-4-8`);
- local agents fuse **harness + model** — `ollama_qwen25_14b`.

As the weekend sweep adds more models (incl. running one harness on multiple models), a harness-only id **collides**: two distinct models share one routing key, and the model — a first-class dimension — is invisible in the key for everything except ollama.

## Proposed change

`agent_id = "<harness>@<model>"` with the **faithful provider model id**:

| Before | After |
|---|---|
| `claude_code` | `claude_code@claude-opus-4-8` |
| `anthropic_api` | `anthropic_api@claude-opus-4-8` |
| `codex_cli` | `codex_cli@gpt-5-codex` (model now declared, was unpinned) |
| `deepseek` | `deepseek@deepseek-chat` |
| `ollama_qwen25_14b` | `ollama@qwen2.5:14b` |
| `ollama_llama32_1b` | `ollama@llama3.2:1b` |
| `ollama_qwen25_3b` / `_7b` / `ollama_llama32_3b` | `ollama@qwen2.5:3b` / `:7b` / `ollama@llama3.2:3b` |

`@` is the single harness/model separator (harness left, model id verbatim right; the model may contain `:`/`.`/`-`). The id **remains a valid opaque key** — you do not have to parse it. Splitting on the first `@` to recover `(harness, model)` is available if you want the model as a routing feature.

## What this asks of arbiter

You treat `agent_id` as an opaque key (`AgentConfig` registry keyed by it; `db.get_agent_stats(agent_id)` etc.). So this is **not a parser break**, but you will need to:

1. **Update your `AgentConfig` registry** entries to the new ids (rename the keys, or add new entries).
2. **Migrate historical keys** in your `benchmark_runs` / stats (rename old → new, or alias) — or accept the old rows as legacy and start fresh on the new ids. Your call.
3. **Optional:** if you want `model` as a routing feature (`features.rs`), parse `agent_id.split('@', 1)`. The harness alone (left of `@`) is the natural grouping for "harness vs API" ablations.

## Open question for you

We chose to **fuse model into `agent_id`** (consistent with ollama). If you'd instead prefer the model as a **separate structured field/feature** (agent_id stays the harness, model travels alongside), say so — ATP can emit that instead. We lean to the fused id because it is self-describing and needs no schema change, but the routing key is yours to constrain.

## Timeline

- ATP holds code until your ack.
- Target: land before the weekend paid sweep (~2026-06-20/21) so the run emits the new ids; the demo is ~2026-06-25.
- The `report_benchmark-v1` **schema is unchanged** — only the `agent_id` string value format changes (additive-safe; no new required fields).

**Please reply with: ack / change-request (esp. on the fused-vs-separate question) / migration preference for your historical keys.**
