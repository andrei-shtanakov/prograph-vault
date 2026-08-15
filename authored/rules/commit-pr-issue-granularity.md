---
title: Granularity — when a commit, when a PR, when an issue (and when a TODO item instead)
type: rule
status: living
owner: Andrei
updated: 2026-08-15
---

# Granularity of commit / PR / issue

`git-workflow.md` says **how** a change travels: feature branch → PR → Copilot review →
human merge → ff-pull. This rule says **when** you reach for each object and **at what
size**. Both operating modes of [[2026-08-15-adr-eco-007-two-modes-and-write-scope]]
share the criteria; per-mode differences are marked *product-delivery* below.

Out of scope, deliberately: what to *do* with things other people opened — inbound
triage, Dependabot classes, Copilot findings, stale PRs. That is `inbound-triage.md`;
this one covers only what you create.

---

## 0. In your own repo the default is a TODO item, not an issue

This is the answer most likely to be got wrong, so it comes first.

**Measured 2026-08-15: three open issues across the entire owned fleet.** The backlog is
not in GitHub issues and never has been — it is `<repo>/TODO.md`, the operational plane
of ADR-ECO-005. Using own-repo issues as a backlog would create a third plane, which is
exactly what that ADR exists to collapse, and its D6 is explicit that the canonical plan
graph is a **derived projection, never a store**.

| You have… | It goes in |
|---|---|
| work you intend to do later | a `TODO.md` item with `@id` |
| work you are doing now, with a reviewable change set | a branch and a PR |
| something that needs a GitHub-native handle | an issue |

A GitHub-native handle means: a defect reported by someone who does not read your
`TODO.md`; something automation must reference by number; or an inbound request — which
by ADR-ECO-006 is opened by the *sender* in your repo, not by you.

So "issue or PR in my own repo?" is usually the wrong question. If it is ready to build,
it is a PR. If it is not, it is a TODO item. An issue is the exception that needs a
reason.

---

## 1. Commit

> A commit can be understood, checked, and reverted on its own without leaving the
> repository knowingly inconsistent.

**Deserves its own commit:** a contract change together with its fixtures and tests; one
agreed task slice; a batch of review findings resolved together; a consumer's migration
to a new contract pin; documentation that records behaviour already shipped.

**Does not:** every generated file of a single spec; every agent iteration; a draft
superseded within the same session; formatting split away from the change that caused it;
transient evidence; a typo fix inside a slice that is not finished yet.

**Specs and plans are not exempt, and not automatic either.** A spec plus the plan
derived from it is *one* commit, not one per file — and an intermediate draft is not a
commit at all. The history of how the spec was reached belongs to the run ledger.

*product-delivery*: identical criterion. How many iterations an agent needed is a fact
about the run, not about the repository.

---

## 2. Pull request

> A PR is the unit of integration, review, and policy enforcement. It is neither a large
> commit nor a record of every step taken.

**Open a PR when the change:** must reach the default branch; alters executable
behaviour, a contract, an architecture, or an accepted spec; completes an independent
slice; requires its own approval gate; or could be accepted or rejected independently of
whatever comes next.

**The sizing test: one PR is one reason to say no.** If a reviewer could reasonably
accept half and reject half, it is two PRs. This is what rules out both extremes — a PR
per file, and a PR carrying a whole stage of unrelated work.

**Branch naming.**

- *ecosystem-development* — `<kind>/<slug>`, owned by `git-workflow.md`. Not restated
  here: two lists of branch kinds is one more than can stay in agreement.
- *product-delivery* — the PR corresponds to a **stage of the delivery plan**, and the
  branch carries a stable identifier rather than prose alone:

  ```
  product/WS-014-requirements
  arch/WS-014-auth-boundary
  feat/WS-014-M1-user-import
  fix/WS-014-M1-review-round-1
  deploy/WS-014-staging
  ```

  A stage may well need more than one PR; what it must not do is spread one reviewable
  decision across several, or bundle several decisions into one.

**Provenance is required in product-delivery.** The PR body must state which plan, which
stage, and which upstream decision it descends from, so that a merged PR remains
traceable once the run is gone: at minimum the workstream id, the stage id, the spec
refs, and the decision refs. A typed PR-metadata contract is **not** defined here — it is
open work, and prose in the body is the interim carrier.

---

## 3. When the plan turns out to be wrong while a PR is open

**The PR must not silently widen.** Name the outcome using the lifecycle classes of
ADR-ECO-007 D4:

| What you found | Class | Where it goes |
|---|---|---|
| local clarification, scope unchanged | `proceed` | amend the plan item; continue in this PR |
| the scope or an architectural decision must change | `return` | back to the owning gate; this PR narrows or closes |
| separate work, worth doing later | — | a `TODO.md` item (§0) |
| a defect in an earlier stage's output *within this run* | `return` | feedback to that stage through the orchestrator — not a new PR against its result |

The distinction that matters: a scope change is a decision belonging to whoever owns that
gate. Absorbing it into the open PR moves an authority decision into an implementation
step, where nobody will see it.

---

## 4. Issue in another repository

Already decided elsewhere; nothing is added here.

- **Ecosystem target** — ADR-ECO-006: an `inbox` issue in the target repo, `slug:` +
  `from:` + prose. Acceptance is derived, never stored.
- **External target** — ADR-ECO-007 D2: the handoff adapter declared by the workflow; a
  GitHub issue where the target supports one.

Two invariants worth restating because they are the ones broken in practice: never edit
the neighbouring repo, and never convert an inbound request into a plan item on the
sender's behalf — accepting it is the target owner's act.

---

## 5. What none of these objects are

The **run ledger**. Agent iterations, retries, cost, intermediate reasoning, and
superseded drafts are audit trail. Pushing them into commits makes the history unreadable
and the ledger redundant; the two carry different questions — *what does this repository
now contain* versus *how did we get here*.

---

## Enforcement

Layer 1 in the ladder of ADR-ECO-007 D5: prose. **Nothing in this rule is checked by CI
today**, and it is stated rather than implied, because the fleet has fresh evidence of
what an unchecked written rule is worth — 14 notes in `authored/notes/` lack the
frontmatter `CLAUDE.md` §7 requires, and two commits of a note sat undelivered on a local
branch for three days while every merged-branch check reported clean. A rule without an
instrument decays quietly.
