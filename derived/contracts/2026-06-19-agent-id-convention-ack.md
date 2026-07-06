---
title: Agent-id convention — acknowledgement
type: contract-snapshot
status: living
source: _cowork_output/contracts/2026-06-19-agent-id-convention-ack.md
sha256: 8f9686a748ce85592c327cdedb33b4a1ba7879485bb9ebe70c00df42ba176f3d
updated: 2026-07-06
---

# ACK: `report_benchmark` `agent_id` → `<harness>@<model>` convention

**From:** arbiter team
**To:** ATP (R-07)
**Date:** 2026-06-19
**Re:** `contracts/2026-06-19-agent-id-convention-change.md`
**Status:** ACK — you are unblocked to implement and emit the new ids for the weekend sweep.

## Decision

1. **ACK the fused `agent_id = "<harness>@<model>"` format.** We agree on the
   fused id over a separate structured field (your open question). It is
   self-describing, keeps `report_benchmark-v1` schema-stable, and matches how
   we treat the id — an opaque routing key. No parser on our side.

2. **Migration preference: start fresh, no historical migration.** Phase 0 data
   recon already established there is no usable legacy ATP data in our store
   (empty dashboard db, agent_id mismatch, no task_type coverage). So there is
   nothing to alias or rename — we start clean on the new ids.

## What we changed on our side (already landed locally, tests green)

We did a **full registry-key rename** so the benchmark join key *is* the
routing key (no split/strip, no second mapping). Our two ATP-benchmarked,
routable agents are now keyed:

| arbiter registry key (new) | matches your emitted `agent_id` |
|---|---|
| `claude_code@claude-opus-4-8` | `claude_code@claude-opus-4-8` |
| `codex_cli@gpt-5-codex` | `codex_cli@gpt-5-codex` |

- `aider` is **unchanged** — you do not benchmark it; its benchmark score stays
  `None` and the re-rank is a no-op for it, which is correct.
- `anthropic_api@…`, `deepseek@…`, `ollama@…` rows you emit will land in
  `benchmark_runs` fine (opaque key) but are **not routable** — arbiter only
  routes to its three configured agents. Only the two keys above influence
  routing via the R-07 re-rank.

This makes `route_task` → `apply_benchmark_rerank` → `get_benchmark_score(agent_id, "code-review")`
join exactly against your rows. Before this change the lookup would have
silently returned `None` and the R-07 A/B (`ARBITER_BENCH_WEIGHT` 0 vs 0.15)
would have been a no-op.

## ⚠️ Coordination note for Maestro (cross-repo, not ATP)

Our routing key is also the value we emit as `chosen_agent` in the `route_task`
response DTO — which Maestro vendors (frozen DTO, `arbiter_client.py` @ `861534e`).
The rename therefore changes the **value** of `chosen_agent` Maestro receives
(`claude_code` → `claude_code@claude-opus-4-8`) and of `preferred_agent` it may
send. **Schema is unchanged; only the string value changes.** This needs a
coordinated arbiter+Maestro release — we are tracking that separately. It does
**not** affect or block ATP: the `report_benchmark` direction (ATP → arbiter)
is purely additive and you can ship now.

## One confirmation requested

Please confirm the exact model id strings you will emit, especially:
- `codex_cli@gpt-5-codex` — your proposal notes Codex was previously **unpinned**;
  we keyed our registry to `gpt-5-codex`. If you pin a different id, tell us and
  we re-key (one-line config change).
- `claude_code@claude-opus-4-8` — matches our pinned model.

If those two are right, the join works on first run.

**Reply: ACK on fused format + start-fresh migration. Awaiting only your model-id confirmation.**
