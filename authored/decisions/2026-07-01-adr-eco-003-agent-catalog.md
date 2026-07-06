---
title: "ADR-ECO-003: Unified model & harness catalog"
type: adr
status: accepted
owner: Andrei
updated: 2026-07-01
---

# ADR-ECO-003: Unified model and harness catalog (model-refresh from one center)

**Status:** Accepted (2026-07-01, Andrei) · **Date:** 2026-07-01
**Deciders:** Andrei (owner Maestro / arbiter / ATP)

> **Ratification note (2026-07-01):** Variant A accepted. Consequence for existing
> tooling: `_cowork_output/devtools/gen_agents_toml.py` sources routable agents from
> `benchmark_runs` (arbiter.db) — that is **Variant C**, rejected here (routable ≠
> measured). It is superseded by catalog-driven scaffold (action item #5) and kept
> only as an interim until the arbiter generator reads the catalog. Execution order
> this session: ATP-side slice (#1 catalog → #2 ATP codegen → #3 conformance).

> **Amendment note (2026-07-03, owner):** the canonical SSOT path is
> **`atp-platform/method/agents-catalog.toml`**, NOT `_cowork_output/contracts/`
> (as it stood in TL;DR #3 and the "Catalog schema"). Reason: `_cowork_output` is a purely
> dev-communication workspace between teams/sessions; users and teams that
> install the projects **do not have it**, and putting canon there turns the dev folder into a
> production dependency (the "_cowork_output as a resource for code" anti-pattern). The ATP repo is
> the distributable home with PR/review/CI; arbiter vendors a `config/` copy;
> `_cowork_output/contracts/agents-catalog.toml` is demoted to a **dev mirror for
> communication** (conformance keeps it byte-in-sync, but it is not the source).
> The conformance script and discovery were updated; the rule "`_cowork_output` = dev-only"
> is written into the CLAUDE.md of all five projects.
**Scope:** ecosystem-wide (ATP + Maestro + arbiter)
**Related:** `decisions/2026-06-20-adr-harness-model-management.md` (ADR-ECO-002, D3),
`contracts/add-new-agent-runbook.md`, `contracts/2026-06-19-agent-id-convention-*.md`,
`status/2026-06-19-pm-agent-id-convention.md`
**Amended by:** ADR-ECO-003a (discovery→adoption), 003b (catalog distribution),
003c (breadth + cost classes local⟂cloud), **003d (mechanics of cloud-`$` pricing)**

> This ADR **extends D3 from ADR-002 with a model axis.** ADR-002 focuses on the harness
> (launch mechanics). The owner's recurring need — "the vendor updated a model / a new player
> appeared" — is 80% about **models**, and that axis is under-specified in 002.

## TL;DR

1. **Two different flows, centralized differently.** Flow 1 "the vendor updated a model" (frequent, cheap, pure data) ≠ Flow 2 "a new CLI player" (rare, expensive, needs code). Mixing them into one mechanism is a mistake.
2. **Today one model = an edit across ≥2–3 repos** with a requirement that `agent_id` match **byte-for-byte**; a desync → `get_benchmark_score`=None → re-rank silently no-ops. This is a documented manual procedure (`add-new-agent-runbook.md`), not automation.
3. **Decision:** a single declarative **catalog** (`models` + `harnesses` + `enrollment`) as the SSOT in `_cowork_output/contracts/`, from which the local configs of the three repos are **generated**; CI conformance checks byte-for-byte.
4. **The key asymmetry is preserved:** enrollment into testing (ATP) — automatic; promotion into routing (arbiter policy) — a manual gate (the `routable` flag in the catalog). Because "in the pool" ≠ "grounds to route" (equal scores → re-rank is indifferent).
5. **Policy is not centralized.** `cost_per_hour`, `supports_types`, etc. remain in arbiter's `agents.toml` (a shared agent registry was rejected earlier — policy is each repo's own). Codegen only **scaffolds sections**, it does not invent numbers.

---

## Context

### What hurts (as-is)

The `agent_id="<harness>@<model>"` convention is merged into all three repos (2026-06-19), but managing the list of models/harnesses is manual and smeared out:

| Repo | Where the "list" is | Type of fact |
|---|---|---|
| ATP | `method/run_pipe_check.py:59-89` — `HARNESSES` dict + `AGENT_MODELS` list (literals) | how to **test** |
| Maestro | `spawners/claude_code.py:20`, `spawners/codex.py:20` — `DEFAULT_<H>_MODEL` (env-override, `#32`) + `AgentType` enum (`models.py:75-79`) | how to **execute** |
| arbiter | `config/agents.toml` — `["<h>@<m>"]` section + policy | routing **policy** |

The only thing shared is the `agent_id` string, and it must match **byte-for-byte** (`run_pipe_check.py:76-79` warns explicitly: otherwise the join in `benchmark_runs` silently returns None). The add procedure is described manually in `contracts/add-new-agent-runbook.md` (case A — a new model; case B — a new harness).

### What is already partly done

- ✅ The `agent_id` convention (fused-id) — all 3 repos.
- 🟡 ADR-002 **D1** partial: Maestro `#32` pins `DEFAULT_<H>_MODEL` via env — but `spawn()` does not accept the model as a parameter (`spawners/base.py:56-62`); there is no full pass-through from arbiter.
- ❌ ADR-002 **D2** (open the `AgentType` gate): `scheduler.py:756` is still `AgentType(...)`→`ValueError`→HOLD; the enum = only claude_code/codex_cli/aider/announce/auto.
- ❌ ADR-002 **action item #4** (extract `HARNESSES` into a declarative config) — not done. **This is exactly the first step of this ADR.**

## Decision Drivers

- **Frequency × cost:** a model-refresh happens on every vendor release and must be trivial; onboarding a new harness is rare and tolerates code.
- **Polyrepo is deliberate** — minimum runtime coupling; no shared service in the hot path.
- **Policy per-repo** — an already-adopted decision (agent-id-convention §6); the catalog must not violate it.
- **Fail-loud instead of silent-None** — an `agent_id` desync must be caught in CI, not in prod as a no-op.
- **Testing ≠ routing** — expanding the measurement pool is cheap; changing routing policy — only deliberately (crossover not yet proven, `status/2026-06-18-r07-direction.md`).

## Decision

Adopt **Variant A** — a declarative catalog + generation/vendoring + CI conformance — as the implementation of D3 (ADR-002), extended with a model axis. Separate the planes of **enrollment (auto)** and **routing (gated)**.

---

## Catalog schema (SSOT)

Physically: `_cowork_output/contracts/agents-catalog.toml` (the contract home; polyrepo-neutral — no repo "owns" the shared axis). Each repo **vendors** a pinned copy (like the observability-contract pin `spec-runner@fa6b106`) and generates its local config from it.

```toml
# agents-catalog.toml — the single source of truth

# --- plane 1: MODELS (what the vendor updates) ---
[models."claude-sonnet-4-6"]
vendor  = "anthropic"
status  = "active"        # active | deprecated | retired
aliases = []

[models."gpt-5.5"]
vendor  = "openai"
status  = "active"

# --- plane 2: HARNESS (launch mechanics; = the D3 descriptor) ---
[harnesses.claude_code]
kind       = "cli"                                   # cli | api-baseline | local
shim       = "method/spawners/claude_code_shim.py"   # ATP side
model_env  = "CLAUDE_MODEL"                          # ATP shim env
model_flag = "--model"                               # Maestro CLI flag
routable   = true

[harnesses.pi]
kind       = "cli"
shim       = "method/spawners/pi_shim.py"
model_env  = "PI_MODEL"
model_flag = "-m"
routable   = true
quirks     = ["nonterminating-guard"]                # escape-hatch for the finicky

[harnesses.ollama]
kind     = "local"
routable = false                                     # never routed (baseline)

# --- plane 3: ENROLLMENT (lifecycle of a pair) ---
[[agents]]
harness  = "claude_code"
model    = "claude-sonnet-4-6"
tested   = true      # → enters the ATP sweep
routable = true      # → arbiter agents.toml scaffold (manual flip)

[[agents]]
harness  = "opencode"
model    = "glm-5.1"
tested   = true
routable = false     # measured, but NOT promoted (no separating data)
```

The three planes are not arbitrary: **a model-refresh touches only plane 1** (and, possibly, a row in 3). A new harness touches 2. Promotion — a single `routable` flag in 3.

---

## Generation per repo

| Repo | What is generated from the catalog | Source today | What stays manual |
|---|---|---|---|
| **ATP** (= ADR-002 a.i.#4) | `HARNESSES` + `AGENT_MODELS` (all `tested=true`) → the `AGENTS` dict is built as now | `run_pipe_check.py:59-89` (literals) | the shims' own code (`method/spawners/*_shim.py`) |
| **Maestro** | `DEFAULT_<H>_MODEL` map + harness registration in `SpawnerRegistry` (all `routable=true`) | `spawners/*.py:20` + enum | the spawner code (for a new harness); **requires D2** |
| **arbiter** | **scaffold** of `["<h>@<m>"]` sections in `agents.toml` only for `routable=true` (create/delete the key) | `config/agents.toml` (manual) | **policy fields** (`cost_per_hour`, `supports_types`, `avg_duration_min`) — by hand |

Critical: arbiter generation is **only the key skeleton**, not policy values. This honors "policy per-repo": the catalog decides *which* agents are routable, arbiter — *how* to weight them.

### Dependency on ADR-002

- **Flow 1 (new model)** already works today, **without D2** — same harness, only the model string changes.
- **Flow 2 (new harness → routable)** still **requires D2** (open the `scheduler.py:756` gate) + D1 (model pass-through). The catalog does not cancel D2 — it **feeds** it (the registry is registered from the catalog). Order: D2 → then full auto-generation of the Maestro side.

---

## CI conformance (fail-loud)

A cross-repo check (can live in `_cowork_output/devtools/` and run in each repo's CI against the vendored copy of the catalog):

1. Every `agent_id` with `routable=true` in the catalog → has a section in arbiter `agents.toml` **byte-for-byte**.
2. Every `tested=true` → the ATP-generated `AGENT_MODELS` contains the pair.
3. Every `routable=true` harness → Maestro `SpawnerRegistry.has(harness)` (after D2) / enum (before D2).
4. `safe_agent_id` collisions (`run_pipe_check.py` `_safe_id_collision`) — none.
5. A model with `status="retired"` does not appear in any `[[agents]]`.

This kills the "silent None → re-rank no-op" class, which today is caught only by eye.

---

## Owner of model statuses and deprecation

- `models.*.status` — a **centralized fact** (Andrei/PM), because the vendor lifecycle is cross-cutting. Deprecation = flipping `status="deprecated"` in one place; codegen excludes it from sweeps on the next run; `retired` — a CI-fail on a live reference.
- **Promotion into routing stays a manual** flip of `routable=true` — that is the deliberate gate (after crossover is proven, not automatic).

---

## Options Considered

| Variant | Essence | Assessment | Verdict |
|---|---|---|---|
| **A. Catalog + codegen/vendor + CI** | an SSOT file; repos generate local configs; CI byte-for-byte | One center for *data*, zero runtime coupling, fixes the desync | ✅ **chosen** (= D3 + model axis) |
| B. Runtime registry service | all repos fetch the list from a live service | auto-discovery, but runtime coupling + SPOF, and it drags policy along | ❌ against polyrepo; excessive |
| C. Auto-discovery of routable from `benchmark_runs` | arbiter picks up the measured ones itself | routable≠measured: it will route baselines (ollama, ablation) | ❌ needs a flag → reduces to A |
| D. Only a consistency CI linter | does not cut the N edits, but catches the desync | cheap | 🟡 taken **as part of A** (step 4), not instead |

### Trade-off

B builds a service for what a static file + generation solves; it breaks the polyrepo ethos. C looks "clever," but it conflates measurement and routing — dangerous (it will route what must not be routed). A gives "one center" for the regular case (refresh) with not a single line of runtime coupling and reuses an already-adopted pin pattern (observability-contract).

---

## Consequences

**Becomes simpler:**
- Model-refresh = 1 catalog edit (+ a sweep run + optional `routable` flip). Flow 1 — without D2.
- A new vendor/model is added to testing trivially; deprecation — a single flag.
- An `agent_id` desync is caught in CI, not as a silent no-op in prod.

**Becomes harder / to watch:**
- A codegen step appears in each repo (a guard is needed: the generated is not hand-edited — a `# GENERATED` marker).
- The vendored copy of the catalog can go stale → pin + a CI version check (like the spec-runner pin).
- arbiter policy fields are still by hand — codegen does not touch them (deliberately).

**Revisit:**
- If the routable pool stops being small and policy starts duplicating en masse — return to the question of generating policy defaults (but not now).
- Flow 2 is fully automated only after D2 (ADR-002).

## Action Items

1. [x] **Catalog:** ✅ 2026-07-01 — `_cowork_output/contracts/agents-catalog.toml` created (3 planes, 13 pairs, routable = claude_code@sonnet-4-6 + codex_cli@gpt-5.5).
2. [x] **ATP (ADR-002 action item #4):** ✅ 2026-07-01 (atp-platform commit `464caec`, branch `adr-eco-003/atp-catalog-loader`) — `run_pipe_check.py` loads `HARNESSES`+`AGENT_MODELS` from the vendored copy `method/agents-catalog.toml` (`_load_agent_catalog()`); byte-for-byte equivalent to the former literals, tests green.
3. [x] **devtools:** ✅ 2026-07-01 — `_cowork_output/devtools/check-agent-id-conformance.py` (5 checks, pre-D2), `make conformance`. Green against the live repos; fail-loud verified.
4. [ ] **Maestro:** generate `DEFAULT_<H>_MODEL` from the catalog; **blocked by D2**. As-is: the literals `DEFAULT_CLAUDE_MODEL="claude-sonnet-4-6"` / `DEFAULT_CODEX_MODEL="gpt-5.5"` (spawners/*.py:20) COINCIDENTALLY match the catalog (no live drift), but are NOT generated from it; the `scheduler.py:756` `AgentType(...)` gate is in place.
5. [x] **arbiter:** ✅ 2026-07-01 (Variant A) — `arbiter/scripts/gen_agents_scaffold.py` reads the vendored `config/agents-catalog.toml`, `load_routable_ids()` takes `routable=true` (not `benchmark_runs`), keys-only with KEEP/NEW/STALE reconciliation (stubs for not-yet-measured routable). Test `arbiter/tests/test_gen_agents_scaffold.py`. A 2nd vendored copy `arbiter/config/agents-catalog.toml` appeared → conformance check #2 extended to it (both copies == SSOT). `devtools/gen_agents_toml.py` (Variant C) is superseded — it remains only optionally for cost/duration seeding.
6. [x] **Runbook:** ✅ 2026-07-01 — `contracts/add-new-agent-runbook.md` rewritten around the catalog: both sequences start with an SSOT edit; case A = catalog edit + re-vendor + sweep; verification via `make conformance`; D3 marked implemented; `gen_agents_toml.py` marked an interim Variant C.
7. [x] **Owner:** ✅ recorded in the catalog header (`owner: Andrei/PM`, "Lifecycle owner — PM/Andrei; retired → CI-fail"). Deprecation = a `status` flip in the catalog.

---

## Appendix: key references

- `atp-platform/method/run_pipe_check.py:59-89` — `HARNESSES`/`AGENT_MODELS` literals (migration target)
- `atp-platform/method/run_pipe_check.py:92-100` — assembly of the `AGENTS` dict (stays)
- `arbiter/config/agents.toml` — 3 sections; policy fields that we do NOT centralize
- `Maestro/maestro/spawners/claude_code.py:20,72,82` — `DEFAULT_CLAUDE_MODEL` + `--model` (interim #32)
- `Maestro/maestro/scheduler.py:751-756` — the `AgentType(...)` gate (D2, blocker of Flow 2)
- `Maestro/maestro/models.py:75-79` — the `AgentType` enum
- `_cowork_output/contracts/add-new-agent-runbook.md` — the manual procedure (as-is)
- `_cowork_output/decisions/2026-06-20-adr-harness-model-management.md` — ADR-002 (D1–D4)
