---
title: R-07 Phase 1 — code-review eval → benchmark → routing MVP
type: adr
status: proposed
owner: Andrei
updated: 2026-06-13
---

# R-07 Phase 1 — MVP vertical: code-review eval → benchmark → routing

> Date: 2026-06-13. Status: design note (proposal). Mode: read-only over the repos.
> Context: `2026-06-13-r07-thin-slice.md` + `status/2026-06-13-r07-phase0-data-recon.md`.
> Decision: the first R-07 vertical = **code-review** (routed as `TaskType::Review`,
> ordinal 5; more deterministic than coding — there is a reference diagnosis, no need to run tests in a sandbox).

## TL;DR

1. **We build one end-to-end slice, not 5 suites.** the code-review family of cases (atp-method) × 3 spawners (`claude_code`/`codex_cli`/`aider`) → new ATP reporter `report_benchmark` → `arbiter.benchmark_runs` → re-rank A/B. We prove the whole pipeline, including the data foundation, on a single vertical.
2. **Taxonomy is fixed: the canon is arbiter's `TaskType`** (it consumes the data). The atp-method axes (`capability`/`construction_axis`/`axis_level`) are an *intra-task* unfolding of difficulty, not a replacement for `task_type`. `benchmark_id="code-review"` ↔ `TaskType::Review`.
3. **The signal comes from the `axis_level` sweep, not from a flat score.** The point at which an agent's `critical_check` begins to fail distinguishes agents *within* code-review — this fixes Blocker 3 of Phase 0 (the flat `comparison.json` gave a monotone global bias Δ≈0.013).
4. **The reader in arbiter gets upgraded: the score must be task_type-scoped.** `get_benchmark_score(agent_id, benchmark_id)` with a filter, otherwise the A/B is invalid (requirement R1). This is a refinement to §3.1 of the thin-slice.
5. **"Export/import between databases" = a new reporter under the M4 contract**, not a bespoke sync. ATP-eval → `report_benchmark-v1` payload → MCP `report_benchmark` → `benchmark_runs`.

---

## 1. Mapping the three taxonomies (closes rake #1)

| Your 5 tasks | Canon `arbiter::TaskType` (ordinal) | atp-method capability | Status for MVP |
|---|---|---|---|
| **code-review** | **Review (5)** | correctness / safety_compliance | ✅ **MVP** |
| coding | Feature (0) / Bugfix (1) / Refactor (2) | correctness, efficiency | Phase 2 |
| documentation | Docs (4) | correctness, calibration | Phase 2 |
| repo-analysis | Research (6) | correctness, recoverability | Phase 3 |
| architecture | — (no slot in the enum) | adaptation | Phase 3 + **decision on the enum** |

> `task_type` is encoded into the vector as `f[0] = task_type.as_ordinal()` (`features.rs:133`) and in `f[15] agent_supports_task_type` (`features.rs:203`). Review is already a valid class — no need to extend the enum for the MVP. architecture-design will require a separate decision (extend `TaskType` or map it onto Research) — deferred until Phase 3.

## 2. MVP suite: the `code-review-planted-defect` family

Each case follows `agent-eval-case.schema.json`. The idea: the agent is given a **diff/PR + an excerpt from the corporate KB rules**, and must produce a review. One defect that violates a specific KB rule is planted in the code; around it are plausible but correct lines (distractors).

### 2.1. `critical_check` — the deterministic backbone (rake #3)
Binary: **the review must flag the planted defect and reference the violated KB rule (`rule_id`)**. A miss or a missing rule reference → the case fails regardless of the rubric. This is not an LLM judgment — it is a match on the presence of the `rule_id` + the defect location in the output (grader `type: programmatic` or `regex` on `rule_id`).

### 2.2. `rubric` — a KB-grounded layer on top (model_graded, on-prem judge)
Weights sum to 1.0: correct severity (0.3), an accurate quotation of the rule, not a paraphrase (0.3), no hallucinated issues on the correct distractor lines (0.25), an actionable fix (0.15). The judge is an LLM-judge via an on-prem `base_url` (v2.1.0), `gold` = the reference review + `rule_id`.

### 2.3. The `axis_level` sweep — the source of the discriminating signal
One `family`, cases differing only in how well the defect is concealed:

| axis_level | Defect construction |
|---|---|
| clean | the defect is obvious, no distractors |
| mild | 1–2 correct distractors nearby |
| moderate | the defect looks "idiomatic", 5+ distractors |
| severe | a logical defect, only surfaces with the KB rule in hand |
| very_severe | a defect via the interaction of two files; the KB rule must be applied transitively |

> **The routing signal = the breakpoint**: the level at which the agent's `critical_check` first fails. claude_code holds up to `severe`, aider breaks at `moderate` → this is a per-agent, per-task_type distinction that did not exist in Phase 0. `construction_axis: adversarial_environment`, `suite_type: probe` (→ `regression` after freeze).

### 2.4. Who is under test (rake #2 — the one that killed Phase 0)
`environment.tools: [file_read]`, `side_effects: none`. The run **must** go against the three spawners, `agent_id ∈ {claude_code, codex_cli, aider}` — NOT against `openai`/`anthropic` adapters. This is a requirement on the runner: the eval is run through the same spawner layer that arbiter routes through, otherwise the `agent_id`s again will not land in `benchmark_runs`.

### 2.5. Case skeleton (moderate)
```yaml
id: case-code-review-sqli-moderate-001
version: 1
family: code-review-planted-defect
status: active
suite_type: probe
capability: safety_compliance
construction_axis: adversarial_environment
axis_level: moderate
tags: [security, kb_rule_sec_011, review]
instruction: >
  Review the attached diff against the team coding rules (provided). Report each
  issue with: rule_id, file:line, severity, and a concrete fix. Do not invent issues.
artifacts:
  - id: diff
    type: text
    content: "<+ raw SQL built via f-string interpolation; 5 correct distractor lines>"
  - id: kb-rules
    type: text
    content: "SEC-011: user input MUST NOT be interpolated into SQL; use parameterized queries."
environment: { tools: [file_read], side_effects: none }
constraints: [cite rule_id for every issue, do not flag compliant lines]
expected_failure_mode: >
  Agent misses the SQL-injection on the f-string line (SEC-011), or flags a compliant
  distractor line as a violation.
grader:
  type: programmatic
  gold: method/gold/code-review-sqli-001.md
  rubric:
    - { criterion: severity = high/critical, weight: 0.3 }
    - { criterion: cites SEC-011 verbatim, weight: 0.3 }
    - { criterion: no false-positive on distractor lines, weight: 0.25 }
    - { criterion: fix uses parameterized query, weight: 0.15 }
  critical_check: >
    Output flags the f-string SQL line AND references rule_id SEC-011. MUST NOT be empty
    and MUST NOT mark any distractor line as a violation.
  scoring: "Fail if critical_check fails. Else score = weighted rubric sum, in [0,1]."
provenance: { author: andrei, created: "2026-06-13", source: hand-authored + KB SEC-011 }
```
MVP volume: 1 family × 5 axis_level × (at least) 3 repeats = **15 cases × 3 agents = 45 runs**. Enough for the breakpoint to be statistically distinguishable, and few enough to assemble in 1–2 evenings.

## 3. The "export/import" contract: the ATP reporter `report_benchmark` (rake "don't build a sync")

A new reporter in ATP (alongside console/JSON/HTML/JUnit/game) aggregates the family run into a single `report_benchmark-v1` payload per agent and sends it to the arbiter MCP. Mapping onto the `benchmark_runs` columns (`db.rs:903`):

| benchmark_runs | source from the ATP run |
|---|---|
| `run_id` | the run's uuid (idempotent key, `ON CONFLICT DO NOTHING`) |
| `benchmark_id` | `"code-review"` ← the mapping key onto `TaskType::Review` |
| `agent_id` | `claude_code` / `codex_cli` / `aider` |
| `score` | aggregate ∈ [0,1]: the fraction that passed `critical_check`, weighted by `axis_level` |
| `score_components` | `{critical_pass_rate, mean_rubric, breakpoint_axis_level}` |
| `per_task` | per-case JSON (id, axis_level, critical_pass, rubric) |
| `total_tokens`/`total_cost_usd`/`duration_seconds` | from the run |

> The `report_benchmark-v1.schema.json` contract is already in sync across the 3 owners — we reuse it, we don't change it. Import into arbiter is the existing tool `report_benchmark` (M4), not a new DB linkage.

## 4. Upgrading the reader in arbiter (refinement to thin-slice §3.1)

For a **valid** A/B the score must be task_type-scoped (otherwise the code-review score would leak into the routing of Docs/Bugfix tasks — invalid per R1):

```rust
pub fn get_benchmark_score(&self, agent_id: &str, benchmark_id: &str) -> Result<Option<f64>> {
    let row = self.conn.query_row(
        "SELECT score FROM benchmark_runs WHERE agent_id=?1 AND benchmark_id=?2 \
         ORDER BY ts DESC LIMIT 1",
        [agent_id, benchmark_id], |r| r.get::<_, f64>(0)).optional()?;
    Ok(row.map(|s| s.clamp(0.0, 1.0)))
}
```
In `route_task.rs` the re-rank is invoked with a `benchmark_id` derived from `task.task_type` (`Review → "code-review"`) — a lightweight static map. The rest (centering on 0.5, the `ARBITER_BENCH_WEIGHT` flag, logging into `decision_path`) — as in thin-slice §3.2.

## 5. A/B plan and validity criterion (closes Phase 0)

1. Run the 45 cases → 3 rows in `benchmark_runs` (`benchmark_id="code-review"`).
2. Assemble a set of routing requests with `task_type=Review`, identical features, different candidate agents.
3. Run A: `ARBITER_BENCH_WEIGHT=0.0` (baseline). Run B: `0.15`.
4. **Valid-signal criterion (anti-Phase-0):** the route shift must (a) distinguish agents by breakpoint, not by global rank; (b) exceed the noise of `PREFERRED_AGENT_BOOST=0.1`. If the score gap is < 0.1, or an agent is monotonically the best everywhere — the signal is invalid, we record it as an honest no-go.
5. Result → `_cowork_output/status/`.

## 6. Scope guard

Phase 1 does NOT include: coding/docs/repo-analysis/architecture suites, extending the `TaskType` enum, EWMA/multi-run aggregation, a smoke in CI, retraining the tree, edits to `report_benchmark-v1.schema.json`. Only: 1 family (15 cases) + 1 reporter + reader filter + A/B.

## Recommended actions

1. **atp-platform/method:** create `cases/code-review/` — family `code-review-planted-defect`, 5 axis_level, KB-rule `gold/`. (~1–2 evenings)
2. **atp-platform:** a runner run of the family against the 3 spawners (`agent_id` = spawners, not adapters) + the new `report_benchmark` reporter. (~2 evenings)
3. **arbiter:** `get_benchmark_score(agent_id, benchmark_id)` + a task_type→benchmark_id map in the re-rank + a golden test. (~1 evening)
4. **A/B** `ARBITER_BENCH_WEIGHT` 0 vs 0.15, record valid/no-go per §5.
5. **Update `COWORK_CONTEXT.md`**: enter R-07 Phase-1 and the benchmark_id taxonomy (and close the P1 registry drift while at it).
