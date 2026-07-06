---
title: "Spec reviews: deployer×2 + Maestro + arbiter + dispatcher + proctor-a (6 specs)"
type: note
status: archived
owner: Andrei
updated: 2026-07-05
archived: 2026-07-06
reason: historical status snapshot (bulk-archived on graduation from _cowork_output)
---

# Spec reviews: deployer×2 + Maestro + arbiter + dispatcher + proctor-a (6 specs)

**Date:** 2026-07-05
**Author:** Cowork TPM/architect review
**Scope:** six specs dated 2026-07-05 (one brainstorming session per repo; deployer — two: verify-timeouts and cli-hardening)
**Mode:** read-only analysis of the repositories; all anchor files checked against the code.

## TL;DR

1. **All four specs are architecturally healthy, no design blockers.** The remarks are text clarifications, protection against drift, and one class of concurrency risk, not rewrites. Authoring quality is aligned across the repos.
2. **A cross-cutting pattern in all four is correct and deliberate:** fail-loud instead of a silent default, a verifiable invariant instead of "the prompt/thread obeyed". This continues the principle from the 2026-07-04 review.
3. **The two most serious individual risks are independent and both "silent":**
   - **arbiter:** `PRICING`/enum growth — growing an enum value in the SSOT breaks **all** parsing in a non-updated loader (forward-compat holds for fields but not for enum values).
   - **dispatcher:** `_SnapshotCache` without a lock moves into a `thread=True` worker — a race on the shared cache.
4. **A cross-cutting weakness in the wording — "parity/modeled on" without an anchor list:** deployer's "matching existing `--max-iterations` pattern" (the pattern is absent in `verify`) and dispatcher's "full parity" (the web-UI features are not enumerated). One class: the declared reference is not pinned.
5. **A shared cost motif:** Maestro (opencode cost=0 = "free" for the router) and arbiter (catalog-loader as the first executed item of ADR-003b) move the same axis — honest cost in the routing loop [[ecosystem-arbiter-loop-status]]. Worth keeping them coordinated.

---

## Spec matrix

| Spec | Status | Foundation check | Design verdict | Key risk |
|---|---|---|---|---|
| `deployer/docs/superpowers/specs/2026-07-05-verify-timeouts-design.md` | approved | anchors ✓ | Solid, correctly scoped | The 600s default does not fix the motivating case (unblock, not fix) |
| `Maestro/docs/superpowers/specs/2026-07-05-opencode-wiring-design.md` | approved | anchors ✓ (wiring complete) | Strong, integration-complete | cost=0 = "infinitely cheap" for the router |
| `arbiter/docs/2026-07-05-catalog-loader-design.md` | Draft → **edit incorporated (2026-07-05)** | anchors ✓ | Strong, variant A (pure core); all 5 remarks closed | (closed) enum growth → degrade-with-warning V7; the fixture reads the vendor directly |
| `dispatcher/docs/superpowers/specs/2026-07-05-dispatcher-tui-design.md` | approved | anchors ✓ | Strong, Approach A (no dup) | Unlocked cache in a `thread=True` worker |
| `proctor-a/docs/superpowers/specs/2026-07-05-task-router-design.md` | Draft | anchors ✓ (the arch plan is correct) | Strong, pure queue (clock injected) | `admit()` race via publish-await; lifecycle tick-loop |
| `deployer/docs/superpowers/specs/2026-07-05-cli-hardening-design.md` | approved | anchors ✓ (on cli.py after PR #3) | Solid, evidence-driven | report overwrite vs the "lost research data" motivation |

---

## 1. deployer — verify timeout forwarding

**What it does:** threads `--build-timeout`/`--health-timeout` through CLI → `verify()` → `verify_docker()` as kwargs; defaults in module constants. Motivation: `locallogai-backend` (llama-cpp-python from source) does not fit in 600s.

**Anchor check:** `verify_docker` already has defaults 600/30 (`verify.py:462-463`); `verify()` does not forward them (`verify.py:488`, call `501-503`); two call sites in `author.py:69` (main) + `:72` (env-retry); the validation pattern `--max-iterations<1→exit 2` is **only** in `_cmd_author` (`cli.py:59-60`), not in `verify`.

| # | Remark | Importance | Essence |
|---|---|---|---|
| 1 | `verify` validation — not "modeled on", but from scratch | Medium | `_cmd_verify` (`cli.py:38`) has no validation; the `--build-timeout 0` test should cover **both** subcommands. |
| 2 | The default does not solve the target task | Medium | 600s is unchanged → `locallogai-backend` is fixed only by hand. Record a known limitation + the link to out-of-scope per-target persistence. |
| 3 | `--health-timeout` is a no-op for non-service | Low | `_run_healthcheck` only when `target.service is not None` (`verify.py:481`). A line in `help=`. |
| 4 | No upper bound | Low | Only `<1` is validated; for a research bench that's ok, mention the deliberateness. |

---

## 2. Maestro — opencode spawner wiring

**What it does:** makes `opencode` a first-class agent type (enum, entry-point, cli-dict, schema-regen), a token parser from JSONL, D2 routing `opencode@<model>`.

**Anchor check:** `opencode.py` exists (Jul 3), no wiring/tests; `AUTO` is the last sentinel (`models.py:79`); the top-level exports only `ClaudeCodeSpawner` (`__init__.py:64`); the parsers map has no opencode (`cost_tracker.py:143-146`); the D2 test `test_scheduler.py:1694` uses `"opencode"` as an example of "harness outside the enum" — registration **falsifies the premise**; fail-loud `HarnessModelUnresolved` is reused. There are no hidden exhaustive matches on `AgentType` beyond those listed.

| # | Remark | Importance | Essence |
|---|---|---|---|
| 1 | cost=0 = "free" for the router | **High** | `PRICING["opencode"]=(0,0)` while tokens actually parse. In cost ranking opencode always wins the tiebreaker. Invariant: exclude from cost comparison (0=unknown, not free). Check the read sites of `PRICING` in arbiter/benchmark. |
| 2 | per-step vs cumulative not proven | **High** | Summing `step_finish` is correct only if usage is per-step (Vercel AI SDK). The multi-step fixture is from a **real** run; verify against the docs. |
| 3 | `cache_read`/`cache_write` discarded | Medium | In the sample `cache_read:21415 > input:22443`. For tokens-only that's ok; a cost follow-up should not bill `cache_read` as input at full rate. |
| 4 | silent skip of malformed "blinds" | Medium | A format change → silent zeros. debug-obs on "non-empty log → 0 step_finish". |
| 5 | dual-registration cli-dict + entry-points | Low | Two sources of "which spawners exist"; the spec edits both — a latent divergence risk. |
| 6 | naming `opencode` vs `codex_cli` | Low | The enum values are inconsistent; fix that the bare name is deliberate. |

---

## 3. arbiter — Rust catalog-loader (ADR-ECO-003b)

> **Update 2026-07-05:** the spec was corrected the same day — all 5 remarks below are closed (enum growth → `Other(String)` degrade-with-warning + rule V7; the happy-path test reads the vendor `config/agents-catalog.toml` directly; the CLI dispatch is fixed as hand-rolled, without clap; "V2+V3 = Check 5" clarified; the toml action corrected). Residual — one forward-looking: the guarantee "`Other`-status = not active" holds only on the allowlist check `== Active` at the future consumer, not `!= Retired`; fix in §3.

**What it does:** a pure `arbiter_core::catalog` (path resolution + parsing + validation) + CLI `arbiter-cli catalog path|check|list`. The runtime arbiter-mcp is untouched.

**Anchor check:** the core/mcp/cli crates are in place; `toml` is **already** in `[workspace.dependencies]` (`Cargo.toml:19`), only `workspace=true` in `arbiter-core` is needed; the vendor copy `config/agents-catalog.toml` is **byte-for-byte identical** to the canon `atp-platform/method/agents-catalog.toml`; conformance Check 5 (`_cowork_output/devtools/check-agent-id-conformance.py:245`) = "missing **or** retired" (i.e. V2+V3, not only V3); `arbiter-cli` is **hand-rolled** (`std::env::args()`, one level; no clap).

| # | Remark | Importance | Essence |
|---|---|---|---|
| 1 | Enum growth breaks all parsing | **High** | A new `status`/`kind` value in the SSOT → `CatalogError` on the whole file. Forward-compat holds for fields, not for enums. Name it a breaking change with coordination or degrade-with-warning. |
| 2 | `valid.toml` = a 3rd copy | **High** | Derive the fixture from `config/agents-catalog.toml` (not a manual copy) + an equality test. Otherwise it contradicts §8 Risk #1. |
| 3 | The CLI dispatch is under-specified | Medium | hand-rolled one level vs a two-level `catalog path\|check\|list`. Fix it: extend the manual match or introduce clap (not in deps). |
| 4 | "mirror of Check 5" is imprecise | Low | Check 5 = V2(missing)+V3(retired); verify the "missing" severity. |
| 5 | "raise toml into workspace.deps" | Low | Already done; the action is `toml={workspace=true}` in `arbiter-core/Cargo.toml`. |

---

## 4. dispatcher — Stage 2 TUI (textual)

**What it does:** a textual TUI with web-dashboard parity; consumes `dispatcher.core` directly (Approach A: extracting snapshot collection into `core/service.py`).

**Anchor check:** `_SnapshotCache` (5s TTL, per-collector guard, undetected append) — all three are real (`server/app.py:24,44,77-88`); `recent_errors(events,days,now=None)`, `_ISO_PREFIX=19` (`app.py:29`); `get()->tuple[list[ProjectSnapshot],list[str]]` (`app.py:52`); CLI argparse subparsers (`cli.py:18`); the collectors are synchronous; `ContractStatus.in_sync: bool|None` (`models.py:61`); the web default `ERRORS_DAYS_DEFAULT=14` (index.html:98), API `days` default=`None` (the front owns "14").

| # | Remark | Importance | Essence |
|---|---|---|---|
| 1 | Unlocked cache in a `thread=True` worker | **High** | A race on `_data`/`_at` when auto-refresh(10s) and `r` intersect. `exclusive=True` on the worker or a lock in `SnapshotService`. The refactor changes the threading assumptions of single-threaded code. |
| 2 | "Full parity" is not anchored | Medium | The web-UI features are in `server/static/index.html`; enumerate them as a checklist/test (project/service selects, toggle, newest-first, columns). |
| 3 | The 10s interval vs 5s TTL | Low-medium | The regular cycle always misses the cache; the TTL only de-dups coincident refreshes — it does not relieve the 10s cycle. |
| 4 | "14" in three places | Low | `ERRORS_DAYS_DEFAULT` + TUI; extract into a core constant shared by web+TUI. |
| 5 | `discover()` outside the per-collector guard | Low | Its failure reaches `get()` and is caught only by the layer-3 toast (does not produce a layer-2 warning snapshot). |
| 6 | `textual` as a regular dependency | Low | Pulled even for `serve`-only; the alternative is an extra `[tui]`. |

---

## 5. proctor-a — TaskRouter (M4, Phase 2)

**What it does:** an admission layer before workflow execution — 4 invariants (`concurrency_limit`, `agent_available`, `scope_isolation`, `branch_not_locked`), a pending queue with TTL, a seam for capability-scoring (Phase 3). A new package `src/proctor/router/`. Not to be confused with the `core/router.py` Router (LABS-65): that one decides *what* to launch, TaskRouter — *whether it can now*.

**Anchor check:** the M4 plan (`docs/plans/2026-03-04-proctor-architecture-design.md:184-200`) describes these invariants + reject verbatim; `core/router.py` Router→WorkflowSpec, emits `routing.unmatched`/`binding_failed` (`router.py:56,96,130`); bootstrap integration in `_handle_trigger_event` (`bootstrap.py:141`, execute inline-await `:183`); `Task` statuses + `StateManager.save_task` (`models.py:15-19`, `state.py:126`); `scope`/`branch` — new fields (not in `spec.py:62-79`); the bus provides concurrency (`transport/local.py:354 create_task`).

| # | Remark | Importance | Essence |
|---|---|---|---|
| 1 | Atomicity of `admit()` via publish-await | **Medium-high** | The bus = concurrent tasks → two admits race. Explicitly: mutate the running-set **before the first `await`**, publish `routing.*` — after the reservation commits. Test: two simultaneous admits at `max_concurrency=1`. |
| 2 | Tick-loop lifecycle not described | **Medium** | `Application` has no background loops (`bootstrap.py` without task_group/cancel). Specify the start in `start()`, cancellation in `stop()`/drain. Built from scratch. |
| 3 | A third copy of the glob heuristic | Medium-low | proctor already has `_is_strictly_broader` (`config.py:309`), Maestro — `_patterns_overlap`; `invariants.py` will add a third. The semantics differ (subsumption vs overlap), but the family is the same — consolidate into a shared `globs` helper. |
| 4 | `agent_available` — not a live query to AgentRuntime | Low | `AgentRuntime` (`runtime.py:48`) has no slots; the v1 profile is static. Fix: until Phase 3 the invariant does not reflect the real runtime load. |
| 5 | `Task.deadline` already exists | Low | `models.py:100`; the queue keeps its own TTL-deadline. Two different meanings (admit-TTL vs run-deadline) — keep separate, note the name collision. |

Strengths: `PendingQueue` is pure, the clock is injected (the same pattern as `resolve_path` in the arbiter spec); scope-overlap **deliberately** prefers a false-positive over a false-negative (right for isolation, better than the Maestro spec); `queue_ttl_seconds:0` preserves the reject semantics of the arch-doc through config; correct in separating the two routers and the `routing.*` namespace.

---

## 6. deployer — CLI hardening (builds on verify-timeouts PR #3)

**What it does:** two gaps from the dogfood run against `locallogai-backend` — (1) `verify` lost failure details (`_print_report` printed only the first line, `_cmd_verify` persisted nothing); (2) argument errors surfaced as tracebacks (`_load_target` threw bare exceptions, `_cmd_author` called it before validations). Plus an exit-code taxonomy 2/1/0.

**Anchor check (on `cli.py` after PR #3):** `_print_report` only the first line (`cli.py:60`); `_cmd_verify` without persist (`:66-87`); `_load_target` bare exceptions (`:26-29`); `_cmd_author` `_load_target` before validations (`:92` before `:93,:96`); `is_dir()` is not checked anywhere; `mkdir(exist_ok=True)` without `parents` (`:113`); `VerificationReport`/`CheckResult` + `model_dump/validate_json` (`models.py:70-113`).

| # | Remark | Importance | Essence |
|---|---|---|---|
| 1 | Overwrite vs "lost research data" | Medium | `verify-report.json` is overwritten → history between runs is lost, and that is the motivation. Fix "latest-run only, history out-of-scope". |
| 2 | `_load_target` diverges from the file's idiom | Medium-low | Chosen "returns `None` + prints itself"; nearby there is already `_timeout_error() -> str\|None` (returns a message, the caller prints). Two idioms in one CLI — consolidate to one. |
| 3 | No test on the validation order | Low-medium | The essence of Part 2 is reordering. A test "non-dir + missing `--target` → the dir error wins" pins the order. |
| 4 | 6-space indent does not align | Low | The prefix `[{icon:>4}] ` = 7 characters; the FAILED tail needs 7 spaces, not 6 (off-by-one). |

Strengths: fully evidence-driven; an exit-code taxonomy with a justified rejection (missing `--target` ≠ exit 1); `is_dir()` correctly **before** the Dockerfile check; incidentally the `_print_report` fix also improves the `author` output (`cli.py:111`).

---

## Recommended actions

**deployer** (`deployer/`)
- **[into the spec text]** "matching the existing `--max-iterations` pattern" → "add validation to both subcommands; `verify` has none today". *(#1)*
- **[into the spec text]** Known-limitation: the 600s default is unchanged → `locallogai-backend` is unblock-through-flag, not fix. *(#2)*
- **[tests]** `--build-timeout 0 → exit 2` for `verify` **and** `author`. *(#1)*
- **[minor]** `help=` for `--health-timeout`: "ignored for non-service targets". *(#3)*

**deployer — CLI hardening** (`deployer/`)
- **[into the spec text]** `verify-report.json` — latest run only; cross-run history out-of-scope. *(cli-hardening #1)*
- **[implementation]** Bring `_load_target` to the `_timeout_error` idiom (return a message, print in one place). *(cli-hardening #2)*
- **[tests]** Validation order: non-dir + missing `--target` → dir error. *(cli-hardening #3)*
- **[implementation]** 7 spaces to align the FAILED tail. *(cli-hardening #4)*

**Maestro** (`Maestro/`)
- **[before merge]** Invariant: while there is no cost-from-log, opencode is excluded from cost ranking (0≠cheapest); check the `PRICING` reads in arbiter/benchmark. *(#1)*
- **[tests, mandatory]** A multi-step fixture from a live `opencode run`; assert `step_finish` per-step. *(#2)*
- **[comment]** cache tokens and `part.cost` are deliberately omitted; the cost follow-up does not bill `cache_read` as input. *(#3)*
- **[verifiable]** debug-obs on "the log is non-empty, but 0 `step_finish`". *(#4)*

**arbiter** (`arbiter/`)
- **[into the spec text, before implementation]** §3: forward-compat for fields, **not** for enums; enum growth = coordinated breaking change (or degrade-with-warning). *(#1)*
- **[into §7]** `valid.toml` derives from `config/agents-catalog.toml` + an equality test. *(#2)*
- **[into §6]** Fix the dispatch mechanics (hand-rolled vs clap; clap not in deps). *(#3)*
- **[into §4]** Clarify Check 5 = V2+V3; verify the "missing" severity. *(#4)*

**dispatcher** (`dispatcher/`)
- **[into the spec text, before implementation]** §3: worker `exclusive=True` or a lock in `SnapshotService`; name the threading model. *(#1)*
- **[into §Testing]** A parity checklist/test against `server/static/index.html`. *(#2)*
- **[into §1]** Extract `ERRORS_DAYS_DEFAULT=14` into a core constant (web+TUI). *(#4)*
- **[clarification §4]** A discover-level failure holds only on layer-3. *(#5)*

**proctor-a** (`proctor-a/`)
- **[into §Error handling, before implementation]** `admit()` reserves a slot synchronously **before** any `await`; publish `routing.*` — after. A test on the race of two admits. *(#1)*
- **[into §Components/bootstrap]** The tick-loop lifecycle: start in `start()`, cancellation in `stop()`/drain. *(#2)*
- **[into §invariants]** `scope_isolation` via a shared glob helper (extend the `config.py` family), not a third copy. *(#3)*
- **[into §Limitations]** `agent_available` until Phase 3 — bookkeeping, not AgentRuntime load. *(#4)*

**Ecosystem (cross-project)**
- **Cost honesty as a shared invariant:** Maestro (opencode cost=0) and arbiter (retired/deprecated in the catalog-loader) move the same routing loop. Lock the principle "0/None = unknown, not free/ok" on the consumer side (arbiter/benchmark ranking), not only on the source.
- **"A declared reference must be pinned"** as a cross-cutting spec-review rule: deployer's "existing pattern" and dispatcher's "full parity" — both are cured by an anchor list/test, not by prose.
- **Anti-duplication keeps surfacing** ([[project-repo-topology-decision]]): dispatcher rejected duplicating the collect-loop (Approach A), arbiter risks a 3rd copy of the catalog, Maestro carries dual-registration, proctor-a — a third copy of the glob-overlap heuristic. One class — keep the SSOT + derivation, not copies.
- **Glob-overlap as a shared primitive:** three independent implementations (`proctor-a/config.py` subsumption, `Maestro/decomposer.py` `_patterns_overlap`, the new `proctor-a/router/invariants.py`). A candidate for a shared cleaned-up helper — the same class as the scope-linter from [[reference-scope-linter-oss]].
