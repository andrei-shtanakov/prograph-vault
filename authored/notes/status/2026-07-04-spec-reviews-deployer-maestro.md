---
title: "Spec reviews: deployer (MVP → facts-v2) + maestro (init/validate)"
type: note
status: archived
owner: Andrei
updated: 2026-07-04
archived: 2026-07-06
reason: historical status snapshot (bulk-archived on graduation from _cowork_output)
---

# Spec reviews: deployer (MVP → facts-v2) + maestro (init/validate)

**Date:** 2026-07-04
**Author:** Cowork TPM/architect review
**Scope:** three approved specs, pre/post-implementation
**Mode:** read-only analysis of the repositories; anchor files checked against the code.

## TL;DR

1. **All three specs are architecturally healthy and correctly scoped.** Not a single design blocker; the remarks are clarifications and protection against future drift, not rewrites.
2. **Ecosystem coherence confirmed:** three of my earlier remarks on the deployer MVP are already implemented in the code (`--network=none` sandbox, `no_progress` early-stop, `environment_failure` classification) — the feedback loop closed.
3. **The most serious risk is the curated `KNOWN_SYSTEM_DEPS` table in deployer facts-v2:** it will go stale and lie confidently (many packages already ship wheels), and the extra apt layer `verify` won't catch it (build passes, the image is bloated).
4. **The most important architectural remark on maestro:** `dag-cycle` is declared "modeled on `TaskDAG._detect_cycles`" = a copy of the algorithm. A shared function needs to be **extracted**, otherwise a duplicate is laid into the foundation (the pain class from [[project-repo-topology-decision]]: `obs.py` in 3 places, `arbiter_client`).
5. **A cross-cutting pattern recommendation:** move rules that are deterministic from facts from prompt-only to verifiable invariants (L1 checks in deployer; preflight checks in maestro) — cheaper and more reliable than "the model/prompt obeyed".

---

## Spec matrix

| Spec | Status | Foundation check | Design verdict | Blockers |
|---|---|---|---|---|
| `deployer/docs/superpowers/specs/2026-07-04-deployer-mvp-design.md` | approved, merged (PR #1) | code in place | Solid, correctly scoped | None (remarks to backlog) |
| `deployer/docs/superpowers/specs/2026-07-04-facts-v2-design.md` | approved, pre-impl | foundation is real (see below) | Strong, evidence-driven | None; 2 "before implementation" items |
| `maestro/docs/superpowers/specs/2026-07-04-init-validate-design.md` | approved, pre-impl | all anchors checked ✓ | Strong, verify-first | 1 (shared cycle detection) |

---

## 1. deployer MVP — review (brief, for context)

Design: authoring ≠ execution, a deterministic pipeline with an LLM step inside, a two-level verify (L1 static → L2 `docker build`), `AuthoringRun` as a research artifact. Assessment — the right choice for a research bench.

Earlier remarks and their fate (checked in the code):

| Remark (MVP review) | Status in code |
|---|---|
| Sandbox L2 (`docker build` executes LLM-authored `RUN`) | **Implemented** — `--network=none` in `src/deployer/verify.py:289` |
| Separate authoring failures from environment failures in metrics | **Implemented** — `environment_failures` property `src/deployer/models.py:84`; classification by network markers `verify.py:206` |
| Early-stop on lack of progress | **Implemented** — `StopReason` includes `no_progress` `models.py:114`; retry-budget `author.py:68` |
| Success = build passes is weak (build ≠ working image) | Partial: `environment`/run-healthcheck exists; image quality metric — see facts-v2 #3 below |
| `analyze_project` covers the easy part, system deps deferred | **Addressed by facts-v2** |

Open MVP backlog: run+healthcheck as a mandatory success gate for the fixtures; structured-output vs plain-text for the Dockerfile itself.

---

## 2. deployer facts-v2 — review

**Foundation checked (real):** `ProjectFacts.dependencies` `models.py:34`; `DeployTarget` `models.py:16`; `AuthoringRun`/`stopped_reason` `models.py:121,130`; `environment_failures` `models.py:84`; sandbox `verify.py:289`. `hints.py` and the `pip_service`/`sysdep_service` fixtures are new, as declared (right now only `tests/fixtures/hello_service`).

**Strengths:** evidence-driven (dogfood + evaluation of lab_aist, not hypotheses); a three-layer model of system deps with explicit rejection of loop-only/intent-only and the reasons; epistemic honesty (hints ≠ facts, a separate prompt header "verify, trust build errors over hints") — preserves the invariant "the scanner does not guess"; shallow non-recursive parsing of requirements; two separate fixtures (a failure points at one feature); lxml instead of psycopg (no DB needed).

| # | Remark | Importance | Essence |
|---|---|---|---|
| 1 | The `KNOWN_SYSTEM_DEPS` table will go stale and lie | **High** | apt name drift (bookworm→trixie) + many packages already ship manylinux wheels (`psycopg2-binary`, `cryptography`, `lxml`, `numpy`, `pillow`) → the hint is false-positive. The extra apt layer `verify` won't catch: build passes, the image is bloated (net-negative). Keep in the table only packages **without** a wheel for the target platform; assign an owner/refresh process. |
| 2 | `-binary`/`-headless` variants | Medium | `psycopg2-binary` should not map to `libpq-dev`+`build-essential` — the whole point is a prebuilt wheel. Encode as empty build_packages, not "in the list = needs build-deps". |
| 3 | The hints value metric is one-sided | Medium | `hints_offered` + Dockerfile measure "reduced iterations", but on wheel-available projects hints add extra apt layers (bloat, not iterations). A second metric is needed — **image size** / "apt layer present, but the build proved it unnecessary", otherwise the research conclusion "hints help" is one-sided. |
| 4 | Hints only hit top-level deps | Medium | A system-dep package is often transitive (the `locallogai-backend` case, "no-wheel dependency"); with non-recursive parsing it stays invisible → goes into the repair loop. Acceptable, but record as a known limitation so the research does not overestimate coverage. |
| 5 | Deterministic rules — from prompt into L1 | Medium | uv-vs-pip and `--no-install-project` are deterministic from facts. "`package_manager=="pip"`, yet the Dockerfile has `uv sync`" — a ready static L1 check. Converting from prompt-hope to a verifiable invariant is more reliable + gives a signal in `AuthoringRun`. |
| 6 | The `requirements_files` type is murky | Low | Normalized names and `-r extra.txt` verbatim in one `list[str]`; `collect_hints` should skip entries on `-` (otherwise it looks up `-r extra.txt` in the table; harmless with `dict.get`, but dirty). |

---

## 3. maestro init/validate — review

**All anchors checked ✓:**

| Spec reference | Fact in code |
|---|---|
| "duplicate IDs / unknown deps / self-dep / ID format already enforced by pydantic" | **Correct** — `WorkstreamConfig` (id format, self-dep) `maestro/models.py:957`; `OrchestratorConfig.validate_unique_workstream_ids` + `validate_workstream_dependencies_exist` `models.py:1270+` |
| `TaskDAG._detect_cycles` | `maestro/dag.py:109` ✓ |
| `Decomposer.validate_non_overlap` / `_patterns_overlap` | `maestro/decomposer.py:400,427` ✓ |
| `_run_orchestrator`, `load_orchestrator_config` | `cli.py:890,898`; the loader is actually in `maestro/config.py:227` (not models.py — a clarification) |

**Strengths:** Approach A (a separate `preflight.py` + `ValidationReport`) instead of pydantic validators and a plugin linter — correct (warnings/FS have no place in clean models; plugins = YAGNI); offloading schema checks to the existing pydantic is legitimate; the `init` self-check via a round-trip of the loader catches template drift; the integration into `orchestrate` at the right seam, `orchestrator.py` is untouched; exit codes + `--strict` under CI.

| # | Remark | Importance | Essence |
|---|---|---|---|
| 1 | `dag-cycle` "modeled on" = a copy of the algorithm | **Blocker** | A second cycle detector next to `TaskDAG._detect_cycles` will diverge. Extract a pure `detect_cycles(nodes: dict[id, deps]) -> path\|None`, call from both. One algorithm, one test. (The duplication class from [[project-repo-topology-decision]].) |
| 2 | `scope-overlap` inherits the accuracy of `_patterns_overlap` | **High** | Headline feature; a correct glob overlap is hard (`a/**/*.py` vs `a/b/*.py`). As a warning the most dangerous is a false-negative — it will silently miss a merge conflict. Check what's inside `_patterns_overlap` (heuristic vs honest intersection); if it's a heuristic — strengthen it or lower expectations in the spec text. |
| 3 | `scope-no-match` — low signal | Medium | A warning, because a glob on a future file is legitimate → a typo and a valid future glob are indistinguishable, while the check's goal is to catch typos. Name it honestly: the check is about "likely empty scope", low value. |
| 4 | `init` self-check vs placeholders | Medium | The logic "the config always loads but fails on FS" hinges on placeholder `repo_url`/`repo_path` passing pydantic (including `validate_repo_path`). Cover with a `test_scaffold.py` test (non-git cwd). |
| 5 | Two styles of git access | Low | `init` pulls sync `subprocess.run` bypassing the async `GitManager` (justified), but isolate it inside `scaffold.py` so a second git path does not spread. |

---

## Recommended actions

**deployer** (`deployer/`)

- **[before facts-v2 implementation]** Audit `KNOWN_SYSTEM_DEPS` against current wheel availability; `-binary`/`-headless` → empty build_packages; fix an owner and a table update process. *(facts-v2 #1, #2)*
- **[before facts-v2 implementation]** Add a second image-quality metric to the research seam (size / extra apt layer), otherwise the conclusion "hints help" is one-sided. *(facts-v2 #3)*
- **[into the spec text]** Record a known limitation: hints see only top-level deps; transitive system-dep packages go into the repair loop. *(facts-v2 #4)*
- **[implementation, 2nd step]** Promote uv-vs-pip and `--no-install-project` from prompt-only to L1 checks. *(facts-v2 #5)*
- **[MVP backlog]** run+healthcheck as a mandatory success gate for the fixtures.

**maestro** (`maestro/`)

- **[MVP-blocking for init/validate]** Extract a shared `detect_cycles(...)`; `preflight.py` and `TaskDAG` (`dag.py:109`) call one function — not a copy. *(init/validate #1)*
- **[before selling scope-overlap as a key feature]** Check the accuracy of `_patterns_overlap` (`decomposer.py:427`); if it's a heuristic — strengthen the matcher or lower expectations in the spec. *(init/validate #2)*
- **[into the spec text]** Reformulate the value of `scope-no-match` (low signal). *(init/validate #3)*
- **[tests]** `test_scaffold.py` case: placeholders from a non-git cwd pass the pydantic schema. *(init/validate #4)*

**Ecosystem (cross-project)**

- The cross-cutting principle **"deterministic-from-data → verifiable invariant, not prompt/hope"**: deployer L1 checks for install-strategy + maestro preflight checks — the same bet. Worth locking in as a shared design principle of both projects.
- The Cowork↔repo knowledge bridge: idea/direction docs live in the `docs/` of the owner repo (`deployer/docs/idea-*.md`, `maestro/docs/idea-workstream-framework.md`), Cowork memory only indexes — otherwise Claude Code and the Cowork agent know different things.
