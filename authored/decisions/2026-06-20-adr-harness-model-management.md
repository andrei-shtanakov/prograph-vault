---
title: "ADR-ECO-002: Model & custom-harness management in Maestro"
type: adr
status: proposed
owner: Andrei
updated: 2026-06-21
---

# ADR-ECO-002: Model and custom-harness management in Maestro

**Status:** Proposed · **updated 2026-06-21** (D2/D3 re-prioritized — see the section at the end)
**Date:** 2026-06-20
**Deciders:** Andrei (owner Maestro/arbiter/ATP)
**Scope:** ecosystem-wide (Maestro + ATP; arbiter is not affected)
**Related:** `contracts/add-new-agent-runbook.md`, `contracts/2026-06-19-agent-id-convention-*.md`, `status/2026-06-19-pm-agent-id-convention.md`, `status/2026-06-21-r07-team-instructions.md`

> **Update 2026-06-21:** the owner confirmed the goal "expand the routing pool." The D3 trigger
> (≥2 custom harnesses) has effectively been reached → **D2 and D3 move from "later/conditional" to
> "now, P0."** Details and the routable-vs-baseline classification are in the "Update" section at the end.

## TL;DR

1. Two blockers in Maestro: (D1) the model chosen by arbiter **never reaches execution** — the spawner takes the harness, the model is lost; (D2) **custom harnesses cannot be plugged in** without editing the closed `AgentType` enum.
2. Both come down to **one shared fact** — "how to launch harness X and how to pass it a model." This is launch mechanics, and it is genuinely shared between the ATP shim and the Maestro spawner (unlike agent-policy, which each owns separately).
3. **D1:** the spawner reads the model from `routed_agent_type` (Maestro already stores it) + a per-harness model-flag mapping — a mirror of `HARNESSES` in ATP. Size — S.
4. **D2:** open the gate — validate against `SpawnerRegistry` (which is **already pluggable**), not against the `AgentType` enum. Size — S. The registration seam is already in place; exactly one point is closed.
5. **D3 (conditional, later):** a narrow vendored `harness-descriptor` (launch command + model-flag) as a single source for ATP and Maestro — **only once ≥2 custom harnesses exist**. Before that — over-engineering.

---

## Context

After the `agent_id = "<harness>@<model>"` convention (2026-06-19), the model became a first-class routing axis in arbiter. But the consumer — Maestro — does not implement it end-to-end:

- **D1 — the model is lost at spawn.** `AgentSpawner.spawn(task, context, workdir, log_file, retry_context)` (`Maestro/maestro/spawners/base.py:57`) **does not accept a model**; `claude_code.py` builds a `subprocess.Popen` without `--model`. The scheduler reduces `chosen_agent` → harness (`scheduler.py:751-756`) and keeps the full id only in `routed_agent_type` for correlation. → If you register two models of the same harness in arbiter and it picks one, Maestro will spawn the harness with the **default** model.
- **D2 — custom harnesses are closed.** `SpawnerRegistry` already supports `discover_entry_points()` / `discover_from_directory()`, and `register()` accepts any `agent_type` string (`spawners/registry.py:74-97`) — that is, **registration is open**. But the scheduler validates `AgentType(harness_of_agent_id(...))` (`scheduler.py:756`) and raises `ValueError` → HOLD on any harness outside the closed `AgentType` enum (`models.py:72`). The gate is **one** point.

Current state of the layers:

| Layer | Open to custom harnesses / models? | Closed point |
|---|---|---|
| arbiter `config/agents.toml` | ✅ opaque key + policy | none |
| Maestro `SpawnerRegistry` | ✅ entry-points / directory | — |
| Maestro `AgentType` enum | ❌ | validation in the scheduler (`scheduler.py:756`) |
| Maestro spawner | ❌ model is not passed through | `spawn()` signature |
| ATP `HARNESSES` | ❌ dict literal | `run_pipe_check.py:62-68` |

**Forces:** polyrepo was chosen deliberately (minimum coupling); arbiter is already decoupled via the opaque key; the crossover (for whose sake multi-model routing is needed) has **not yet** been proven (`status/2026-06-18-r07-direction.md`) — meaning D1 does not pay off immediately.

## Decision

Adopt **D1** and **D2** as two small independent edits in Maestro; **D3** (the shared descriptor) is a deferred, conditional decision gated on a proven need.

---

## D1 — model-passing in Maestro

### Options Considered

#### A. Spawner reads the model from `routed_agent_id` + per-harness model-flag (recommended)
| Dimension | Assessment |
|---|---|
| Complexity | Low — Maestro already stores the full id; a harness→flag mapping is added |
| Cost | S |
| Coupling | low — the mapping mirrors ATP `HARNESSES[h]=(shim, model_env)` |

**Pros:** minimal code; the harness stays the spawner key; symmetry with ATP; backward-compatible (id without `@` → default).
**Cons:** the harness→flag mapping is duplicated with ATP (a candidate for D3); validation of an unknown model is needed.

#### B. A separate structural `model` field in Task/DTO
| Dimension | Assessment |
|---|---|
| Complexity | Med — change the data model, thread it through the scheduler |
| Cost | M |
| Coupling | medium |

**Pros:** explicitness.
**Cons:** duplicates what already lives in `agent_id`; more changes; the convention specifically moved from separate-field to fused-id.

#### C. Do nothing (pin one model per harness)
**Pros:** zero work. **Cons:** the model in arbiter stays decorative; multi-model routing is impossible.

### Trade-off
B contradicts the already-adopted fused-id convention (ack from 2026-06-19). C forecloses crossover. A reuses data that already exists, plus a fact (model-env per harness) that **already** lives in ATP.

---

## D2 — open the gate for custom harnesses

### Options Considered

#### A. Validate against `SpawnerRegistry`, keep the enum for built-in/AUTO (recommended)
| Dimension | Assessment |
|---|---|
| Complexity | Low — replace `AgentType(h)` with `registry.has(h)`; keep the AUTO sentinel |
| Cost | S |
| Coupling | none |

**Pros:** the registry is **already** pluggable (entry-points/dir); exactly one point opens up; a custom spawner plugs in without touching core.
**Cons:** the compile-time exhaustiveness of the enum is lost; a test is needed to ensure AUTO invariants are not broken.

#### B. A full plugin framework / harness manifests
| Dimension | Assessment |
|---|---|
| Complexity | High |
| Cost | L |

**Pros:** "room to grow." **Cons:** the seam already exists — this is reinvention; classic over-engineering ahead of need.

#### C. Keep the enum, add harnesses by hand (status quo)
**Pros:** simple. **Cons:** every custom AI agent/application = an enum edit + a PR to Maestro core.

### Trade-off
B builds a framework on top of the already-existing registry. C does not scale to "many custom AI applications." A is the minimal edit, consistent with the fact that the registry is already open; the enum remains as a typed convenience for built-ins but stops being a **gate**.

---

## D3 — shared harness-descriptor (conditional, later)

Both D1 and D2 come down to one fact: "the launch mechanics of harness X" (launch command + how to pass the model). This is **genuinely shared** between the ATP shim and the Maestro spawner — unlike agent-policy (see `status/2026-06-19-pm-agent-id-convention.md`, section 6: a shared agent registry was rejected because policy is each repo's own).

**Decision:** a narrow declarative `harness-descriptor` (harness → `{launch command/template, model env/flag}`), vendored as a contract between ATP and Maestro (arbiter is outside it — the opaque id + policy are enough for it). **Introduction trigger:** the appearance of ≥2 custom harnesses. Until the trigger — keep the D1 mapping local to Maestro (a mirror of ATP), do not formalize it.

**Why not now:** one or two harnesses do not justify a shared contract; a premature shared abstraction would raise polyrepo coupling with no confirmed benefit.

---

## Consequences

**Becomes simpler:**
- arbiter can route between models of the same harness — the model reaches execution (D1).
- Custom AI applications/agents plug in via a spawner plugin without touching core (D2).
- ATP data captured now hooks up later without migration (opaque key; the rule is a stable `agent_id` from the first run).

**Becomes harder / needs watching:**
- Validity of the model string for a specific CLI (D1) — a fallback + warn on an unknown model is needed.
- Loss of enum exhaustiveness (D2) — a test of AUTO invariants is needed, and an unknown harness → explicit refusal, not a silent default.
- The harness→model-flag mapping is temporarily duplicated ATP↔Maestro (removed by D3).

**Revisit:**
- D3 — when there are ≥2 custom harnesses.
- D1 payoff — after crossover is proven (then multi-model routing is genuinely needed).

## Action Items

1. [ ] **Maestro D1:** extend `AgentSpawner.spawn` / per-harness spawners — read the model from `routed_agent_type`, inject it into the CLI (`--model`/env); mirror the harness→flag mapping from ATP `HARNESSES`. Test: id without `@` → default (backward-compat).
2. [ ] **Maestro D2:** replace the `AgentType(harness)` validation (`scheduler.py:756`) with a `SpawnerRegistry` check; keep the enum for built-ins + AUTO. Test: a custom entry-point spawner routes; an unknown harness → explicit HOLD.
3. [ ] **Maestro:** run `discover_entry_points()` in the production init path if it isn't wired in yet.
4. [ ] **ATP (for D3 readiness):** extract `HARNESSES` into a declarative config (preparation for a shared descriptor, without formalizing the contract).
5. [ ] **D3 decision:** record the "≥2 custom harnesses" trigger and return to the ADR when it is reached.
6. [ ] **Cross-repo reminder:** for benchmarks outside `code-review`, synchronously add the `task_type↔benchmark_id` pair (`arbiter route_task.rs:42` + ATP `taxonomy.py`).

---

## Update 2026-06-21 — the goal "expand the routing pool"

After the `sweep-2026-06-21` run (13 agents), the owner confirmed: the goal is to **expand the pool of routable agents**, not to stay at two. This changes the ADR's priorities and requires separating two sets.

### Routable ≠ the measurement matrix

The run is a **measurement matrix** (13, at maximum, to find signal/crossover), not the routing pool. Of the 13, only the CLI harnesses are routable-capable (they edit files in a worktree); the rest are baselines by design (labeled in the ATP shims):

| Agent | Type (per ATP shim) | Into the routing pool? |
|---|---|---|
| `claude_code@claude-sonnet-4-6` | CLI harness | ✅ already |
| `codex_cli@gpt-5.5` | CLI harness | ✅ already |
| `opencode@glm-5.1` | CLI harness (marked non-routable) | ✅ **candidate** |
| `pi@gpt-5` | CLI harness, agentic (non-routable) | ✅ **candidate** (slow, 470s; non-termination quirk; its own auth) |
| `deepseek` / `mimo` / `qwen` | raw-API baseline | ⚠️ only if wrapped in a harness |
| `anthropic_api@claude-sonnet-4-6` | ablation (same model, no harness) | ❌ never |
| `ollama@*` (×5) | bare local models | ❌ not a harness; score 0.0–0.73 |

**Realistic pool gain — +2 (opencode, pi).** API baselines are promoted only by writing a coding harness around the API (separate work).

### Re-prioritization

- **D2 (open the `AgentType` gate) — P0, now.** The bottleneck for onboarding custom harnesses.
- **D3 (generic templated spawner) — P0, now (not "at ≥2").** The trigger has been reached. It turns "add a routable agent" into a config edit across 3 repos instead of code. An escape hatch for the finicky ones (template + optional hooks; `pi` — non-termination guard).
- **D1 (model-passing) — rises in value** (a multi-model pool is more realistic).
- **Per-harness vs generic:** for exactly +2, two thin spawners are simpler; generic is justified **if** the pool keeps growing (a research platform — it will). Decision: generic, because the goal is a process, not a one-off +2.

### Data caveat (important for expectations)

opencode and pi on `code-review` scored **0.8 — same as claude/codex**. Promotion **will add routing options but no grounds to prefer them**: re-rank cannot distinguish equal scores. Only crossover (separating cases by task type) provides grounds — the main open front of R-07 (`status/2026-06-18-r07-direction.md`). That is, expanding the pool and proving the pool's usefulness are two different tasks.

### Additional action items (2026-06-21)

7. [ ] **ATP:** reclassify `opencode`, `pi` from baseline to routable (the label in the shims is the source of truth for the routable set).
8. [ ] **Maestro:** implement the generic templated spawner (D3) + open the gate (D2); add `opencode`, `pi` as config entries; a non-termination guard for `pi`.
9. [ ] **arbiter:** `opencode@glm-5.1`, `pi@gpt-5` sections in `agents.toml` (with `"review"` in supports_types).
10. [ ] **method/R-07:** separating cases where opencode/pi differ from claude/codex — otherwise the pool is wider but re-rank is indifferent.
