# Handoff → github-checker: content-PR path needs a new scoped propose-pr command

> **Context (2026-07-17):** building dispatcher's spec-runner config editor
> (`docs/superpowers/specs/2026-07-17-spec-runner-config-editor-design.md`,
> DESIGN-304) surfaced that its core assumption about `github-checker open-pr`
> is wrong. Found on dispatcher's final whole-branch review — dispatcher
> can't fix this itself (github-checker is a neighbor repo), fixing here.
> Revised same day after design review: recommendation changed from
> "extend open-pr" to "new command, scoped paths, temp worktree".

## TL;DR

`github_checker/actions.py::open_pr()` docstring: *"Never pushes — an
unpushed branch is an error, not a side effect."* It only runs `gh pr view`
then `gh pr create --fill` on whatever branch is currently checked out. It
does **no** `git checkout -b`, `git add`, `git commit`, or `git push`.
This is not a bug — it is a deliberately stated contract ("deliberately
tiny and safe" whitelist) that dispatcher's new content-PR action wrongly
relied on.

dispatcher's new content-PR action class (`core/spec_runner_config_actions.py`)
writes a file edit directly into the operator's real working tree, then
calls `github-checker open-pr <dir>` expecting it to turn that dirty tree
into a branch + commit + push + PR. That assumption is false for `open-pr`
as shipped (github-checker's whitelist is exactly two commands: `pull` and
`open-pr`; there is no `create-pr` command — that's the name of dispatcher's
API route, not a github-checker command). Net effect: the edit lands as an
uncommitted change in the operator's workspace (usually on whatever the
current/default branch is), `gh pr create` has no pushed head branch to PR
from, and the confirmed action reports failure — the feature's actual PR
step never happens.

## Why this wasn't caught earlier

Every dispatcher test that exercises this path fakes `github-checker` with a
stub script that prints a fixed `{"ok": true, ...}` JSON blob and does no
real git operations — so the write-then-invoke sequence "works" in tests
regardless of whether `open-pr` does real git plumbing. Only reading the
actual `github_checker/actions.py` source (done during dispatcher's final
review, not any single per-task review) surfaced the mismatch. Suggests a
github-checker integration test against a real temporary git repo (`gh` can
be faked; `git` should not be) to close this class of stub-swallowed errors.

## Recommendation

**Do NOT change `open-pr`'s semantics.** Its never-pushes invariant is load-
bearing for existing callers; a command that commits and pushes is a
qualitatively different privilege level. Instead add a **new command**
(working name `propose-pr`), designed as:

1. **Explicit file scope, not "commit the dirty tree".** Signature along the
   lines of `propose-pr <dir> --message <msg> <paths...>`: commit ONLY the
   listed paths, refuse if any listed path has no changes in status. The
   operator's working copy may contain other unrelated uncommitted work —
   a blind `git add -A && commit` would leak someone's unfinished changes
   into a public PR branch. Scoping also dissolves the "dirty-tree guard"
   dilemma: unrelated dirt simply stays where it is.
2. **Work in a temporary git worktree off the default branch**, not in the
   operator's live checkout: create worktree → apply/commit the scoped edit
   → push → `gh pr create` → remove worktree. The operator's working copy is
   never touched, and "what if the current checkout is the default branch /
   mid-rebase / dirty" disappears by construction. (This can live entirely
   inside the new command; branch naming is github-checker's call — some
   collision-resistant suffix recommended for parallel edits.)
3. **Invariants preserved:** PR-only, never a push to a default branch,
   never a merge — same spirit as `pull`'s ff-only-by-construction.
4. Keep the existing `gh pr view` idempotency behavior for the created
   branch where it applies.

### Counter-question to dispatcher's own design (for dispatcher, not here)

The worktree approach also implies dispatcher should stop writing edits into
the operator's live working tree at all. If `propose-pr` applies content in
its own worktree, dispatcher's contract becomes "render the new file
content, hand it to propose-pr" — no live-tree mutation, no race with the
operator's manual work, no accidental landing on whatever branch happens to
be checked out. dispatcher's `core/spec_runner_config_actions.py` write path
should be reworked to match once the command exists (dispatcher-side change,
tracked on dispatcher's side).

## Status

**RESOLVED 2026-07-17** — github-checker shipped `propose-pr` (PR #11,
merge `7684d27`; spec PR #9, plan PR #10) implementing exactly the
recommendation below: new command (open-pr untouched), explicit content
passing (`--edit repo-path=content-file`), temp worktree off
`origin/<default>`, `--if-match` stale-base guard, PR-only invariants.
Remaining consumer work (dispatcher side, tracked there): un-gate
`SPEC_RUNNER_CONFIG_WRITE_GATED`, rework the runner to call `propose-pr`
instead of writing the live tree, branch on `detail == "no-op"` (NOT on
ok/exit-code — no-op is `ok=false` + exit 1 by design), add a real-git
integration test.

Original status (historical): blocking — dispatcher's
`core/spec_runner_config_actions.py::_invoke` (the content-PR write path)
did not work end-to-end without this. The read-only side of dispatcher's
feature (viewing/validating the config) was unaffected.

## References

- Finding: dispatcher final whole-branch review of `feat/spec-runner-config-editor`,
  2026-07-17 (session review, not a numbered dispatcher commit).
- `github_checker/actions.py:81-138` (`open_pr`), `github_checker/actions.py:5-6`
  (module docstring stating the never-pushes invariant).
- dispatcher design doc: `docs/superpowers/specs/2026-07-17-spec-runner-config-editor-design.md`
  DESIGN-304 (the "Open question ... verify at implementation time" this
  handoff resolves — unfavorably) and its conditional handoff H-5.
