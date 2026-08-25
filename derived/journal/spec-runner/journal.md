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

## 2026-08-05 22:30 — change: battle round 3 (#96/#97) → stacked PRs #98/#99

- Two S2-round-3 findings implemented same day they were filed. #96: harness-written
  spec/.gitignore (the #62 fix) was swept into the first subtask's auto-commit and
  tripped maestro's ex-post scope gate (maestro#122, M-03); stage_all_except_runtime
  now excludes it when not tracked in HEAD. #97: explicit no-op completion marker
  (F-20, maestro#123) — new attempts.no_op column, additive "no_op": true in
  --json-result (emitted only when true; non-breaking per state-schema.md policy),
  [no-op] tag in status; new golden json-result-single-noop.json for Maestro.
- Investigation fact: F-20's "ledger not-done" did NOT reproduce — the state DB
  records no-op tasks as success even in the maestro-worktree scenario (checkout
  master fails, task branches stack); the 4/5 display was maestro's missing final
  poll. Commented on maestro#122/#123 with both resolutions.
- PR #99 is stacked on #98 (merge #98 first). After both: release v2.16.0 (minor).
- Links: spec-runner/src/spec_runner/git_ops.py:45, spec-runner/src/spec_runner/hooks.py:193,
  https://github.com/andrei-shtanakov/spec-runner/pull/98,
  https://github.com/andrei-shtanakov/spec-runner/pull/99

## 2026-08-05 23:55 — result: v2.16.0 released (battle round 3 shipped same day)

- PRs #98/#99 merged by owner; stacked #99 needed a rebase --onto after #98's
  squash-merge (stacked-PR + squash pattern). Release PR #100 → merge 8f3c6d2 →
  tag v2.16.0 → publish.yml success → PyPI 2.16.0 live → GitHub Release;
  release-tag-guard green. Issues #96/#97 auto-closed.
- Maestro can drop the per-workstream spec/.gitignore scope workaround after
  pinning spec-runner >= 2.16 (noted on maestro#122).
- Links: https://github.com/andrei-shtanakov/spec-runner/releases/tag/v2.16.0,
  https://github.com/andrei-shtanakov/spec-runner/pull/100

## 2026-08-06 08:20 — change: battle round 4 (#101–#104) → stacked PRs #105/#106/#107

- Four findings from run d4d33ad0 (kapelle TASK-007, on v2.16.0), three implemented
  same day as a 3-PR stack: #105 commit provenance (exec work committed under the
  task label BEFORE review — the whole feature used to land in the "code review
  fixes" commit), #106 execution-summary delta (cumulative executor_meta counters
  were reported as this run's result: completed=2 on a single-task run), #107
  pr_opened notification event (human-merge gate no longer depends on a watched
  terminal; dispatcher can consume the webhook).
- #102 (Copilot review-bot loop inside the tool) deliberately NOT implemented:
  spec-runner post-PR stage vs maestro hook is an owner decision (same fork as
  ex-post approver_cmd); trade-off analysis posted on the issue, TODO entry added.
- Links: https://github.com/andrei-shtanakov/spec-runner/pull/105 …/106 …/107,
  spec-runner/src/spec_runner/hooks.py:193, spec-runner/src/spec_runner/notifications.py

## 2026-08-06 09:40 — result: v2.17.0 released (battle round 4: 3/4 shipped same day)

- Stack #105/#106/#107 merged (auto-retarget worked, no manual rebases), release PR
  #108 → tag v2.17.0 → publish.yml success → PyPI 2.17.0 → GitHub Release; issues
  #101/#103/#104 closed. Notification surface gains pr_opened; Maestro interop
  contract untouched.
- Only open item: #102 (review-bot loop) — ownership decision pending
  (spec-runner post-PR stage vs maestro hook); trade-off analysis on the issue.
- Links: https://github.com/andrei-shtanakov/spec-runner/releases/tag/v2.17.0

## 2026-08-06 10:30 — decision: #102 review-bot loop → `spec-runner review-pr` (owner)

- Owner decided: the Copilot-comment loop lives in spec-runner as a separate
  resumable command `spec-runner review-pr` + optional post-PR stage; Maestro later
  invokes the same command via a thin hook. Approval policy stays in maestro
  approver_cmd (maestro#137) — approval never mixes with mutation. Design doc with
  state machine, normative constraints and M1→M3 phasing: PR #109
  (docs/superpowers/specs/2026-08-06-review-pr-loop-design.md).
- Links: https://github.com/andrei-shtanakov/spec-runner/issues/102#issuecomment-5200985431,
  https://github.com/andrei-shtanakov/spec-runner/pull/109

## 2026-08-06 12:30 — result: v2.18.0 released — review-pr M1 shipped

- Phase M1 of the #102 review-bot loop implemented and released same day as the
  design decision: `spec-runner review-pr` (collect from allowed bots → verify with
  fail-closed verdicts → durable cursor in pr_review_comments → text/--json report,
  exit contract 0/1/2). Copilot review caught a real stranding bug (--no-verify
  comments were never verified later) — fixed before merge.
- Remaining on #102: M2 (fix+reply), M3 (post-PR stage + maestro hook contract).
- Links: https://github.com/andrei-shtanakov/spec-runner/releases/tag/v2.18.0,
  https://github.com/andrei-shtanakov/spec-runner/pull/110

## 2026-08-06 14:30 — result: v2.19.0 released — review-pr M2 (fix + reply)

- The #102 loop now closes end-to-end: verify → TDD fix (per-comment commits with
  Review-Comment-Id trailers) → gates (red gate reverts) → single push → thread
  replies (fix SHA / refutation evidence; uncertain never auto-answered), under
  rounds/comments/diff/cost/wall limits with fail-closed dirty-tree/head-mismatch/
  force-push/push-failure handling. Same-day: M1 released in 2.18.0 (morning),
  M2 in 2.19.0 (afternoon).
- Remaining on #102: M3 — optional post-PR stage + maestro hook contract doc.
- Links: https://github.com/andrei-shtanakov/spec-runner/releases/tag/v2.19.0,
  https://github.com/andrei-shtanakov/spec-runner/pull/112

## 2026-08-06 16:00 — result: v2.20.0 released — #102 closed, review-pr complete

- M3 shipped: optional post-PR stage (off|verify|full, default off; crashed-loop
  leftovers stashed, never stranded) + documented external caller contract
  (0→PR_REVIEWED, 2→NEEDS_REVIEW, 1=infra failure) for maestro's future
  post_pr_command hook. Issue #102 closed by the merge.
- The whole line ran in one day: owner decision → design doc (#109) → M1
  (#110, v2.18.0) → M2 (#112, v2.19.0) → M3 (#114, v2.20.0). Repo: zero open
  issues. Maestro-side hook is now unblocked against a stable contract.
- Links: https://github.com/andrei-shtanakov/spec-runner/releases/tag/v2.20.0,
  spec-runner/docs/superpowers/specs/2026-08-06-review-pr-loop-design.md

## 2026-08-06 17:30 — result: v2.21.0 released — review-pr --json purity (inbox #116)

- Inbox request from maestro's accepted post-pr-command item: with --json, stdout
  must be exactly one JSON document. It was not — limit stops and fail-closed paths
  printed to stdout, and exit 1 emitted no JSON at all. Fixed: diagnostics to stderr,
  one document on every exit path, additive `exit_code` in the payload. Acceptance
  verified live on the real gh transport, not mocks.
- Maestro's post-pr-command is now unblocked; its form is `maestro review-pr` —
  advisory post-delivery cleanup with its own audit/read-model, NOT a lifecycle gate
  and NOT the synchronous hook our design doc sketches (owner correction). Rewriting
  that doc section after maestro#147 merges is offered but not yet approved.
- Links: https://github.com/andrei-shtanakov/spec-runner/releases/tag/v2.21.0,
  https://github.com/andrei-shtanakov/spec-runner/pull/117

## 2026-08-07 — decision: our docs state only our contract (PR #119, merged)

- The review-pr design doc had restated a Maestro-side lifecycle
  (PR_CREATED → post_pr_command → PR_REVIEWED/NEEDS_REVIEW) that was never
  their accepted shape; it went stale within a day and was read back as fact.
  Fixed by removing the class of drift, not the snapshot: the contract section
  now states only spec-runner's promises (invocation, exit 0/1/2 with 1 =
  infrastructure/protocol failure, one-JSON-document stdout, stderr
  diagnostics, idempotent resume, mutating-mode preconditions) and points at
  maestro#147 / todo://maestro/post-pr-command. Also recorded why this is not
  a vendored contract yet, and who would own the schema if it became one.
- Boundary rule for the ecosystem: the producing repo fixes its external
  contract, the consumer fixes consumption, the link is a pointer not a copy.
  Historical release notes are not retro-edited; clarifications land in the
  next release's notes.
- Note: PR #119's red checks were a GitHub Actions outage artifact (jobs
  cancelled, zero failed steps), not a code failure — re-run after the
  incident cleared, all seven green.
- Links: https://github.com/andrei-shtanakov/spec-runner/pull/119

## 2026-08-07 — status: stale TODO parent for #102 closed (PR #120)

- The #102 parent checkbox and the round-4 section header still claimed open
  work days after M1–M3 shipped; only child items were current. Flipped the
  checkbox (first-line prose untouched — it is Robin's identity key, tags
  excluded per robin-runtime#27) and corrected the header to 4/4 with split
  provenance. Verified with the canonical `make plan-check`: spec-runner
  8/9 → 8/8 open items with @owner, the phantom item gone.
- Open, not addressed: devtools' strict @owner grammar wants
  github:<handle>; every `@owner:andrei` in this TODO is outside it
  (reported, never failing) — a file-wide rename is a separate decision.
- Links: https://github.com/andrei-shtanakov/spec-runner/pull/120
