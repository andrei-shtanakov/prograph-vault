---
title: spec-runner — activity journal
type: journal
source: kb-save
project: spec-runner
updated: 2026-07-14
---

# spec-runner — activity journal

> Append-only log of significant project actions (written by the kb-save skill).
> Not authoritative and not regenerable. Curation/archival by kb-curator.

## 2026-07-12 20:33 — change: H-1/H-2 governed-run fixes shipped as PR #36

- H-1: run exits 1 on pre-run validation failure (was bare return -> rc=0;
  orchestrators read that as success — the empty-run bug the gates caught live).
- H-2: plan --full validates its own tasks.md with the runner's parse_tasks
  right after generation (zero parsed tasks -> exit 1, file kept); the
  plan->run format contract is self-enforced.
- 3 execution tests adapted (relied on silent return-0); suite 988 passed.
- Links: https://github.com/andrei-shtanakov/spec-runner/pull/36,
  vault authored/notes/2026-07-12-governed-run-findings.md

## 2026-07-13 11:15 — change: interactive `plan` edit action persists the draft (#38, #39)

- Bug found live in dispatcher: choosing `edit` at the `[y/N/edit]` prompt of
  interactive `spec-runner plan` printed "Edit tasks.md manually" but wrote
  nothing — with no pre-existing tasks.md the generated proposal was lost with
  the scrollback (worse than answering N: generation cost silently discarded).
- Fix (#38, merged): `[y/N/edit]` handling extracted into
  `cli_plan.py:apply_plan_confirmation()`; both `y` and `edit` append the
  proposal to tasks.md (creating file + parent dir), `edit` then opens $EDITOR
  on it — matching the gated flow, which already writes DRAFT before editing.
  4 regression tests in tests/test_plan_confirm.py.
- Follow-up (#39, merged): Copilot review caught the new tests writing
  spec/.executor-progress.txt into pytest's CWD via log_progress(); fixed with
  an autouse fixture patching spec_runner.runner.PROGRESS_FILE to tmp_path.
- Links: https://github.com/andrei-shtanakov/spec-runner/pull/38,
  https://github.com/andrei-shtanakov/spec-runner/pull/39

## 2026-07-14 12:24 — result: OpenSpec-inspired roadmap fully shipped (M0–M4, PRs #40–#46)

- Studied the OpenSpec repo (study-only, workspace root) on 2026-07-13 and
  ported its four borrow-worthy patterns into spec-runner over five merged
  PRs (2026-07-13..14), each with a GitHub Copilot review round addressed
  pre-merge:
  - **M0** (#40 + hardening #42): opt-in `spec_context`/`spec_rules` config
    keys inject `<context>`/`<rules>` blocks into plan --full/--gated
    generation prompts; validate errors on >50KB context / wrong types.
  - **M1** (#43): tolerant id-keyed requirements parser (`requirements.py`) —
    rejected OpenSpec's rigid Requirement/Scenario grammar against real data;
    a requirement block's exact `raw` is the merge unit.
  - **M4** (#44, engine-only): stage profiles are a DAG (`requires:` edges,
    cycle detection, `stage_readiness()`); sibling stages no longer wrongly
    stale-cascaded; lite byte-identical (exhaustive equivalence test).
  - **M2** (#45): change-as-folder — `spec/changes/<id>/` self-rooted spec dir
    via `--change`; per-change state-db ⇒ per-change run lock ⇒ parallel
    changes. **No contract change** (owner decision): db location is config
    (paths.state precedent); `change_id` in --json-result deferred (would break
    additionalProperties: false). Design doc:
    spec-runner/docs/plans/2026-07-13-m2-change-folder-design.md.
  - **M3** (#46): delta specs (`changes/<id>/specs/requirements.md`,
    ADDED/MODIFIED/REMOVED/RENAMED, id-keyed identity) + deterministic
    all-or-nothing merge into flat spec/requirements.md on `change archive`
    (atomic write, --dry-run plan, re-apply → conflict, `validate --change`
    fail-fast).
- 1129 tests pass; Maestro interop contract (state-db schema, --json-result)
  untouched throughout. M5 (OpenSpec tasks.md bridge) intentionally deferred
  until a real use case appears.
- Links: spec-runner/docs/plans/2026-07-13-openspec-inspired-roadmap.md,
  https://github.com/andrei-shtanakov/spec-runner/pull/40 …/42 …/43 …/44 …/45 …/46
