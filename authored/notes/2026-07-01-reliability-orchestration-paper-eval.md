---
title: Reliability orchestration — paper evaluation
type: note
status: living
owner: Andrei
updated: 2026-07-01
---

# Evaluation of the "reliability orchestration" proposals (from the paper) against the ecosystem code

> Date: 2026-07-01
> Author: PM/architect (cowork)
> Input: a set of proposals from a paper breakdown — confidence/risk/verification_summary/cost
> in the result, statuses NEEDS_REVIEW/VERIFICATION_INCONCLUSIVE, Arbiter strategy
> selection, verifier reliability, ensemble/cost-to-target.
> Checked against: spec-runner, arbiter, Maestro (HEAD 2026-07-01).

## TL;DR

1. **The author's framing is useful, but ~half of the "MVP" is already implemented** — "log the Arbiter decision + reason" and "add cost" are done. The proposals were written without reading the code.
2. **Only two things are genuinely new and valuable:** (a) fail-closed statuses / the `verification` block; (b) **verifier reliability as a data source for the R-07 re-rank** — and this fits into the mechanism already built, which is currently starved on its input (data, not code).
3. **The main risk is not "add a field" but breaking the frozen R-04.** There are two different `status` surfaces; one of them hard-fails on an unknown enum value on the Maestro side.
4. **confidence/risk in spec-runner — reject outright.** The worker has no source of confidence; the number would be synthetic. Confidence belongs to the Arbiter (already there).
5. **Advanced block (ensemble diversity, cost-to-target) — defer:** expensive and/or duplicates existing budget mechanisms.

---

## 1. What from the proposals already exists (crossing out)

| Proposal | Status | Reference |
|---|---|---|
| "log the Arbiter decision + reason" | ✅ Done. `RouteResult` carries `confidence`, `reasoning`, `decision_path`, `fallback_reason`, `invariant_checks`; all persisted in SQLite (`DecisionRecord`). | `arbiter/arbiter-mcp/src/tools/route_task.rs:88-105`; `arbiter/arbiter-mcp/src/db.rs:63-77` |
| "add cost to the JSON result" | ✅ Done. `cost_usd`, `tokens{input,output}`, `duration_seconds`. | `spec-runner/schemas/json-result.schema.json:34-52` |
| "confidence in the result" | ⚠️ Partial. confidence already lives in the Arbiter and in `route_task` response.metadata; it is not in spec-runner (and should not be — see §4). | `arbiter/arbiter-mcp/src/tools/route_task.rs:92` |
| "verification_summary" | ⚠️ Partial. There is a scalar `review` (`passed/fixed/failed/skipped/rejected`), but not a summary object. | `spec-runner/schemas/json-result.schema.json:53-57` |

Conclusion: from the author's MVP list, essentially only **fail-closed statuses** remain.

---

## 2. What is genuinely new and worth taking

### 2.1. Verifier reliability → input for the R-07 re-rank (highest ROI)

The most valuable item. And it **fits into the mechanism already built**, requiring no new architecture:

- The R-07 re-rank is built and deterministic (PR #26 ingest+re-key, PR #27 determinism). The hook: post-inference confidence correction, mirroring `PREFERRED_AGENT_BOOST`. See `_cowork_output/decisions/2026-06-13-r07-thin-slice.md`.
- **The real R-07 blocker is data, not code.** On the canonical `@model` keys the benchmark scores are degenerate (both agents 0.8/0.8 on `code-review`) → the re-rank is a no-op. See `_cowork_output/status/2026-06-21-r07-benchmark2-request-to-atp.md`.
- **Verifier reliability is a natural second separating signal** for the same re-rank: where the benchmarks do not separate agents, the historical reliability of the verifier can. The same ingest path (`report_benchmark` → `benchmark_runs`), the same reader, the same A/B flag. Zero new contract surface on the input.

**Difference from the author:** he proposes calibration as a separate "Advanced." In reality this is the closest increment to the already-burning R-07, not a distant feature.

### 2.2. Fail-closed status — but via the `verification` block, not via the `status` enum

The real gap: there is currently no state "the run passed, but the verifier did not render a verdict." `status` = `done/failed/unknown` (`json-result.schema.json:24-27`).

**The critical contract risk — detailed in §3.** In short: adding a value to the `status` enum is dangerous; adding a field is safe.

---

## 3. Design sketch: how not to break the frozen R-04

### 3.1. Two different `status` surfaces (do not confuse)

| Surface | File | Enum | Who parses it on the Maestro side |
|---|---|---|---|
| **json-result** (stdout `--json-result`) | `spec-runner/schemas/json-result.schema.json:24-27` | `done / failed / unknown` | interop fixtures `spec-runner/tests/fixtures/maestro-interop/` |
| **executor-state** (on-disk state) | `spec-runner/schemas/executor-state.schema.json:41-44` | `pending / running / success / failed / skipped` | `ExecutorState` → `ExecutorTaskStatus` |

### 3.2. Where exactly it will blow up

- Maestro `ExecutorState.model_config = {"extra": "ignore"}` (`Maestro/maestro/models.py:1220`) — **new *fields* are ignored silently, which is safe.**
- BUT `ExecutorTaskStatus` is a `StrEnum` with exactly `pending/running/success/failed/skipped` (`Maestro/maestro/models.py:1155-1160`). `extra="ignore"` ignores unknown *fields*, **but not unknown enum values** — Pydantic will throw on an unknown `status`. That is, **adding a new value to `status` is a hard-fail change**, not an additive one.
- Both schemas stand on `additionalProperties: false` — any new field requires editing the schema + fixtures, otherwise CI interop goes red.

### 3.3. Recommended form (fail-closed by construction)

Do not touch the `status` enum. Add an **additive object** `verification` to json-result:

```jsonc
// json-result: TaskResult (additive)
"verification": {
  "verifier_id": "pytest",       // which verifier
  "verdict": "pass|fail|inconclusive",
  "ran": true                    // did it actually run (fail-closed when false)
}
```

Compatibility invariant: if `verdict=inconclusive` or `ran=false`, `status` stays **safe (`failed`)**, not `done`. Old consumers (unaware of `verification`) see a fail-closed value and do not regress. New ones read `verification` and distinguish "it failed" vs "we couldn't verify."

Order of work so interop does not go red:
1. `spec-runner/schemas/json-result.schema.json` — add `verification` (optional), bump `$id`/version.
2. New fixtures in `spec-runner/tests/fixtures/maestro-interop/` (inconclusive case).
3. Maestro — optional reading of `verification` (additive, `extra="ignore"` already covers it).
4. **Do NOT touch executor-state** — its enum is strictly validated by StrEnum.

The precedent for versioning an additive in the ecosystem is `arbiter_report` with `payload_version: Literal["1.0.0"]` + `extra="forbid"` (`Maestro/maestro/benchmark/arbiter_report.py:151-153`): any drift requires an explicit bump. Apply the same disciplined approach to `verification`.

---

## 4. Where I disagree with the author

**confidence / risk as spec-runner result fields — reject.** spec-runner has no source of confidence: it runs the Claude CLI + verify. Any scalar will be synthetic and mislead downstream. `risk` is even more speculative.
Alternative: the worker emits **facts** (the `verification` block, §3.3), and the **Arbiter computes confidence** from the verifier's historical statistics (§2.1). Confidence belongs to the policy engine — it is already there (`route_task.rs:92`) — not to the worker.

**"Arbiter strategy selection: agent / retry / verifier set / escalation."** The direction is correct (the Arbiter is the policy engine), and `agent` is already selected. But `verifier_set` selection requires the Arbiter to know the catalog of verifiers — that is a **new contract surface** Arbiter↔spec-runner/ATP. Take it only after §2.1 (first learn to *measure* verifiers, then *select* them).

**Advanced block — defer.** `ensemble diversity scoring` requires running several agents/verifiers per task (expensive, conflicts with the budget). `cost-to-target execution mode` largely duplicates the existing `get_budget_status` + `Constraints` in the Arbiter.

---

## 5. Recommended actions (in decreasing ROI)

1. **[arbiter, R-07]** Wire verifier reliability as a second separating signal into the already-built re-rank hook — the same ingest path `report_benchmark`→`benchmark_runs`, the same A/B flag. Closes the data starvation that R-07 ran into (`_cowork_output/status/2026-06-21-r07-benchmark2-request-to-atp.md`).
2. **[spec-runner, R-04]** Add the additive `verification` block + the fail-closed invariant (`status=failed` on inconclusive) — following the procedure in §3.3. Do not touch the `status` enum and do not touch executor-state.
3. **[Maestro]** Optional reading of `verification` (additive, zero risk due to `extra="ignore"`).
4. **Defer:** confidence/risk in the worker, verifier_set selection in the Arbiter, ensemble diversity, cost-to-target.

---

## Appendix: key references

- `spec-runner/schemas/json-result.schema.json:24-27,34-57` — the current result contract
- `spec-runner/schemas/executor-state.schema.json:41-44` — the status of on-disk state
- `arbiter/arbiter-mcp/src/tools/route_task.rs:88-105` — `RouteResult` (confidence/reasoning/decision_path)
- `arbiter/arbiter-mcp/src/db.rs:63-77` — `DecisionRecord` (what is persisted)
- `Maestro/maestro/models.py:1155-1160` — `ExecutorTaskStatus` StrEnum (hard-fail on an unknown value)
- `Maestro/maestro/models.py:1212-1220` — `ExecutorState` `extra="ignore"` (fields ignored)
- `Maestro/maestro/benchmark/arbiter_report.py:151-153` — the precedent for a versioned additive
- `_cowork_output/decisions/2026-06-13-r07-thin-slice.md` — the re-rank mechanism
- `_cowork_output/status/2026-06-21-r07-benchmark2-request-to-atp.md` — the R-07 blocker = data
