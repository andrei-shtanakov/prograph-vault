---
title: Opinion review & agent-id drift
type: note
status: living
owner: Andrei
updated: 2026-06-28
---

# Review of an external opinion + verification of agent-id drift

> Date: 2026-06-28 · Role: TPM / systems architect · Mode: read-only
> Input: an external opinion (Phase 6 + priority list P0–P3 + a 5/5 rating)

## TL;DR

1. **The opinion is architecturally accurate but ~2 weeks out of date.** Its top priorities P0 #1 (fix the arbiter test with agent IDs) and P0 #2 (write `contracts/agent-id.md`) are **already closed** by the contract exchange of June 19–21. Starting with them means doing what's done.
2. **The model-axis drift hypothesis is confirmed — but the bottleneck is not a "failing test" but a silent no-op.** When the `agent_id` key does not match, the benchmark-rerank in arbiter is silently disabled (not an error, but a silent skip) — `route_task.rs:70` + exact string comparison in `db.rs:822`.
3. **The live keys now appear to be aligned on `sonnet-4-6` / `gpt-5.5`**, BUT the signed contract `atp-confirm.md` (19.06) still asserts "confirmed exact" for the **dead** keys `claude_code@claude-opus-4-8` and `codex_cli@gpt-5-codex`. Contract and reality have diverged — exactly the "no single source of truth" ailment the opinion named, in a concrete form.
4. **The live ATP emission path is verified — correct and guarded.** `method/run_pipe_check.py:76-89` emits exactly `claude_code@claude-sonnet-4-6` / `codex_cli@gpt-5.5` (the `AGENT_MODELS` matrix + `f"{harness}@{model}"`, no bare fallback), with an explicit comment `:71-75` that these keys MUST match arbiter, otherwise "silent no-op." The "mine" of bare `claude_code` and `DEFAULT_MODEL=opus` in the live sweep is **not active** (the bare artifacts are pre-convention; opus is overridden by per-agent model injection). What remains is purely **documentation** drift, not runtime.
5. **Re-prioritization:** the highest leverage is not the smoke-yaml itself, but the **identity/outcome contract as a CI invariant** (combine P1 #4 outcome adapter + the agent-id convention into the spine of the work). Phase 6 — defer entirely, it contradicts the opinion's own conclusion "do not add features."

---

## 1. What is correct in the opinion (accept as is)

| Opinion's thesis | Assessment | Rationale |
|---|---|---|
| Clean role separation (Maestro=what/when, Arbiter=who, spec-runner=how locally, ATP=how well) | ✅ Correct | Matches the integration map in `COWORK_CONTEXT.md` |
| `Maestro↔spec-runner` — the most mature pairing | ✅ Correct | The R-04 contract is frozen, fixtures `spec-runner/tests/fixtures/maestro-interop/` |
| spec-runner = local executor backend, NOT a 4th orchestrator | ✅ Correct, low risk | Does not spawn a competing orchestrator; matches the fact |
| Main takeaway: one flawless e2e, document it, run it in CI | ✅ Support | The highest leverage right now |
| outcome adapter (one mapper result→TaskOutcome→report_outcome→ATP record) | ✅ Valuable, but **underrated** (worth P1) | This is the spine of the e2e — see §4 |

## 2. What is out of date / incorrect in the opinion

| Opinion's thesis | Actual status | Files |
|---|---|---|
| P0 #1 "fix the Arbiter test with agent IDs" | **Closed** by the convention | `_cowork_output/contracts/2026-06-19-agent-id-convention-change.md` (ACKed by the arbiter) |
| P0 #2 "write `contracts/agent-id.md`" | **Exists** (under a different name) | `contracts/add-new-agent-runbook.md` + 4 files `…agent-id-convention…` |
| Phase 6 (scope-overlap enforcement, retention, service-account tokens, deployment profiles) | **Contradicts** the opinion's conclusion "do not add features" | — |
| P1 #6 "extract arbiter-py (vendored client)" | Real debt, but **not a blocker** | vendored with SHA-pin + version negotiation works (`COWORK_CONTEXT.md`, Maestro↔Arbiter) |

## 3. Confirmed conclusion: agent-id drift is contract-vs-reality, not a test

### 3.1 Mechanism (why it's dangerous)

The benchmark-rerank in arbiter joins ATP scores to candidates by `agent_id`:

- `arbiter-mcp/src/tools/route_task.rs:70` — `if let Some(score) = db.get_benchmark_score(agent_id, bench)?` … otherwise "**left untouched**" (doc-comment `route_task.rs:51-52`).
- `arbiter-mcp/src/db.rs:821-824` — `WHERE agent_id = ?1 AND benchmark_id = ?2` — **exact** string comparison.

Result: key did not match → row not found → `None` → the rerank **silently** does nothing. This is **not a failing test and not an error** — it is an invisible no-op. The same failure mode described for codex in `contracts/2026-06-20-codex-model-rekey.md:32-33`.

Additionally: the rerank is currently enabled only for `Review → code-review` (`route_task.rs:42-47`), the other task types do not use benchmark data at all.

### 3.2 Chronology of the divergence (three keys for one agent)

| Date | Event | claude key | codex key |
|---|---|---|---|
| 19.06 | `atp-confirm.md` — "confirmed exact", signed | `claude_code@claude-opus-4-8` | `codex_cli@gpt-5-codex` |
| 20.06 | `codex-model-rekey.md` — the API rejected gpt-5-codex | (unchanged) | → `codex_cli@gpt-5.5` |
| 21.06 | `arbiter/config/agents.toml` R-07 sweep re-key | → `claude_code@claude-sonnet-4-6` | `codex_cli@gpt-5.5` |

Comment in `agents.toml:1-4`: re-keyed "onto the swept models (sonnet-4-6 / gpt-5.5), **the only agent_ids with code-review benchmark data**". That is, arbiter moved off opus onto sonnet because the data sits under sonnet.

### 3.3 Current state of the keys

| Source | claude key | File |
|---|---|---|
| arbiter live registry | `claude_code@claude-sonnet-4-6` ✅ | `arbiter/config/agents.toml:5` |
| **Live ATP emitter (code)** | `claude_code@claude-sonnet-4-6` ✅ **matches** | `atp-platform/method/run_pipe_check.py:77` (+ `:71-75` explicit guard comment) |
| Signed contract (19.06) | `claude_code@claude-opus-4-8` ❌ dead | `_cowork_output/contracts/2026-06-19-agent-id-convention-atp-confirm.md` |
| ATP method default | `claude-opus-4-8` ⚠ overridden by per-agent model injection → **not active** | `atp-platform/packages/atp-method/atp_method/envelopes.py:16` |
| Old ATP pipecheck artifacts | bare `claude_code` — **pre-convention, not the live path** | `atp-platform/_cowork_output/r07-pipecheck/*/report_benchmark_claude_code.json:5` |

**Conclusion (refined after checking the live code):** the routable join **works right now and is explicitly guarded** — `run_pipe_check.py:71-75` carries a comment that the keys MUST match arbiter, otherwise the re-rank returns None. So there is no runtime risk. What remains is **documentation** drift: the signed contract `atp-confirm.md` declares "exact" on two dead keys (opus / gpt-5-codex), not reflecting the two re-keys (20.06 codex, 21.06 claude). This misleads anyone who takes the contract as the source of truth, but the code source is currently correct. Severity: low (docs), not high (runtime).

## 4. Re-prioritization (my alternative to the opinion's list)

| From the opinion | My assessment | Why |
|---|---|---|
| P0 #1/#2 (arbiter test, agent-id.md) | **Drop — done** | contract ACKed 19.06, the runbook exists |
| P1 #4 outcome adapter + P1 #7 cross-repo CI smoke | **→ P0, the spine of the work** | a single mapper + a golden agent-id set, validated in the CI of all repos — this is "one e2e," and it also automatically catches the drift from §3 |
| P0 #3/#4 smoke yaml + smoke script | P0, but **as part** of the ecosystem CI, not separately | smoke without conformance will not catch a silent no-op (the rerank is silent, the smoke is green) |
| P1 #6 extract arbiter-py | Keep P1 | vendored+SHA-pin works, not urgent |
| Phase 6 in full | **Defer** | contradicts the "do not add features" conclusion |

The central idea: the opinion hides the most valuable item (the outcome adapter) in the middle. Make it the **single source of truth for identity+outcome** and lock it in as a CI invariant — this attacks the **cause** (no canon for keys/outcomes), not the symptoms.

## 5. Recommended actions

**arbiter**
- Do not touch the live `config/agents.toml` — it is currently correct (sonnet/gpt-5.5). Read-only reminder: at the next model re-key, the contract docs must be updated in the same PR.
- (P1) Consider a log-warning in `apply_benchmark_rerank` when the chosen agent has not a single benchmark row — so the silent no-op becomes visible in observability.

**ATP (atp-platform)**
- The live path `run_pipe_check.py` is already correct (`AGENT_MODELS` + guard comment) — **no action required**. The earlier items about `DEFAULT_MODEL` and bare `claude_code` are withdrawn after the check: the default is overridden, the bare artifacts are pre-convention.
- (P2, hygiene) Clean up the stale bare `claude_code` artifacts in `_cowork_output/r07-pipecheck/` so they do not confuse future imports/analysis.

**Contracts (_cowork_output/contracts)**
- (P0) Update `2026-06-19-agent-id-convention-atp-confirm.md`: the keys are now `claude_code@claude-sonnet-4-6` and `codex_cli@gpt-5.5`. Right now the signed contract points to dead keys.

**Ecosystem / CI (new workstream "identity & outcome contract")**
- (P0) One golden set of `agent_id` + one outcome format (mapper `spec-runner JSON → TaskOutcome → report_outcome → ATP record`), validated by cross-repo CI: a test that fails if `arbiter/config/agents.toml` routable keys ≠ the set of `agent_id` emitted by ATP. This turns "one flawless e2e" from a demo script into a contract invariant and physically closes the drift from §3.

---
*Sources: repository files (read-only), quotes with paths and lines above. The opus/sonnet hypothesis from the previous discussion — confirmed and refined.*
