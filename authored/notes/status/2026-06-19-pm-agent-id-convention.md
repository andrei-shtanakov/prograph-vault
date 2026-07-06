---
title: 'Status (PM) — the `agent_id = "<harness>@<model>"` convention has landed'
type: note
status: archived
owner: Andrei
updated: 2026-06-19
archived: 2026-07-06
reason: historical status snapshot (bulk-archived on graduation from _cowork_output)
---

# Status (PM) — the `agent_id = "<harness>@<model>"` convention has landed

> Date: 2026-06-19 (Friday), evening snapshot
> Method: `git log/status/grep` across all repositories + reading contract files and consumer code.
> Baseline report for the delta: `_cowork_output/status/2026-06-19-status.md` (morning).
> Mode: read-only; output only to `_cowork_output/`.

## TL;DR

1. **The `agent_id = "<harness>@<model>"` convention was merged into all three repos in a single day.** The contract went through the full handshake cycle (change → ack → confirm) and landed in code: ATP emits the fused-id, arbiter keys the registry and joins `benchmark_runs` by it, Maestro accepts it and reduces to harness. The `report_benchmark-v1` schema **did not change** — only the format of the `agent_id` string.
2. **The morning status was stale by evening.** Maestro broke its 4-week silence today of all days (`#29` accept fused-id + `#30` bump vendored-pin), arbiter brought the convention to master (`#24`, `#25`). The old P0 "Maestro pin rotted by 7–10 commits" is **closed**: the pin is now `f3c955c` (lag — 1 docs commit).
3. **The "uncommitted files" from the morning snapshot turned out to be junk** (`.claude/settings.local.json`, `arbiter/logs/`, a deleted lock) — not work. False alarm cleared.
4. **The contract change is compatibility-preserving:** protocol stayed `1.1.0`, the `route_task` DTO didn't change, R-07 re-rank behavior is gated via `ARBITER_BENCH_WEIGHT` (default `0.0`). In prod the re-rank is **effectively off**.
5. **Still open:** enabling R-07 in prod (weight > 0 + e2e), crossover (the R-07 thesis is only half-proven), COWORK_CONTEXT drift (6th week), R-06b M5 (CLI).

---

## 1. What landed today

A coordinated change of the shared `agent_id` contract — three repos, one day:

| Repo | Role in the contract | Commits (2026-06-19) | Where it is now |
|---|---|---|---|
| **atp-platform** | producer (emits the id) | `1c39e24` data-driven registry + safe filenames; `b64e252` parse model → `SuiteExecution.model`; `5bf6a9a` fail-fast on safe-id collisions | branch `r07/agent-id-convention`; **merged into `main` (origin + local), confirmed by Andrei** ¹ |
| **arbiter** | consumer (reads the score) | `f3c955c (#24)` full registry-key rename; `8b6bfec (#25)` docs/README sync | `master` ✅ |
| **Maestro** | consumer (`chosen_agent`) | `bce7f0f (#29)` accept fused-id + reduce to harness; `b8de57d (#30)` bump pin `7aeb6b1 → f3c955c` | `master` ✅ |

> ¹ At the moment of reading the mounted folder (~17:05), the git snapshot still showed `origin/main = c31c413` and the working branch `r07/agent-id-convention` — a folder-sync lag, not a contradiction. The "merged into main" state is recorded per Andrei's confirmation.

### The contract handshake (in a single day)

`_cowork_output/contracts/2026-06-19-agent-id-convention-*.md`:

1. **change** — ATP proposes the fused-id, open question "fused vs separate field".
2. **ack** (arbiter) — fused format accepted; migration "start fresh, no history carry-over" (there is no usable legacy data in the store); confirmation of the model-id strings requested.
3. **atp-confirm** — both routable keys match byte-for-byte: `claude_code@claude-opus-4-8`, `codex_cli@gpt-5-codex` (codex pinned to `gpt-5-codex`).

---

## 2. Current state of the agent registry (by code layer)

`agent_id = "<harness>@<model>"` is an **opaque join key**. ATP produces it, arbiter and Maestro consume it.

| Layer | File | What it does |
|---|---|---|
| ATP — registry | `atp-platform/method/run_pipe_check.py:62-91` | `HARNESSES` (harness→shim+env) × `AGENT_MODELS` (list of `(harness, model)`) → `AGENTS[f"{harness}@{model}"]` |
| ATP — safe names | `run_pipe_check.py` `safe_agent_id` / `_safe_id_collision` | `[@:.]→_` for filenames; lossy → guard against collisions |
| arbiter — routable registry | `arbiter/config/agents.toml` | **exactly 3 keys**: `claude_code@claude-opus-4-8`, `codex_cli@gpt-5-codex`, `aider` |
| arbiter — loader | `arbiter/arbiter-mcp/src/agents.rs:46` | TOML → `AgentRegistry` → upsert into SQLite |
| arbiter — re-rank | `arbiter/arbiter-mcp/src/tools/route_task.rs:345` | `ARBITER_BENCH_WEIGHT` (default `0.0`) → `apply_benchmark_rerank` |
| Maestro — reduction | `Maestro/maestro/models.py:103` | `harness_of_agent_id()` = `split("@",1)[0]`, backward-compatible |
| Maestro — spawner selection | `Maestro/maestro/scheduler.py:751-756` | harness → `AgentType` → spawner; the full id is stored in `routed_agent_type` for correlation |

**Key asymmetry:** a benchmark row with the new `agent_id` lands in `benchmark_runs` automatically (opaque key), but it **affects routing only if the key is manually added to `arbiter/config/agents.toml`**. There is no auto-discovery from `benchmark_runs`. The key must match the ATP id byte-for-byte, otherwise `get_benchmark_score` silently returns `None` and the re-rank becomes a no-op.

---

## 3. Contract points

| Contract | File | Status |
|----------|------|--------|
| `report_benchmark` schema | `arbiter/arbiter-mcp/tests/contract/report_benchmark-v1.schema.json` vs `atp-platform/method/contract/report_benchmark-v1.schema.json` | ✅ identical, schema unchanged (only the `agent_id` value format changed) |
| MCP protocol version | `arbiter/arbiter-mcp/src/server.rs` | ✅ `1.1.0` unchanged |
| `route_task` DTO | `arbiter/arbiter-mcp/src/tools/route_task.rs` | ✅ DTO unchanged; the **value** of `chosen_agent` changed (`claude_code` → `claude_code@claude-opus-4-8`) |
| Maestro→arbiter vendored client | `Maestro/maestro/coordination/arbiter_client.py:65` | ✅ pin `f3c955c` (was `7aeb6b1`); lag — 1 docs commit |

---

## 4. What remains open

| # | Topic | State | Zone |
|---|---|---|---|
| 1 | **R-07 disabled in prod** | `ARBITER_BENCH_WEIGHT` default `0.0` → re-rank no-op; no enablement plan and no e2e `route_task → report_outcome` on real `benchmark_runs` | arbiter × Maestro |
| 2 | **Crossover not proven** | only `claude_code > codex_cli` dominance on `code-review` confirmed; the winner doesn't change by task type (`status/2026-06-18-r07-direction.md`) | atp × arbiter |
| 3 | **codex `$` unmeasured** | budget-aware re-rank is blind to price; needs a token→price lookup | atp |
| 4 | **COWORK_CONTEXT drift** | versions lie (spec-runner listed 2.0.0, actually 2.7.0; atp 2.0.0); `appgraph/prograph/prograph-vault` unregistered and without git | registry |
| 5 | **R-06b M5 (CLI)** | `maestro benchmark <id>` pending; the full loop is still via a one-off seed | Maestro |

---

## 5. A pitfall (for the future)

Maestro selects the spawner **by harness and does not pass the model chosen into the spawner** (`scheduler.py:751-754` — the full id is stored only in `routed_agent_type` for correlation and per-model `report_outcome`). It's safe for now (one routable-id per harness). But as soon as **two models of the same harness** appear in `arbiter/config/agents.toml` as separate routable agents (e.g. `claude_code@opus` vs `claude_code@sonnet`) and arbiter picks a specific one — the model decision will be lost on spawn: Maestro will spawn the harness with its default model.

---

## Recommended actions

1. **atp-platform (P0):** make sure the convention is available for the weekend sweep from the branch/remote that the run is actually launched from (origin/main). If the sweep pulls from gitlab/main — the convention **isn't there** (`gitlab/main = 48bd4eb`, 40 commits behind).
2. **arbiter × Maestro (P0):** define the R-07 enablement plan — who sets `ARBITER_BENCH_WEIGHT > 0` and when; add an e2e `route_task → report_outcome` on real `benchmark_runs`. Target — before the demo ~2026-06-25.
3. **atp (P1):** codex token→$ lookup + 1–2 FP-discipline cases for signal robustness (move away from "2 cases = the whole signal").
4. **arbiter (P1):** Phase 2 gate — a second routable benchmark (not `code-review`) for crossover; close R-06b **M5 (CLI)**.
5. **COWORK_CONTEXT (P1, 6th week):** update the versions; decide the fate of `appgraph/prograph/prograph-vault` (register them or explicitly mark as untracked; all three are without git).

---

## 6. Simplifying the registration of new agents and CLI tools

> Context: ATP is a shared test platform, its agent set is **deliberately a superset** of arbiter's routable set (agents arbiter doesn't know about — `deepseek/ollama/anthropic_api` — land in `benchmark_runs` but aren't routed, by design). Question: is a shared registry needed and how to simplify adding agents.

### What is actually duplicated

The three repos store **different facts** about an agent; the only common thing is `agent_id` (identity), and that's already shared via the convention.

| Repo | Stores | Purpose |
|---|---|---|
| ATP `method/run_pipe_check.py:62-91` | `HARNESSES` (shim, model env) + `AGENT_MODELS` | launching for the benchmark |
| arbiter `config/agents.toml` | `supports_languages/types`, `max_concurrent`, `cost_per_hour`, `avg_duration_min` | routing policy |
| Maestro `models.py:72` `AgentType` + `spawners/` | how to launch for real work | execution |

### Key fact: arbiter's production registry is already free of duplication

The live path is the `arbiter-mcp` MCP server; it loads agents from `config/agents.toml` via `ArbiterConfig` (`server.rs`, `config.rs`). Adding a routable agent in prod = **one TOML section**. The hardcoded `bench_agents()` are **dev tools**, not prod:

| Location | What it is |
|---|---|
| `config/agents.toml` | production registry (loaded by `arbiter-mcp`) — the single source for routing |
| `arbiter-cli/src/main.rs:46` | `bench_agents()` — CLI smoke tests (`Cargo.toml`: "CLI for Arbiter smoke tests and benchmarks") |
| `arbiter-cli/benches/routing.rs:42` | `bench_agents()` (copy) — Criterion perf bench |

### Assessment of a "shared registry"

| Option | Effort | Coupling | Verdict |
|---|---|---|---|
| **0. Dedup inside arbiter** (CLI → reads TOML) | XS | none | ✅ hygiene, but **low-value**: prod is already clean, only `main.rs` gets fixed |
| **1. Shared catalog file** (vendored as schema, identity + caps) | S–M | low | ⚠️ only against proven drift of ATP↔arbiter capability tags |
| **2. Codegen from a single source** | M–L | medium | ❌ brittle, overkill for a handful of agents |
| **3. Runtime registry/service** | L | high | ❌ new dependency, a step back from polyrepo |

### Pitfalls of option 0 (important)

1. **The perf bench `benches/routing.rs` wants to be frozen — that's a feature.** Criterion measures the same 3-agent tree run to run. Tying it to `config/agents.toml` would make the perf numbers irreproducible. **Keep** the bench frozen (mark with a comment), apply dedup only to `main.rs`.
2. **Option 0 doesn't touch the real cross-repo fragility — silent-None.** When a routable agent is *added* to `agents.toml`, its `agent_id` must match byte-for-byte what ATP emits, otherwise `get_benchmark_score` silently returns `None` → re-rank no-op. Deduplication doesn't catch this.
3. **The truly growing registry is inside ATP, not shared.** Under multi-testing the bottleneck will be the single `HARNESSES`/`AGENT_MODELS` in `run_pipe_check.py` — that's an ATP-internal task (sets per campaign), not a shared registry.

### Refined recommendation (priorities in descending order of benefit)

1. **ATP↔arbiter join guard (high benefit, S):** a contract test "arbiter's routable keys ⊆ `agent_id` actually written into `benchmark_runs`" + a metric/log for a no-op re-rank (a routable agent with zero bench rows). Catches silent-None — the only real cross-repo trap. *Do the actual key-match check **after tomorrow's run** — as of 2026-06-19 there are no ready new keys in `benchmark_runs` yet.*
2. **Dedup `main.rs` → read `config/agents.toml` (hygiene, XS):** leave the bench `benches/routing.rs` frozen.
3. **ATP-internal agent sets per campaign (if the pain is confirmed, M):** a structure inside ATP for multi-testing, not a shared registry.

**Conclusion:** a shared registry (option 1/3) for the scenario "ATP knows agents arbiter doesn't" is **not needed** — on the contrary, it's an argument to keep the sets separate and leave the link as a thin join contract (which already exists). Identity (`agent_id`) is the only necessarily-shared thing, and it's already shared.
