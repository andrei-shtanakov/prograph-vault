# Idea #17 (architect/editor split) — Maestro fit assessment (bounded spike)

> Source idea: `2026-07-22-ideas-from-ai-repos-research.md` #17 (aider
> `architect_coder.py`): architect model reasons in prose, a separate editor
> model makes mechanical edits, cost aggregated across both; note tagged it for
> spec-runner / Maestro / arbiter.
>
> This is a **fit assessment only** — no implementation. Decision gate at the
> bottom.

## The four questions

### Q1 — Is aider actually used in Maestro configs/routing/catalog/tests?
**Registered but model-unaware; not actively model-routed.**
- aider is a first-class spawner: registered in `examples/*.yaml`, the cli
  default spawner set (`cli.py:138,533`), bench agents (`cli.py:103`), and has
  interface/registry tests (`test_spawners.py`, `test_spawner_registry.py`).
- BUT Maestro explicitly treats it as **model-unaware**: `cli.py:1105` — "aider
  ignores model"; `spawners/aider.py` marks its `model` param "unused (no model
  concept)" and passes **no** `--model` in argv (the only spawner that resolves
  no catalog model).
- Arbiter routing keys on `<harness>@<model>` (`models.py:105`); aider has no
  model, so `model_of_agent_id` returns None and it falls back to its own
  default. No policy-tree evidence of aider being model-routed.
- **Verdict:** interface-present, low-signal usage; the least model-aware harness.

### Q2 — Is there user demand for architect/editor among Maestro users?
**None found.** grep across `TODO.md`, `docs/`, `DOGFOOD_LOG.md`, and
`prograph-vault/authored/notes/` (excluding the source idea file) returns no
mention of architect/editor, editor-model, or planner+editor. #17 is purely
research-derived, not a user/dogfood request.

### Q3 — Can the current cost/outcome/routing contract represent a model pair?
**No — the contract is single-model per agent.**
- Routable identity is one `<harness>@<model>` and `report_outcome` stats are
  **per-model** (`models.py:113`). There is no representation of a
  (architect-model, editor-model) **pair** as one routable unit.
- Cost: `TaskCost.cost_usd` is one number per task; aider is priced from token
  counts (`cost_tracker.py:30`). aider aggregates architect+editor cost
  **internally**, so Maestro already sees a single collapsed number — it cannot
  attribute cost to the two distinct models, and the split is invisible to it.
- Making the pair a first-class routable unit would require extending the
  `agent_id`/outcome contract — which is the **arbiter's** contract (read-only
  neighbor repo), not Maestro's to change.

### Q4 — Does the capability belong to spec-runner or a separate harness?
**Yes — it's a harness-internal concern.** "Architect reasons → editor edits →
apply" is exactly what a coding harness does; aider already implements it
natively (`--architect --model A --editor-model E`) and aggregates the cost.
Maestro orchestrates external CLIs and does not call LLM APIs. Adopting the
split as a Maestro capability (option C) would turn Maestro into an LLM harness
— a layer violation. The natural homes are the harness (aider, already done) or
spec-runner (which runs tasks inside the worktree).

## Decision gate

| Signal | Finding |
|---|---|
| aider usage (model-aware/routed) | **weak** (registered, model-unaware, not routed) |
| user demand | **none** (research-derived only) |
| cost/outcome contract for a pair | **cannot** (single-model agent_id; arbiter's contract) |
| capability ownership | **harness / spec-runner**, not Maestro's orchestration layer |

Even the narrowest option A (aider `--architect` passthrough) scores poorly: it
invests in the least-used, model-unaware harness, with no demand, and duplicates
aider's own `.aider.conf.yml` config mechanism for no Maestro-level gain — aider
already does the split + cost aggregation internally, so Maestro passing the
flags adds a config surface, not a capability.

**Recommendation: D — do NOT build #17 in Maestro.** It is a harness/spec-runner
concern (aider already ships it). Pivot to a Maestro-native idea; the strongest
adjacent fit is **#25 (cost tracker on EventBus)**, which lands directly on the
event log just activated in PR #96 (`create_event_logger` now wired into
`run`/`orchestrate`), and matches Maestro's role (aggregate cost/observability
across the run). C is excluded (layer violation). A is technically possible but
low-value; revisit only if real aider-architect demand appears.
