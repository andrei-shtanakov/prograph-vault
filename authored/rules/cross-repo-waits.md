---
title: Cross-repo waits — a wait not recorded as a blocker edge does not exist
type: rule
status: living
owner: Andrei
updated: 2026-08-17
---

# Cross-repo waits

`inbound-triage.md` governs what arrives from others; `commit-pr-issue-granularity.md`
governs what you create. This rule covers the third leg: **what you are waiting
for** — the moment repo A hands work to repo B (an inbox issue per ADR-ECO-006, a
contract pending upstream, an acceptance run on the other side) and something in A
now depends on the outcome.

---

## 1. The one rule

A cross-repo wait exists **only** as a checkbox item in the waiting repo's
`TODO.md`, carrying `@blocked_by:todo://<repo>/<id>` (canonical) or
`@blocked_by:<repo>#<number>` (transitional, for an inbox issue that has no todo
id on the other side).

Session memory, vault notes, handoff documents and chat may *mirror* the wait,
but must never be its only carrier. A wait recorded anywhere else is invisible to
the machinery and rots silently.

## 2. Why the plane matters — two incidents and a counter-example, one week

- **impresario, observed 2026-08-17.** A session carried «ждём steward» in its
  own notes; steward's acceptance had landed on 2026-08-13. Four days of phantom
  waiting, discovered only by a manual re-check.
- **disputatio, 2026-08-17.** The umbrella's session memory reported "next step
  D3" while the repo had merged D3, D4 and MUT-02/03 a week earlier. Same
  failure, other direction: neighbour state recorded outside the checked plane.
- **The counter-example, same day.** spec-runner's `dec007-vault-note-update`
  sat open with a closed blocker — and the fleet plan-check flagged exactly that
  as `PF-BLOCKER-STALE`. The wake-up signal works. It just watches only
  `TODO.md` edges.

The daily fleet plan-check (devtools `check-plan-fields.py` over the workspace
manifest) computes the waiting-by-blocker bucket and raises `PF-BLOCKER-STALE`
the morning after a blocker closes. Today that signal is the **entire return
leg** of ADR-ECO-006: the requester repo learns its inbox request was delivered
only through this edge. A wait written anywhere else has opted out of the only
alarm clock the ecosystem has.

## 3. Session ritual — both directions

The fleet ritual already checks the inbox (incoming). This rule adds the
outgoing half: at session start, alongside
`gh issue list --label inbox --state open`, review your repo's open items
carrying `@blocked_by`, and treat every `PF-BLOCKER-STALE` finding against your
repo as "your wait is over — act, or re-tag with the real remaining blocker".
Closing the delivered item without acting on it is the one forbidden move: the
finding is the payload, not the noise.

## 4. Known gaps — named, not hidden

- Blockers in the transitional `<repo>#<number>` form are matched textually;
  their *state* (issue closed = delivered) is not yet resolved by the sensor.
  Tracked as devtools inbox `blocker-issue-state-resolution`. Until it lands, an
  inbox-issue wait needs the canonical `todo://` edge on the receiver's side
  when one exists — or an honest manual check when it does not.
- The signal currently surfaces in a red scheduled run; the daily human read is
  Robin's digest. An "unblocked since yesterday" digest section is tracked as
  robin-runtime inbox `digest-unblocked-section`.

## 5. Adoption

The rule is cross-cutting and lives here (SSOT). Repo `CLAUDE.md` files
reference it the way they reference `repo-boundaries.md` and `git-workflow.md`; the
fleet-wide reference line rolls out with the next CLAUDE.md normalization pass,
not as twenty simultaneous PRs.
